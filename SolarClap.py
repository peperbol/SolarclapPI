__author__ = 'Pepijn W'

import SongLevel
import Hand
from neopixel import Color

hands = [ Hand.Hand(Color(168,168,254),"white",27), Hand.Hand(Color(0,0,255),"blue",22), Hand.Hand(Color(255, 64, 0),"orange",23) ]
song = SongLevel.SongLevel("Vivacity", 140)
song.play(hands)