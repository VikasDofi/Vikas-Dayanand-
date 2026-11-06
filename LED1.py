from gpiozero import LED
from time import sleep

red = LED(18)
yellow = LED(17)
green = LED(16)

leds = [red, amber, green]

while True:
    for led in leds:
        led.on()
        sleep(0.5)
        led.off()

    for led in leds[-2::-1]:
        led.on()
        sleep(0.5)
        led.off()