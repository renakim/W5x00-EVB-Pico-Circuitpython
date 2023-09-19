import board
import digitalio

PIR_PIN = board.GP17   # Pin number connected to PIR sensor output wire.

# Setup digital input for PIR sensor:
pir = digitalio.DigitalInOut(PIR_PIN)
pir.direction = digitalio.Direction.INPUT
print('Check')

# Main loop that will run forever:
old_value = pir.value
while True:
    pir_value = pir.value
    if pir_value:
        if not old_value:
            print('Motion detected!')
    else:
        if old_value:
            print('Motion ended!')
    old_value = pir_value