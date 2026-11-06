import psutil
from gpiozero import LED

# GPIO setup
leds = {
    "1": LED(16),  # Red
    "2": LED(17),  # Green
    "3": LED(10),  # White
    "4": LED(18)   # Yellow
}

names = {"1": "Red", "2": "Green", "3": "White", "4": "Yellow"}
current_led = None

def all_off():
    for led in leds.values():
        led.off()

try:
    while True:
        # System monitoring
        print("\n--- SYSTEM MONITORING ---")
        print("CPU Usage:", psutil.cpu_percent(interval=1), "%")
        print("CPU Count:", psutil.cpu_count())

        disk = psutil.disk_usage('/')
        print("Disk Usage:", disk.percent, "%")
        print("Disk Used:", round(disk.used / 1024**3, 2), "GB")
        print("Total Disk:", round(disk.total / 1024**3, 2), "GB")

        # LED menu
        print("\n--- LED CONTROL ---")
        print("1. Red  2. Green  3. White  4. Yellow")
        print("5. ALL ON  6. ALL OFF  7. EXIT")

        choice = input("Enter option: ")

        if choice in leds:
            all_off()
            if current_led != choice:
                leds[choice].on()
                current_led = choice
                print(names[choice], "ON")
            else:
                current_led = None
                print(names[choice], "OFF")

        elif choice == "5":
            for led in leds.values():
                led.on()
            current_led = "all"
            print("ALL LEDs ON")

        elif choice == "6":
            all_off()
            current_led = None
            print("ALL LEDs OFF")

        elif choice == "7":
            break

        else:
            print("Invalid option!")

finally:
    all_off()
    for led in leds.values():
        led.close()