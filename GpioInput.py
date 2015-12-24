__author__ = 'Pepijn W'


import RPi.GPIO as GPIO
import SongSelectMenu

IsGpioSet = False

def setGPIO():
    global IsGpioSet
    if not IsGpioSet:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        IsGpioSet = True


def GpioButtonInputHandler(pin1, pin2):
    global buttoncallback
    setGPIO()

    GPIO.setup(pin1, GPIO.IN)
    GPIO.setup(pin2, GPIO.IN)

    pin1Press = False;
    pin2Press = False;
    while SongSelectMenu.ssm.gameRunning:
        if(GPIO.input(pin1)):
            if not pin1Press:
                pin1Press = True
                buttoncallback.b1(pin1Press, pin2Press)
        else:
            pin1Press = False

        if(GPIO.input(pin2)):
            if not pin2Press:
                pin2Press = True
                buttoncallback.b2(pin1Press, pin2Press)
        else:
            pin2Press = False

class ButtonCallback:
    def __init__(self, b1, b2):
        self.b1 = b1
        self.b2 = b2

buttoncallback = ButtonCallback(lambda : 0,lambda :0)

def GpioHandInputHandler( level, hands):
    setGPIO()

    inputs = []
    for i in range(len(hands)):
        for j in range(i+1,len(hands )):
            inputs.append(InputPair(level,hands[i], hands[j]))

    def checkInput(check, other):
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