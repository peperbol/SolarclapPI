__author__ = 'Pepijn W'

import pygame
import GpioInput
ssm = False
class SongSelectMenu:
    def __init__(self, songs, inputThread):
        global ssm
        ssm = self

        pygame.mixer.init()

        self.songs = songs
        self.selectIndex = 0
        self.Action = False
        self.gameRunning = True
        inputThread.start()
        self.activate()
        self.waitForAction()

    def activate(self):

        def next():
            self.setIndex(self.selectIndex +1)
            self.playsound()
        def setnext(b1,b2):
            self.Action = next

        def setplaysong(b1,b2):
            self.Action = self.songs[self.selectIndex].play
        GpioInput.buttoncallback = GpioInput.ButtonCallback( setplaysong ,setnext)
        self.playsound()


    def playsound(self):
        pygame.mixer.music.load(self.songs[self.selectIndex].spokenname)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()
    def waitForAction(self):
        while self.gameRunning:
            if self.Action:
                self.Action()
                self.Action = False


    def setIndex(self, i):
        self.selectIndex = i%len(self.songs)