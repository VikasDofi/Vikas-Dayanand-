
from gpiozero import LED
from time import sleep

# North: Red, Yellow, Green
NR, NY, NG = LED(17), LED(27), LED(22)

# South
SR, SY, SG = LED(10), LED(9), LED(11)

# East
ER, EY, EG = LED(5), LED(15), LED(13)

# West
WR, WY, WG = LED(19), LED(7), LED(21)

roads = [
    (NR, NY, NG),
    (SR, SY, SG),
    (ER, EY, EG),
    (WR, WY, WG)
]

def all_red():
    for red, yellow, green in roads:
        red.on()
        yellow.off()
        green.off()

try:
    while True:
        for current in roads:
            # All roads red
            all_red()
            sleep(1)

            # Current road green, others red
            red, yellow, green = current
            red.off()
            green.on()
            sleep(5)

            # Current road yellow for 2 seconds
            green.off()
            yellow.on()
            sleep(2)

            # Current road red again
            yellow.off()
            red.on()

except KeyboardInterrupt:
    pass

finally:
    for red, yellow, green in roads:
        red.off()
        yellow.off()
        green.off()
