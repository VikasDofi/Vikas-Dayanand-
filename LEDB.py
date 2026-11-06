
import RPi.GPIO as GPIO
import time

RED = 17
YELLOW = 27
GREEN = 6
BUTTON = 23

GPIO.setmode(GPIO.BCM)

GPIO.setup(RED, GPIO.OUT)
GPIO.setup(YELLOW, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)

GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

leds_on = False

try:
    while True:
        if GPIO.input(BUTTON) == GPIO.LOW:
            time.sleep(0.05)  # Debounce

            if GPIO.input(BUTTON) == GPIO.LOW:
                leds_on = not leds_on

                GPIO.output(RED, leds_on)
                GPIO.output(YELLOW, leds_on)
                GPIO.output(GREEN, leds_on)

                # Wait for button release
                while GPIO.input(BUTTON) == GPIO.LOW:
                    time.sleep(0.05)

        time.sleep(0.01)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
