__author__ = 'Pepijn W'

import Hand

class Tick:

    def __init__(self, pairs):
        self.pairs = pairs

    def clap(self, hand1, hand2):
        handled = False

        for p in self.pairs:
            if(p.isTheSameAs(hand1, hand2)):
                handled = True
                p.clapped = True

        if handled:
            print("Clap!")
        else:
            print("Mislap!")

    def getOther(self, hand):
        for p in self.pairs:
            if(p.getOther(hand)):
                return p.getOther(hand)
        return False

    def end(self):
        for p in self.pairs:
            p.end()

    def hasPairs(self):
        return len(self.pairs) > 0

    def isSucceeded(self):
        result = True
        for p in self.pairs:
            result &= p.clapped
        return result
