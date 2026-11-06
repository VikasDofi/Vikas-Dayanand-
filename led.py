from gpiozero import LED

led = LED(15)  # GPIO 18

while True:
    command = input("Type on or off: ").lower()

    if command == "off":
        led.on()
        print("Light OFF")

    elif command == "on":
        led.off()
        print("Light ON")

    elif command == "exit":
        led.off()
        break

    else:
        print("Invalid command! Type on, off, or exit.")