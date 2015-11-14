__author__ = 'Pepijn W'

from neopixel import *


PIN = 18
strip = Adafruit_NeoPixel(8, PIN, brightness=15 )
strip.begin()

strip.setPixelColor(0, Color(168,255 ,0))#lime
strip.setPixelColor(1, Color(128,0,255))#violet
strip.setPixelColor(2, Color(255,168,168))#salmon
strip.setPixelColor(3, Color(0,255,0))#green
strip.setPixelColor(4, Color(255,0,0))#red
strip.setPixelColor(5, Color(255,128,0))#orange
strip.setPixelColor(6, Color(0,168,255))#light blue
strip.setPixelColor(7, Color(255,0,168))#barbie pink
strip.show()