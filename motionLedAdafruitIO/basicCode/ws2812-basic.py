# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
NeoPixel example for Pico. Turns the NeoPixel red.

REQUIRED HARDWARE:
* RGB NeoPixel LEDs connected to pin GP0.
"""
import board
import neopixel
import time

pixel = neopixel.NeoPixel(board.GP6, 1)
pixel.brightness = 0.1

pixel.fill((0, 255, 0))
time.sleep(3)
pixel.fill((0, 0, 0))
