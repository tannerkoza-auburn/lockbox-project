import RPi.GPIO as GPIO
import time
from transitions import Machine, State
from relay import *



class OurBox:

    # Possible LockBox States
    states = [
        State(name='double_locked'),
        State(name='single_locked'),
        State(name='unlocked')
    ]

    # OurBox Instance Initialization
    def __init__(self):
        # Initialize the State Machine
        self.machine = Machine(model=self, states=OurBox.states, initial='double_locked')

        # Define Transitions
        self.machine.add_transition('rfid_unlocking', 'double_locked', 'single_locked', after= 'rfid_unlock')
        self.machine.add_transition('face_unlocking', 'single_locked', 'unlocked', after= 'face_unlock')
        self.machine.add_transition('locking', 'unlocked', 'double_locked', after= 'manual_lock')
        
        # GPIO Setup
        self.lockLED = 20
        self.scanLED = 27
        self.unlockLED = 22
        self.relay4 = 18

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.lockLED, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.scanLED, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.unlockLED, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.relay4, GPIO.OUT, initial=GPIO.LOW)

        # Lock OurBox Instance and begin RFID scan
        self.auto_lock()


    # Define Methods that control hardware

    def rfid_unlock(self):
            print('RFID SCAN...\n')
            GPIO.output(self.scanLED, GPIO.HIGH)
            time.sleep(10)
            print('ACCESS GRANTED\n')
            self.state
            self.face_unlocking()       

    def face_unlock(self):
        print('FACE SCAN...\n')
        future = time.time() + 10
        while True:
            if time.time() < future:
                GPIO.output(self.scanLED, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(self.scanLED, GPIO.LOW)
                time.sleep(0.5)
            else:
                self.relay()
                break
            
        GPIO.output(self.scanLED, GPIO.LOW)
        GPIO.output(self.lockLED, GPIO.LOW)
        GPIO.output(self.unlockLED, GPIO.HIGH)
        print('ACCESS GRANTED\n')
        self.state
        self.locking()

    def auto_lock(self):
        print('LOCKED\n')
        GPIO.output(self.unlockLED, GPIO.LOW)
        GPIO.output(self.lockLED, GPIO.HIGH)
        self.state
        self.rfid_unlocking()
        
    def manual_lock(self):
        lock_cmd = input('PRESS ENTER TO LOCK\n')
        print('LOCKED\n')
        GPIO.output(self.unlockLED, GPIO.LOW)
        GPIO.output(self.lockLED, GPIO.HIGH)
        self.state
        self.rfid_unlocking()
        
    def relay(self):
        GPIO.output(self.relay4, GPIO.HIGH)
        
try:
    BOX = OurBox()
    print('CTRL + C TO CANCEL/CLEAN')          
except KeyboardInterrupt:
    GPIO.cleanup()