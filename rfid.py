import RPi.GPIO as GPIO
import time
import sys
from mfrc522 import SimpleMFRC522


reader = SimpleMFRC522()

LED = 18
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)

my_uid = 797306821553

try:
    while True:
        id, uid = reader.read()
        print(uid)
        if id == my_uid:                
            print("Access Granted")
            GPIO.output(LED, GPIO.HIGH)  
            time.sleep(5)                
            GPIO.output(LED, GPIO.LOW)   
            
        else:                            
            print("Access Denied, YOU SHALL NOT PASS!")
            
except KeyboardInterrupt:
    GPIO.cleanup()
    raise

