import RPi.GPIO as GPIO
import dht11
import time

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

while True:
    # read data using pin 13
    instance = dht11.DHT11(pin = 13)
    result = instance.read()
    '''
    while not result.is_valid():
        result = instance.read()
    
    print("Temperature: %-3.1f C" % result.temperature)
    print("Humidity: %-3.1f %%" % result.humidity)
    
'''    

    if result.is_valid():
        print("Temperature: %-3.1f C" % result.temperature)
        print("Humidity: %-3.1f %%" % result.humidity)
        time.sleep(2)
    '''    
    else:
        print("Error: %d" % result.error_code)
    '''
        
    
    

