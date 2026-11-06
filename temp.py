
import time
import os
import board
import adafruit_dht
import requests
from datetime import datetime

# ==========================================
# RASPBERRY PI 4 + DHT11 + THINGSPEAK
# ==========================================

# ThingSpeak configuration
API_KEY = os.getenv("WMM8E130A5NW5CWK")
THINGSPEAK_URL = "https://api.thingspeak.com/update"

if not API_KEY:
    raise SystemExit("ERROR: ThingSpeak API key not configured!")

# GPIO14 = Physical pin 8
dht = adafruit_dht.DHT11(
    board.D14,
    use_pulseio=False
)

# Upload interval: 20 seconds
UPLOAD_INTERVAL = 20
last_upload = 0

print("\n========================================")
print(" RASPBERRY PI 4 - DHT11 THINGSPEAK")
print("========================================")
print("Sensor       : DHT11")
print("GPIO         : GPIO14")
print("Cloud        : ThingSpeak")
print("Field 1      : Temperature")
print("Field 2      : Humidity")
print("Upload rate  : Every 20 seconds")
print("----------------------------------------")
print("Monitoring started...\n")

try:
    while True:

        try:
            # Read sensor
            temperature = dht.temperature
            humidity = dht.humidity

            if temperature is not None and humidity is not None:

                fahrenheit = (temperature * 9 / 5) + 32

                current_time = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                print("----------------------------------------")
                print("Date & Time :", current_time)
                print("Temperature :", temperature, "°C")
                print("Temperature :", round(fahrenheit, 1), "°F")
                print("Humidity    :", humidity, "%")

                if temperature >= 30:
                    print("Alert       : HIGH TEMPERATURE!")
                else:
                    print("Status      : NORMAL")

                # Upload to ThingSpeak every 20 seconds
                if time.monotonic() - last_upload >= UPLOAD_INTERVAL:

                    payload = {
                        "api_key": API_KEY,
                        "field1": temperature,
                        "field2": humidity
                    }

                    try:
                        response = requests.post(
                            THINGSPEAK_URL,
                            data=payload,
                            timeout=10
                        )

                        response.raise_for_status()

                        entry_id = response.text.strip()

                        if entry_id and entry_id != "0":
                            print("ThingSpeak  : UPLOAD SUCCESSFUL")
                            print("Entry ID    :", entry_id)
                        else:
                            print("ThingSpeak  : UPLOAD FAILED")
                            print("Check API key and channel settings")

                    except requests.RequestException as error:
                        print("Cloud Error :", error)

                    last_upload = time.monotonic()

                print("----------------------------------------")

        except RuntimeError as error:
            print("Sensor reading error:", error)
            print("Retrying sensor...")

        time.sleep(2.5)

except KeyboardInterrupt:
    print("\nMonitoring stopped.")

finally:
    dht.exit()
    print("DHT11 sensor disconnected.")
