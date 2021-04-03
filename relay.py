import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

RELAIS_1_GPIO = 18
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign Mode
GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # on
