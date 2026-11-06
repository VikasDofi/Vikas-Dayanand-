
from gpiozero import LED, Button
from time import sleep, time

red = LED(17)
yellow = LED(27)
green = LED(6)
button = Button(23, pull_up=True, bounce_time=0.2)

while True:
    button.wait_for_press()

    start = time()

    while time() - start < 10:
        red.on()
        yellow.off()
        green.off()
        sleep(1)

        if time() - start >= 10:
            break

        red.off()
        yellow.on()
        sleep(1)

        if time() - start >= 10:
            break

        yellow.off()
        green.on()
        sleep(1)

    red.off()
    yellow.off()
    green.off()

    button.wait_for_release()
