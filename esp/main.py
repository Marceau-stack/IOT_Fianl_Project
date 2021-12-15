import machine
from machine import ADC
import time,onewire,ds18x20
from machine import Pin, PWM
import json
import socket
import network

def GetTemp(ds):
        roms = ds.scan()
        ds.convert_temp()
        time.sleep_ms(500)
        for rom in roms:
                print("temp",ds.read_temp(rom))
        return(ds.read_temp(rom))

ESSID = "Tanvi"
PASSWD = "12345678"

wlan = network.WLAN(network.STA_IF)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.active(True)
    wlan.connect(ESSID, PASSWD)
    while not wlan.isconnected():
        pass
print("connected")        

if __name__=='__main__':
        adc=ADC(0)

        ow=onewire.OneWire(Pin(14))
        ds=ds18x20.DS18X20(ow)
        
        addr = ("172.20.10.7", 1235)
        while True:
                #print(adc.read()) 
                speed=pow((float(adc.read()) - 264.0) / 85.6814, 3.3)
                print("windspeed",speed)
                temp1=GetTemp(ds)

                data = {"wind_speed":speed, "temp_out":temp1}
                data = json.dumps(data)
                s = socket.socket()
                s.connect(addr)
                s.send(data.encode())
                s.close()

                time.sleep(2)