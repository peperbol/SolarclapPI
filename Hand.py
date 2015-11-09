__author__ = 'Pepijn W'


class Hand:
    def __init__(self, color, name, pin):
        self.color = color
        self.name = name
        self.pin = pin

class HandPair:
    def __init__(self, hand1: Hand, hand2: Hand):
        self.hands = [hand1,hand2]
        self.clapped = False

    def isTheSameAs(self, hand1, hand2):
        return (hand1 in self.hands) and (hand2 in self.hands)

    def getOther(self, hand):
        if (hand in self.hands):
            if self.hands.index(hand) == 0:
                return self.hands[1]
            else:
                return  self.hands[0]
        return False
    def end(self):
        if not self.clapped:
            print("Missed!")
