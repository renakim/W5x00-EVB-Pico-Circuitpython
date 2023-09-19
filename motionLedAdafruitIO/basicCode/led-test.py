import time
import random
import board
import neopixel

# Initialize NeoPixel
led = neopixel.NeoPixel(board.GP6, 1)
led.brightness = 0.1


# Basic Scenarios
def led_off():
    led.fill((0, 0, 0))


def led_on():
    led.fill((255, 255, 255))


# Interesting Variations
def gradual_increase():
    for i in range(0, 256, 5):
        led.fill((i, i, i))
        time.sleep(0.1)


def color_change():
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    led.fill(random.choice(colors))


def blink_effect():
    for _ in range(3):
        led.fill((255, 255, 255))
        time.sleep(0.5)
        led.fill((0, 0, 0))
        time.sleep(0.5)


def pulsing_effect():
    for i in range(0, 256, 5):
        led.fill((i, i, i))
        time.sleep(0.1)
    for i in range(255, -1, -5):
        led.fill((i, i, i))
        time.sleep(0.1)


def random_effect():
    led.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))


# Test the functions
led_off()
# time.sleep(1)
# led_on()
# time.sleep(1)
# gradual_increase()
# color_change()
# time.sleep(1)
# blink_effect()
pulsing_effect()
# random_effect()
# time.sleep(1)
time.sleep(3)
led_off()
