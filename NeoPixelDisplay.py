
from neopixel import *

class NeoPixelDisplay:
    def __init__(self,  hands, tickSequence):
        self.ledsPerGlove = 4
        self.headerLeds = 1

        self.hands = hands
        self.tickSequence= tickSequence
        PIN = 18
        self.strip = Adafruit_NeoPixel(self.getLedCount(), PIN, brightness=255 )
        self.OFF = 0
        self.strip.begin()

    def getLedPositionOnStrip(self, glove, num ):
        return self.ledsPerGlove * glove + num + self.headerLeds

    def getLedCount(self):
        return self.ledsPerGlove * len(self.hands) + self.headerLeds

    def setLedColor(self, glove, num, color):
        self.strip.setPixelColor(self.getLedPositionOnStrip(glove,num), color)

    def display(self, t):
        #header
        # todo: implement header leds
        col = self.OFF;
        if t>0 :
            if self.tickSequence[t-1].hasPairs():
                if self.tickSequence[t-1].isSucceeded():
                    col = Color(0,255,0)
                else:
                    col = Color(255,0,0)
        self.strip.setPixelColor(0, col)

        #hands
        for h in range(len(self.hands)):
            hand = self.hands[h]

            for i in range(self.ledsPerGlove):
                if t+i >= len(self.tickSequence): #buiten de range van de sequence
                    self.setLedColor(h,i,self.OFF)
                    continue
                r = self.tickSequence[t+i].getOther(hand) #
                if r:
                    self.setLedColor(h,i, r.color)
                else:
                    self.setLedColor(h,i,self.OFF)

        self.strip.show()



