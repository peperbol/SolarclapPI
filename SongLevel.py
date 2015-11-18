__author__ = 'Pepijn W'

import Ticker
import pygame
import threading
import GpioInput
import math
import Hand
import Tick
import NeoPixelDisplay
import Score
import time

class SongLevel:
    def __init__(self, song, bpm):
        self.song = "Sound/" + song + ".wav"
        self.sequence = "Sequence/" + song + ".txt"
        self.bpm = bpm
        self.playing = False


    def play(self, hands):
        pygame.mixer.init()
        pygame.mixer.music.load(self.song)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()

        ticker = Ticker.Ticker(self.bpm)

        tickSequence = self.makeTickSequence(hands)
        score = Score.Score(self.countBeats(tickSequence))

        t = threading.Thread(target=GpioInput.GpioInputHandler, args=[self, hands])
        t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.

        display = NeoPixelDisplay.NeoPixelDisplay(hands,tickSequence)

        lastT = 0
        self.currentTick = tickSequence[0]
        self.playing = True
        t.start()
        for t in ticker.Ticks(0):
            if t >= len(tickSequence) :
                break

            DeltaT = t- lastT
            self.currentTick.end(score)
            self.currentTick = tickSequence[t]

            display.display(t,score)
            self.DebugLog(hands, tickSequence, t)

            lastT = t

        self.playing = False
        time.sleep(1)

    def DebugLog(self, hands, tickSequence, t):
        print("---")
        for h in hands:
            text = h.name + ":"
            while len(text) < 15:
                text += " "
            text+= "|"
            for i in range(t, min(t+8, len( tickSequence))):
                if tickSequence[i].getOther(h):
                    text += tickSequence[i].getOther(h).name[0]
                else:
                    text += "."
            print(text)

    def countBeats(self, tickSequence):
        counter = 0
        for tick in tickSequence:
            if tick.hasPairs():
                counter += 1
        return counter

    def makeTickSequence(self, hands):
        file = open(self.sequence, 'r')
        lines = file.readlines()
        seq = []
        for l in lines:
            if "#" in l:
                break
            pairs = []
            for i in range(int(math.floor((len(l)-2)/2))):
                pairs.append( Hand.HandPair(hands[min( int(l[i*2]),int(l[i*2+1]) )],hands[max( int(l[i*2]),int(l[i*2+1]) )]))
            seq.append(Tick.Tick(pairs) )
        return  seq
