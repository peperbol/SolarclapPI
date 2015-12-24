__author__ = 'Pepijn W'

import SongSelectMenu
import RPi.GPIO as GPIO
import time

class ExitGame:
    def __init__(self, soundfile):
        self.spokenname = "menu/" + soundfile + ".wav"
    def play(self):
        SongSelectMenu.ssm.gameRunning = False;
        time.sleep(0.1)
        GPIO.cleanup()