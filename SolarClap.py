__author__ = 'Pepijn W'

import SongLevel
import Hand

hands = [ Hand.Hand("w","white",27), Hand.Hand("b","blue",22), Hand.Hand("o","orange",23) ]
song = SongLevel.SongLevel("Vivacity", 140)
song.play(hands)