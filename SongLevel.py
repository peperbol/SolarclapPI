__author__ = 'Pepijn W'

import Ticker
import pygame
import threading
import GpioInput
import math
import Hand
import Tick


class SongLevel:
    def __init__(self, song, bpm):
        self.song = "Sound/" + song + ".wav"
        self.sequence = "Sequence/test_" + song + ".txt"
        self.bpm = bpm
        self.playing = False


    def play(self, hands):
        pygame.mixer.init()
        pygame.mixer.music.load(self.song)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()

        ticker = Ticker.Ticker(self.bpm)

        tickSequence = self.makeTickSequence(hands)

        t = threading.Thread(target=GpioInput.GpioInputHandler, args=[self, hands])
        t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.

        lastT = 0
        self.currentTick = tickSequence[0];
        self.playing = True
        t.start()
        for t in ticker.Ticks(0):
            if t >= len(tickSequence) :
                break

            DeltaT = t- lastT;

            self.currentTick.end()
            print("---")
            self.currentTick = tickSequence[t];

            for h in hands:
                text = h.name + ":"
                while len(text) < 10:
                    text += " "
                text+= "|"
                for i in range(t, min(t+8, len( tickSequence))):
                    if tickSequence[i].getOther(h):
                        text += tickSequence[i].getOther(h).color;
                    else:
                        text += "."
                print(text)

            lastT = t;

        self.playing = False

    def makeTickSequence(self, hands):
        file = open(self.sequence, 'r')
        lines = file.readlines();
        seq = []
        for l in lines:
            if "#" in l:
                break
            pairs = []
            for i in range(math.floor(len(l)/2)):
                pairs.append( Hand.HandPair(hands[min( int(l[i*2]),int(l[i*2+1]) )],hands[max( int(l[i*2]),int(l[i*2+1]) )]))
            seq.append(Tick.Tick(pairs) )
        return  seq
