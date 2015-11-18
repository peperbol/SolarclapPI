__author__ = 'Pepijn W'

import SongLevel
import Hand
from neopixel import Color

hands = [
    #Hand.Hand(Color(168,255 ,0)        ,"lime"           ,17),
    Hand.Hand(Color(128,0,255)         ,"violet"         ,27),
    #Hand.Hand(Color(255,168,168)       ,"salmon pink"    ,22),
    Hand.Hand(Color(0,255,0)           ,"green"          ,23),
    #Hand.Hand(Color(255,0,0)           ,"red"            ,24),
    Hand.Hand(Color(255,128,0)         ,"orange"         ,25),
    #Hand.Hand(Color(0,168,255)         ,"light blue"     ,4),
    Hand.Hand(Color(255,0,168)         ,"barbie pink"   ,7)
]
song = SongLevel.SongLevel("Vivacity", 140)
song.play(hands)