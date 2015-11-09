__author__ = 'Pepijn W'


import RPi.GPIO as GPIO
import SongLevel
import Hand


def GpioInputHandler( level, hands):
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    GPIO.setwarnings(False)

    inputs = []
    for i in range(len(hands)):
        for j in range(i+1,len(hands )):
            inputs.append(InputPair(level,hands[i], hands[j]))

    def checkInput(check:Hand.Hand, other):
        for o in other:
            GPIO.setup(o.pin,GPIO.IN)
        GPIO.setup(check.pin,GPIO.OUT)
        GPIO.output(check.pin,GPIO.HIGH)
        for o in other:
            for i in inputs :
                if i.isTheSameAs(check, o):
                    i.input( GPIO.input(o.pin))

    while(level.playing):
        for i in range(len(hands)):
            other = []
            for j in range(len(hands)):
                if j != i:
                    other.append(hands[j])
            checkInput(hands[i], other)

class InputPair:
    def __init__(self, level, hand1, hand2):
        self.level = level;
        self.pressed = False;
        self.hands = [hand1,hand2]

    def isTheSameAs(self, hand1, hand2):
        return (hand1 in self.hands) and (hand2 in self.hands)

    def input(self, pressed ):
        if self.pressed == pressed:
            return
        self.pressed = pressed
        if pressed:
            #print(self.hands[0].name + " touched " +self.hands[1].name)
            self.level.currentTick.clap(self.hands[0], self.hands[1])