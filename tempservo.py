import RPi.GPIO as GPIO
import time
import glob

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')

GPIO.setmode(GPIO.BOARD)
In_Pin=35

GPIO.setup(In_Pin,GPIO.OUT,initial=GPIO.LOW)
p=GPIO.PWM(In_Pin,50)

def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return(temp_c, temp_f)
    
def temp_compare(temp_in,temp_out):
    if temp_out-temp_in>1:
        cur_status=1
    else:
        cur_status=0
    return (cur_status)
    

p.start(0)
p.ChangeDutyCycle(2.5)
post_status=0
cur_status=0
while True:
    device_file = device_folder[0] + '/w1_slave'
    device_file_out = device_folder[1] + '/w1_slave'
    
    post_status=cur_status
    temp_in=read_temp(device_file)[0]
    temp_out=read_temp(device_file_out)[0]
    cur_status=temp_compare(temp_in,temp_out)
    
    print(read_temp(device_file))
    print(read_temp(device_file_out))
    
    if cur_status!=post_status and cur_status==1:
        print("Change to Open")
        r=180
        p.ChangeDutyCycle((2.5+r/360*20))
        time.sleep(2)
    elif cur_status!=post_status and cur_status==0:
        print("Change to Close")
        r=90
        p.ChangeDutyCycle((2.5+r/360*20))
        time.sleep(2)
    else:
        time.sleep(2)
            
    time.sleep(1)
