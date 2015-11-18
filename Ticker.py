__author__ = 'Pepijn W'
import time
import math

class Ticker:
    def __init__(self, bpm):
        self.startTime =  time.time()
        self.timeBetween = float(60)/bpm
    #makes sure to have the right timing
    def Ticks(self, delayOffset):
        currentTime = 0
        startTime =  time.time() + delayOffset;

        while True:
            currentTime = time.time() - startTime
            #print(self.timeBetween)
            nextTick = max(math.ceil(currentTime/ self.timeBetween),1)
            nextTime = nextTick * self.timeBetween
            time.sleep(nextTime - currentTime)
            yield int(nextTick)
