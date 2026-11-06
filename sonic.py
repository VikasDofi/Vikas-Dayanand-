
from gpiozero import DistanceSensor, LED
from time import sleep

# ---------------- CONFIGURATION ----------------

TRIG_PIN = 15
ECHO_PIN = 14
LED_PIN = 27

DETECTION_DISTANCE_CM = 100  # Detect objects within 100 cm

# ------------------------------------------------

# Initialize ultrasonic sensor
sensor = DistanceSensor(
    echo=ECHO_PIN,
    trigger=TRIG_PIN,
    max_distance=2.0,
    queue_len=5
)

# Initialize LED
led = LED(LED_PIN)

print("====================================")
print(" HC-SR04 ULTRASONIC DETECTION SYSTEM ")
print("====================================")
print("System started.")
print(f"Detection range: {DETECTION_DISTANCE_CM} cm")
print("Press CTRL+C to stop.\n")

try:
    while True:

        # Measure distance in meters and convert to centimeters
        distance_cm = sensor.distance * 100

        # Display measured distance
        print(f"Distance: {distance_cm:.2f} cm")

        # Detect an object within the configured range
        if distance_cm <= DETECTION_DISTANCE_CM:
            led.on()
            print("OBJECT DETECTED - LED ON\n")

        else:
            led.off()
            print("NO OBJECT IN RANGE - LED OFF\n")

        sleep(0.2)

except KeyboardInterrupt:
    print("\nProgram stopped by user.")

finally:
    led.off()
    sensor.close()
    led.close()
    print("LED turned OFF. Resources released.")