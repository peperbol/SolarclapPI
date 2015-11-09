__author__ = 'Pepijn W'
import RPi.GPIO as GPIO
print("hi")
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)
print("off")
GPIO.output(17,GPIO.LOW)