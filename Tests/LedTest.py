__author__ = 'Pepijn W'

from neopixel import *
import time

LEDS = 12

PIN = 18
strip = Adafruit_NeoPixel(LEDS, PIN, brightness=100 )
strip.begin()
while True:
    for i in range(LEDS):
        strip.setPixelColor(i, Color(255,0,0))
    strip.show()
    time.sleep(1)

    for i in range(LEDS):
        strip.setPixelColor(i, Color(0,255,0))
    strip.show()
    time.sleep(1)

    for i in range(LEDS):
        strip.setPixelColor(i, Color(0,0,255))
    strip.show()
    time.sleep(1)