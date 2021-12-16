import RPi.GPIO as GPIO
import time
import glob
import dht11
import pigpio
import socket
import json
from datetime import datetime
import requests


base_url = "http://2f46-160-39-38-116.ngrok.io"
port_from_server = 1234
port_from_esp = 1235

hum_rain = 50
hum_dry = 10
wind_max = 10


def read_hum(instance):
    while True:
        result = instance.read()
        if result.is_valid():
            return result.humidity


def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp = float(temp_string) / 1000.0
        return temp


def status_compare(weather, preference, cur_status):
    reason = None
    if preference.close_when_rainy and weather["hum_out"] > hum_rain:
        reason = "Outside is rainy."
        return 0, reason
    if preference.close_when_dry and weather["hum_out"] < hum_dry:
        reason = "Outside is too dry."
        return 0, reason
    if preference.close_when_windy and weather["wind_speed"] > wind_max:
        reason = "Outside is windy."
        return 0, reason
    if abs(weather["hum_in"] - weather["hum_out"]) > preference.diff_hum:
        reason = "Balance indoor and outdoor humidities."
        cur_status = 1
    if preference.temp_min <= weather["temp_out"] <= preference.temp_max:
        if abs(weather["temp_in"] - weather["temp_out"]) > preference.diff_temp:
            reason = "Balance indoor and outdoor temperatures."
            cur_status = 1
    else:
        reason = "Outdoor temperature is not in the range."
        return 0, reason
    return cur_status, reason


def request_to_server(url, data):
    headers = {'conten-type': 'application/json'}
    response = requests.post(url=url, headers=headers, json=data)
    if response.text != "200":
        print("Request Failed!")


def rotate_servo(pwm, degree):
    pwm.set_servo_pulsewidth(500 + degree * 100 / 9)


class Preference:
    def __init__(self):
        self.user = None
        self.close_when_rainy = None
        self.close_when_dry = None
        self.close_when_windy = None
        self.temp_min = None
        self.temp_max = None
        self.diff_temp = None
        self.diff_hum = None

    def set(self, information):
        self.user = information["username"]
        self.close_when_rainy = information["close_when_rainy"]
        self.close_when_dry = information["close_when_dry"]
        self.close_when_windy = information["close_when_windy"]
        self.temp_min = information["temp_min"]
        self.temp_max = information["temp_max"]
        self.diff_temp = information["diff_temp"]
        self.diff_hum = information["diff_hum"]


if __name__ == "__main__":
    # Initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    # Set temperature sensor data dir
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')
    device_file_in = device_folder[0] + '/w1_slave'
    device_file_out = device_folder[1] + '/w1_slave'

    # Initialize humidity sensor
    hum_sensor_out = dht11.DHT11(pin=33)
    hum_sensor_in = dht11.DHT11(pin=37)

    # Initialize PWM
    servo = 18
    pwm = pigpio.pi()
    pwm.set_mode(servo, pigpio.OUTPUT)
    pwm.set_PWM_frequency(servo, 50)
    rotate_servo(pwm, 0)

    # Set requests url
    url_weather = base_url + "/data/post_weather"
    url_history = base_url + "/data/post_history"

    # Initialize sockets
    addr = ("0.0.0.0", port_from_server)
    socket_from_server = socket.socket()
    socket_from_server.setblocking(False)
    socket_from_server.settimeout(0.3)
    socket_from_server.bind(addr)
    socket_from_server.listen(5)

    addr = ("0.0.0.0", port_from_esp)
    socket_from_esp = socket.socket()
    socket_from_esp.bind(addr)
    socket_from_esp.listen(5)

    # Initialize user's preference
    preference = Preference()

    # Initialize wind speed
    wind_speed = 0

    # Initialize window status
    cur_status = 0
    pre_status = 0

    sent = False
    while True:
        try:
            conn_from_server, addr_server = socket_from_server.accept()
        except OSError:
            # Read indoor and outdoor temperature
            temp_in = read_temp(device_file_in)
            temp_out = read_temp(device_file_out)

            # Read indoor and outdoor humidity
            hum_in = read_hum(hum_sensor_in)
            hum_out = read_hum(hum_sensor_out)

            # Receive wind speed from esp
            conn_from_esp, addr_esp = socket_from_esp.accept()
            data = conn_from_esp.recv(4096).decode()
            data = json.loads(data)
            wind_speed = data["wind_speed"]

            weather = {
                "temp_in": temp_in,
                "temp_out": temp_out,
                "hum_in": hum_in,
                "hum_out": hum_out,
                "wind_speed": wind_speed
            }

            # Judge whether to close or open the window
            if preference.user is None:
                # When there is no user, keep the window closed
                rotate_servo(pwm, 0)
            else:
                cur_status, reason = status_compare(weather, preference, cur_status)
                # If window's status changes, send data to the server
                if cur_status != pre_status:
                    if cur_status == 1:
                        rotate_servo(pwm, 80)
                        status = "Opened"
                    else:
                        rotate_servo(pwm, 0)
                        status = "Closed"
                    history = {
                        "status": status,
                        "user": preference.user,
                        "reason": reason
                    }
                    print(status)
                    request_to_server(url_history, history)
                    request_to_server(url_weather, weather)
                pre_status = cur_status

            # Send data every 10 minutes
            minute = datetime.now().minute
            if minute % 10 == 0:
                if not sent:
                    request_to_server(url_weather, weather)
                    sent = True
            else:
                sent = False

            time.sleep(1)

        else:
            information = conn_from_server.recv(4096).decode()
            if len(information) > 0:
                information = json.loads(information)
                print(information)
                preference.set(information)
