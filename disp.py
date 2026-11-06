import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD
import time

lcd = CharLCD(
    numbering_mode=GPIO.BCM,
    cols=16,
    rows=2,
    pin_rs=5,
    pin_e=6,
    pins_data=[12, 13, 16, 26],
    pin_rw=None
)

lcd.write_string("Hello World!")
lcd.cursor_pos = (1, 0)
lcd.write_string("Raspberry Pi 4")

time.sleep(10)
lcd.clear()
lcd.close()
GPIO.cleanup()
