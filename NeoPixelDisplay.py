
from neopixel import *

class NeoPixelDisplay:
    def __init__(self,  hands, tickSequence):
        self.ledsPerGlove = 4
        self.headerLeds = 7
        self.validationLED = 0
        self.progressLED = 1
        self.ammOfProgressLEDs = 6

        self.validationBrightness = 0.4
        self.progressBrightness = 0.4
        self.handBrightness = 0.4

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
        self.strip.setPixelColor(self.getLedPositionOnStrip(glove,num),  self.dampColor( color,self.handBrightness))

    def display(self, t, score):
        #header

        # validation
        col = self.OFF;
        if t>0 :
            if self.tickSequence[t-1].hasPairs():
                if self.tickSequence[t-1].isSucceeded():
                    col = Color(0,255,0)
                else:
                    col = Color(255,0,0)
        self.strip.setPixelColor(self.validationLED, self.dampColor( col,self.validationBrightness))

        # - progress
        beatsPerLed = score.getPartLenth(self.ammOfProgressLEDs)
        for i in range(self.ammOfProgressLEDs):
            part = score.getPart(beatsPerLed,i)
            brightness = float(len(part))/beatsPerLed
            prG= score.getProcentGood(part)
            prW= score.getProcentWrong(part)
            multipl = 1 / max(prG,prW)
            c = Color(min(255,int(multipl*prW*255)),min(255,int(multipl*prG*255)),0 )
            c = self.dampColor(c,brightness)
            self.strip.setPixelColor(self.progressLED+i,  self.dampColor( c,self.progressBrightness))

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

    def dampColor(self,color,brightness):
        red = (color >>16) % 256
        green = (color >>8) % 256
        blue = (color >>0) % 256
        return Color(int(red*brightness),int(green*brightness),int(blue*brightness))

