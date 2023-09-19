import board
import busio
import digitalio
import time
import random
import adafruit_requests as requests
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket
import neopixel

# PIR sensor
PIR_PIN = board.GP22
pir = digitalio.DigitalInOut(PIR_PIN)
pir.direction = digitalio.Direction.INPUT

# WS2812 LED
LED_PIN = board.GP6
led = neopixel.NeoPixel(LED_PIN, 1)
led.brightness = 0.1

# Get Adafruit.io details from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("secrets are kept in secrets.py, please add them there!")
    raise


def init_ethernet():
    MAC_ADDR = (0x00, 0x08, 0xdc, 0x03, 0x04, 0x05)
    cs = digitalio.DigitalInOut(board.GP17)
    eth_rst = digitalio.DigitalInOut(board.GP20)
    eth_rst.direction = digitalio.Direction.OUTPUT
    # SCK, MOSI, MISO
    spi_bus = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)
    print("Hard Resetting")
    # Initialize ethernet interface with DHCP
    eth = WIZNET5K(spi_bus, cs, reset=eth_rst, mac=MAC_ADDR)
    # Initialize a requests object with a socket and ethernet interface
    requests.set_socket(socket, eth)

    print("Chip Version:", eth.chip)
    print("MAC Address:", [hex(i) for i in eth.mac_address])
    print("IP address:", eth.pretty_ip(eth.ip_address))


def create_feed(name):
    data = {
        "feed": {"name": name}
    }
    endpoint = f'http://io.adafruit.com/api/v2/{secrets["aio_username"]}/feeds'
    headers = {"X-AIO-KEY": secrets["aio_key"]}
    response = requests.post(endpoint, json=data, headers=headers)
    print(response.json())
    response.close()


def update_feed(feed_key, data):
    endpoint = f'http://io.adafruit.com/api/v2/{secrets["aio_username"]}/feeds/{feed_key}'
    headers = {"X-AIO-KEY": secrets["aio_key"]}
    response = requests.put(endpoint, json=data, headers=headers)
    print(response.json())
    response.close()


def create_data(feed_name, data):
    endpoint = f'http://io.adafruit.com/api/v2/{secrets["aio_username"]}/feeds/{feed_name}/data'
    headers = {"X-AIO-KEY": secrets["aio_key"]}
    response = requests.post(endpoint, json=data, headers=headers)
    print(response.json())
    response.close()


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


def main():
    init_ethernet()

    feed_name = "w5100s-evb-pico"
    # create_feed(feed_name)
    # time.sleep(1)

    old_value = pir.value
    while True:
        pir_value = pir.value
        if pir_value:
            if not old_value:
                print('Motion detected!')
                create_data(feed_name, {"value": "Motion detected!", "lat": 23.1, "lon": -72.3})
        else:
            if old_value:
                print('Motion ended!')
        old_value = pir_value

    # data = {"value": 27, "humidity": 50, "lat": 23.1, "lon": -72.3}
    # data = {
    #     "feed": {"value": 27, "humidity": 50, "lat": 23.1, "lon": -72.3}
    # }
    # update_feed(feed_name, data)
    # create_data(feed_name, data)

    # print('Done.')


main()
