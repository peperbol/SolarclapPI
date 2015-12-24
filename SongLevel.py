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
import SongSelectMenu

class SongLevel:
    def __init__(self, song, bpm, hands):
        self.song = "Sound/" + song + ".wav"
        self.sequence = "Sequence/" + song + ".txt"
        self.spokenname = "menu/" + song + ".wav"
        self.bpm = bpm
        self.playing = False
        self.hands = hands


    def play(self):
        pygame.mixer.music.load(self.song)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()

        ticker = Ticker.Ticker(self.bpm)

        tickSequence = self.makeTickSequence(self.hands)
        score = Score.Score(self.countBeats(tickSequence))

        tr = threading.Thread(target=GpioInput.GpioHandInputHandler, args=[self, self.hands])
        tr.daemon = True  # thread dies when main thread (only non-daemon thread) exits.

        def stop(b1,b2):
            if b1 and b2:
                self.playing = False

        GpioInput.buttoncallback = GpioInput.ButtonCallback(stop, stop)

        display = NeoPixelDisplay.NeoPixelDisplay(self.hands,tickSequence)

        lastT = 0
        self.currentTick = tickSequence[0]
        self.playing = True
        tr.start()
        for t in ticker.Ticks(0):
            if not self.playing or t >= len(tickSequence) :
                break

            DeltaT = t- lastT
            self.currentTick.end(score)
            self.currentTick = tickSequence[t]

            display.display(t,score)
            self.DebugLog(self.hands, tickSequence, t)

            lastT = t


        pygame.mixer.music.stop()
        t = len(tickSequence)
        self.playing = False
        time.sleep(2)
        for frame in score.sort(3):
            display.display(t,frame)
        SongSelectMenu.ssm.activate()

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
