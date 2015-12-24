
#from neopixel import *
import serial
import struct
from numpy.f2py.auxfuncs import throw_error


class NeoPixelDisplay:
    def __init__(self,  hands, tickSequence):
        self.ledsPerGlove = 4
        self.validationLED = 0
        self.progressLED = 1
        self.ammOfProgressLEDs = 6

        self.validationBrightness = 0.4
        self.progressBrightness = 0.4
        self.handBrightness = 0.4

        self.hands = hands
        self.tickSequence= tickSequence
        #PIN = 18
        serialset = False
        serialnum = 0;
        while not serialset:
            try:

                self.serial = serial.Serial('/dev/ttyACM'+ str(serialnum), 9600)
                serialset = True
            except serial.serialutil.SerialException:
                serialset = False
                serialnum += 1
                if serialnum >9:
                    raise

        self.colorArray = []
        for i in range(self.getLedCount()*3):
            self.colorArray.append(0)

        self.OFF = Color(0,0,0)
        self.show()

    def getLedPositionOnStrip(self, glove, num ):
        return self.ledsPerGlove * glove + num + self.ammOfProgressLEDs +1

    def getLedCount(self):
        return self.ledsPerGlove * 8 + self.ammOfProgressLEDs +1

    def setLedColor(self, glove, num, color):
        self.setPixelColor(self.getLedPositionOnStrip(glove,num),  self.dampColor( color,self.handBrightness))

    def setPixelColor(self, pos, color):
        self.colorArray[pos*3+0] = color.r
        self.colorArray[pos*3+1] = color.g
        self.colorArray[pos*3+2] = color.b

    def show(self):

        self.serial.write('0')
        for i in self.colorArray:

            self.serial.write(struct.pack('!B',i))
        #for i in range(self.serial.inWaiting()):
        self.serial.write('#')
    def clear(self):
        for i in range(len(self.colorArray)):
            self.colorArray[i] = 0

    def display(self, t, score):
        self.clear();
        #header

        # validation
        col = self.OFF
        if t>0 :
            if self.tickSequence[t-1].hasPairs():
                if self.tickSequence[t-1].isSucceeded():
                    col = Color(0,255,0)
                else:
                    col = Color(255,0,0)
        self.setPixelColor(self.validationLED, self.dampColor( col, self.validationBrightness))

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
            self.setPixelColor(self.progressLED+i,  self.dampColor( c,self.progressBrightness))

        #hands
        for h in range(len(self.hands)):
            hand = self.hands[h]

            for i in range(self.ledsPerGlove):
                if t+i >= len(self.tickSequence): #buiten de range van de sequence
                    self.setLedColor(h,i,self.OFF)
                    continue
                r = self.tickSequence[t+i].getOther(hand)
                if r:
                    self.setLedColor(h,i, r.color)
                else:
                    self.setLedColor(h,i,self.OFF)

        self.show()

    def dampColor(self,color,brightness):
        return Color(int(color.r*brightness),int(color.g*brightness),int(color.b*brightness))

class Color:
    def __init__(self,r,g,b):
        self.r = r
        self.g = g
        self.b = b