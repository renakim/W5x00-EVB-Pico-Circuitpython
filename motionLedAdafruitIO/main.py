import board
import busio
import digitalio
import time
import neopixel
import adafruit_requests as requests
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket

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


# Ethernet
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


# Adafruit.io
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


# LED functions
def led_on():
    led.fill((255, 255, 255))


def led_off():
    led.fill((0, 0, 0))


def pulsing_effect_on():
    for i in range(0, 256, 5):
        led.fill((i, i, i))
        time.sleep(0.1)


def pulsing_effect_off():
    for i in range(255, -1, -5):
        led.fill((i, i, i))
        time.sleep(0.1)


def main():
    init_ethernet()

    feed_name = "w5500-evb-pico-motion"
    # create_feed(feed_name)
    # time.sleep(1)

    old_value = pir.value
    while True:
        pir_value = pir.value
        if pir_value:
            if not old_value:
                print('Motion detected!')
                led.brightness = 0.5
                pulsing_effect_on()
                create_data(feed_name, {"value": 1})
        else:
            if old_value:
                print('Motion ended!')
                pulsing_effect_off()
        old_value = pir_value


main()
