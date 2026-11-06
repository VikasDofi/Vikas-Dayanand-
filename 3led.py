import psutil
from gpiozero import LED

# GPIO connections
r = LED(16)
g = LED(17)
w = LED(10)
y = LED(18)

current_led = None

# Turn OFF all LEDs
def all_off():
    r.off()
    g.off()
    w.off()
    y.off()

# LED selection
leds = {
    "1": r,
    "2": g,
    "3": w,
    "4": y
}

names = {
    "1": "Red",
    "2": "Green",
    "3": "White",
    "4": "Yellow"
}

try:
    while True:

        # PSUtil monitoring
        print("\n------ PROCESSOR MONITORING ------")
        print("CPU Usage:", psutil.cpu_percent(interval=1), "%")
        print("CPU Count:", psutil.cpu_count())

        print("\n------ LED CONTROL ------")
        print("1. Red")
        print("2. Green")
        print("3. White")
        print("4. Yellow")
        print("5. ALL LEDs ON")
        print("6. ALL LEDs OFF")
        print("7. EXIT")

        choice = input("\nEnter your option: ")

        if choice in leds:

            if current_led == choice:
                all_off()
                current_led = None
                print(names[choice], "LED OFF")

            else:
                all_off()
                leds[choice].on()
                current_led = choice
                print(names[choice], "LED ON")

        elif choice == "5":
            all_off()
            r.on()
            g.on()
            w.on()
            y.on()
            current_led = "all"
            print("ALL FOUR LEDs ON")

        elif choice == "6":
            all_off()
            current_led = None
            print("ALL LEDs OFF")

        elif choice == "7":
            all_off()
            print("Program stopped")
            break

        else:
            print("Invalid option!")

finally:
    all_off()
    r.close()
    g.close()
    w.close()
    y.close()