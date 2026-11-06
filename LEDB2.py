
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

# State: 0=OFF, 1=RED, 2=YELLOW, 3=GREEN
state = 0

def update_leds(state):
    GPIO.output(RED, state == 1)
    GPIO.output(YELLOW, state == 2)
    GPIO.output(GREEN, state == 3)

update_leds(state)

try:
    while True:
        if GPIO.input(BUTTON) == GPIO.LOW:
            time.sleep(0.05)  # Debounce

            if GPIO.input(BUTTON) == GPIO.LOW:
                state = (state + 1) % 4
                update_leds(state)

                print("State:", ["OFF", "RED", "YELLOW", "GREEN"][state])

                # Wait until button is released
                while GPIO.input(BUTTON) == GPIO.LOW:
                    time.sleep(0.02)

        time.sleep(0.01)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()

