import time
import RPi.GPIO as GPIO
from transitions import Machine, State
from mfrc522 import SimpleMFRC522
from facial_rec import *


# Define Lock Box Class
class OurBox:
    # Possible LockBox States
    states = [
        State(name='double_locked'),    # Completely Locked
        State(name='single_locked'),    # RFID Unlocked; Facial Recognition Locked
        State(name='unlocked')  # Specified Compartment Unlocked
    ]

    # OurBox Instance Initialization
    def __init__(self):
        # Initialize the State Machine
        self.machine = Machine(model=self, states=OurBox.states, initial='double_locked')

        # Define Transitions
        self.machine.add_transition('rfid_unlocking', 'double_locked', 'single_locked', after='rfid_unlock')    # RFID Unlocking
        self.machine.add_transition('face_unlocking', 'single_locked', 'unlocked', before='face_unlock',    # Facial Recognition Unlocking
                                    after='locking')
        self.machine.add_transition('denied_locking', 'single_locked', 'double_locked', after='auto_lock')  # Facial Recognition Denied Locking
        self.machine.add_transition('locking', 'unlocked', 'double_locked', before='manual_lock',   # RFID Locking
                                    after='rfid_unlocking')

        # GPIO Setup
        self.lockLED = 0    # Locked Indicator
        self.scanLED = 0    # RFID & Facial Scanning Indicator
        self.unlockLED = 0  # Unlocked Indicator
        self.relay_j = 18   # Justin's Compartment Relay
        self.relay_t = 23   # Tanner's Compartment Relay
        self.relay_d = 24   # Danilo's Compartment Relay

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.lockLED, GPIO.OUT, initial=GPIO.LOW)    # Start All Pins Low
        GPIO.setup(self.scanLED, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.unlockLED, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.relay_j, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.relay_t, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.relay_d, GPIO.OUT, initial=GPIO.LOW)

        # RFID Setup
        self.my_uid = [97306821553, 1070020666444]   # Badge ID Numbers

        # Lock OurBox Instance and begin RFID scan
        self.auto_lock()

    # Define Hardware Functions
    def relay_ctrl(self, user_id):
        """This functions takes in a user's name and opens their respective compartment.
        """

        # Define Opening Logic
        if user_id == 'Justin':
            GPIO.output(self.relay_j, GPIO.HIGH)    # Open Justin's Compartment
            print('ACCESS GRANTED. Hello Justin!\n')

        elif user_id == 'Tanner':
            GPIO.output(self.relay_t, GPIO.HIGH)  # Open Tanner's Compartment
            print('ACCESS GRANTED. Hello Tanner!\n')

        elif user_id == 'Danilo':
            GPIO.output(self.relay_d, GPIO.HIGH)  # Open Danilo's Compartment
            print('ACCESS GRANTED. Hello Danilo!\n')

        else:
            print('PERMISSION DENIED.\n')
            self.denied_locking()   # Trigger Denied Locking to Start RFID Scan

    # Define State Methods
    def rfid_unlock(self):
        """This method creates an instance of the RFID scanner and continually scans until a known badge is recognized.
         After recognized, this method initiates the facial recognition scan.
         """

        print('RFID SCAN...\n')

        reader = SimpleMFRC522()    # Define RFID Reader Instance

        while True:
            uid = reader.read()    # Read RFID Values and Save Badge Numbers
            
            if id == self.my_uid[0] or self.my_uid[1]:
                print('ACCESS GRANTED.\n')
                break
            else:
                print('ACCESS DENIED!\n')

        self.face_unlocking()   # Initiate Facial Recognition Scan with Recognized Badge

    def face_unlock(self):
        """This method calls the facial recognition method and relay control function.
        The facial recognition method checks for a known user for a period of time. If a known user is recognized, that user's name is passed to the relay control function
        to open the user's compartment. If no user is recognized, the scan times out and returns to the RFID scan.
        """

        print('FACE SCAN...\n')

        user = self.facialRec()     # Runs Facial Recognition Method and Saves Identified User
        self.relay_ctrl(user)    # Takes Identified User and Opens Their Compartment

    def auto_lock(self):
        """This method automatically "locks" the box if the face scan times out.
        The box will return to the RFID scan and change the state of the indicators.
        """

        print('LOCKED\n')

        self.rfid_unlocking()

    def manual_lock(self):
        """This method is like the rfid_unlock method except it locks the box when the user completes their task."""

        print('RFID SCAN TO LOCK.\n')

        reader = SimpleMFRC522()  # Define RFID Reader Instance

        while True:
            uid = reader.read()  # Read RFID Values and Save Badge Numbers
            
            if id == self.my_uid[0] or self.my_uid[1]:
                GPIO.output(self.relay_j, GPIO.LOW)    # Locks All Compartments In Case One Is Open
                GPIO.output(self.relay_t, GPIO.LOW)
                GPIO.output(self.relay_d, GPIO.LOW)

                print('SUCCESSFUL MANUAL LOCK.\n')
                
                time.sleep(5)  # Sleep for 5 seconds to avoid RFID unlock
                break
            else:
                print('TRY AGAIN!\n')
                
    # Define External Facial Recognition Method
    facialRec = facial_rec  # Imports facial_rec from facial_rec.py


try:
    print('CTRL + C TO CANCEL/CLEAN.\n')
    BOX = OurBox()  # Creates Instance of Class
except KeyboardInterrupt:
    GPIO.cleanup()
