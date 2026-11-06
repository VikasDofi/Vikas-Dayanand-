
import RPi.GPIO as GPIO
import time
import requests
import threading

# ---------------- GPIO Configuration ----------------

TRIG = 15
ECHO = 14
LED = 27

# ---------------- Detection Configuration ----------------

DETECT_CM = 100
CLEAR_CM = 115

# ---------------- ThingSpeak Configuration ----------------

WRITE_API_KEY = "1WFSA9SXK6MQXOLB"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

UPLOAD_INTERVAL = 16

# ---------------- GPIO Setup ----------------

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

GPIO.output(TRIG, False)
GPIO.output(LED, False)

time.sleep(2)


# ---------------- Measure Distance ----------------

def measure_distance():

    # Send a 10-microsecond trigger pulse
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Wait for ECHO to become HIGH
    start_wait = time.monotonic()

    while GPIO.input(ECHO) == 0:
        if time.monotonic() - start_wait > 0.03:
            return None

    pulse_start = time.monotonic()

    # Wait for ECHO to become LOW
    while GPIO.input(ECHO) == 1:
        if time.monotonic() - pulse_start > 0.03:
            return None

    pulse_end = time.monotonic()

    # Calculate distance in centimetres
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 34300 / 2

    return round(distance, 2)


# ---------------- ThingSpeak Upload ----------------

def upload_to_thingspeak(distance, detected):

    params = {
        "api_key": WRITE_API_KEY,
        "field1": distance,
        "field2": int(detected),
        "field3": int(detected)
    }

    try:
        response = requests.get(
            THINGSPEAK_URL,
            params=params,
            timeout=8
        )

        response.raise_for_status()

        entry_id = response.text.strip()

        if entry_id.isdigit() and int(entry_id) > 0:
            print(
                "\n[ThingSpeak] Upload successful. "
                "Entry ID: {}".format(entry_id)
            )
        else:
            print(
                "\n[ThingSpeak] Upload failed. "
                "Check your Write API Key and channel."
            )

    except requests.RequestException as error:
        print("\n[ThingSpeak] Connection error:", error)


# ---------------- Main Program ----------------

try:
    print("=" * 55)
    print("HOME INTRUSION DETECTION SYSTEM")
    print("Ultrasonic Sensor + LED + ThingSpeak")
    print("=" * 55)

    print("TRIG: GPIO15")
    print("ECHO: GPIO14")
    print("LED : GPIO27")
    print("Detection threshold: {} cm".format(DETECT_CM))
    print("Monitoring started. Press Ctrl+C to stop.\n")

    detected = False

    last_status_time = 0
    last_upload_time = time.monotonic() - UPLOAD_INTERVAL

    upload_thread = None

    while True:

        distance = measure_distance()
        current_time = time.monotonic()

        # Process only valid ultrasonic readings
        valid_reading = (
            distance is not None
            and 2 <= distance <= 400
        )

        if valid_reading:

            # Turn detection ON at 100 cm or closer
            if not detected and distance <= DETECT_CM:
                detected = True
                print(
                    "\n[ALERT] OBJECT DETECTED! "
                    "Distance: {:.2f} cm".format(distance)
                )

            # Clear detection at 115 cm or farther
            elif detected and distance >= CLEAR_CM:
                detected = False
                print(
                    "\n[CLEAR] NO OBJECT NEARBY. "
                    "Distance: {:.2f} cm".format(distance)
                )

            # Control LED
            GPIO.output(
                LED,
                GPIO.HIGH if detected else GPIO.LOW
            )

        # Invalid readings do not immediately change the
        # previous detection state or LED state.
        if current_time - last_status_time >= 1:

            if valid_reading:
                status = (
                    "OBJECT DETECTED"
                    if detected
                    else "NO OBJECT NEARBY"
                )

                print(
                    "Distance: {:.2f} cm | Status: {} | LED: {}".format(
                        distance,
                        status,
                        "ON" if detected else "OFF"
                    )
                )

            else:
                print("[WARNING] Invalid reading or object out of range")

            last_status_time = current_time

        # Upload in a background thread so network requests
        # do not block the sensor monitoring loop.
        if (
            valid_reading
            and current_time - last_upload_time >= UPLOAD_INTERVAL
            and (
                upload_thread is None
                or not upload_thread.is_alive()
            )
        ):

            upload_thread = threading.Thread(
                target=upload_to_thingspeak,
                args=(distance, detected),
                daemon=True
            )

            upload_thread.start()
            last_upload_time = current_time

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nMonitoring stopped by user.")

finally:
    GPIO.output(LED, GPIO.LOW)
    GPIO.cleanup()
    print("GPIO cleanup completed.")
