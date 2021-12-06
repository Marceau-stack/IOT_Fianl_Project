import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

In_Pin=35

GPIO.setup(In_Pin,GPIO.OUT,initial=GPIO.LOW)
p=GPIO.PWM(In_Pin,50)
p.start(0)
str1="please input the degree(0<=a<=180)\nor press q to quit\n"
r=input(str1)
try:
    while not r=="q":
        if r.isdigit():
            r=int(r)
        else:
            print("please input a number(0<=num<=180)")
            continue
        if r<0 or r>180:
            print("a must be [0,180]")
            continue
        p.ChangeDutyCycle((2.5+r/360*20))
        time.sleep(0.02)
        r=str(input(str1))
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()