import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

In_Pin=3

GPIO.setup(In_Pin,GPIO.OUT,initial=GPIO.LOW)
p=GPIO.PWM(In_Pin,50)
p.start(0)
def SetAngle(angle):
    duty = angle / 360*20 + 2.5
    GPIO.output(3, True)
    p.ChangeDutyCycle(duty)
    sleep(1)
    
for i in range(0, 180, 10):
    SetAngle(i)
for i in range(180, 0, -10):
    SetAngle(i)
p.stop()
GPIO.cleanup()