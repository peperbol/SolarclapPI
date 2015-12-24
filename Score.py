__author__ = 'Pepijn W'
import math
import time

class Score:
    def __init__(self, total):
        self.total = total
        self.done = []
        self.GOOD = True
        self.WRONG = False

    def addGood(self):
        self.done.append(self.GOOD)

    def addWrong(self):
        self.done.append(self.WRONG)

    def getProcentGood(self, list):
        def f(i): return  i
        if len(list) == 0: return 1
        return float(len(filter(f,list))) / len(list)

    def getProcentWrong(self, list):
        def f(i): return  not i
        if len(list) == 0: return 1
        return float(len(filter(f,list))) / len(list)

    def getPart(self, length, part):
        arr = []
        for i in range(part*length, (part+1) * length):
            if i< len(self.done):
                arr.append(self.done[i])

        return arr

    def getPartLenth(self, ammountofParts):
        return int( math.ceil(self.total / ammountofParts))

    def sort(self, animationlength):
        start = time.time()
        deltatime = 0
        startdone = self.done
        displacements = []
        displacement = 0
        for b in startdone:
            if b :
                displacement += 1
                displacements.append(-1)
            else:
                displacements.append(displacement)

        while deltatime <= animationlength:
            deltatime =  time.time() - start
            pr = min (deltatime/animationlength,1)
            for i in range(len(self.done)):
                self.done[i] = True

            for i in range(len(displacements)):
                if displacements[i] != -1:
                    d = int(round( displacements[i] * pr))
                    self.done[i-d] = False
            yield self
            time.sleep(0.05)
