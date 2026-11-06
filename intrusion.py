
#!/usr/bin/env python3

from datetime import datetime
from time import sleep, monotonic

from gpiozero import DigitalInputDevice, LED


# ==================================================
# CONFIGURATION
# ==================================================

PIR_GPIO = 17             # Physical pin 11
LED_GPIO = 27             # Physical pin 13

WARMUP_SECONDS = 10
POLL_INTERVAL = 0.05      # Read input every 50 ms
STATUS_INTERVAL = 1.0     # Refresh status every second
DEBOUNCE_SECONDS = 0.15   # Ignore very brief signal fluctuations
IDLE_CONFIRM_SECONDS = 1  # Require LOW before arming


def timestamp():
    return datetime.now().astimezone().strftime(
        "%Y-%m-%d %H:%M:%S %Z"
    )


def main():
    print("=" * 60)
    print("       HOME INTRUSION DETECTION SYSTEM")
    print("=" * 60)
    print(f"[INFO] Started: {timestamp()}")
    print(f"[INFO] PIR: GPIO{PIR_GPIO} (physical pin 11)")
    print(f"[INFO] LED: GPIO{LED_GPIO} (physical pin 13)")
    print(f"[INFO] Warm-up: {WARMUP_SECONDS} seconds")

    try:
        with DigitalInputDevice(
            PIR_GPIO, pull_up=False
        ) as pir, LED(
            LED_GPIO, initial_value=False
        ) as led:

            led.off()

            # ------------------------------------------
            # 1. SENSOR WARM-UP
            # ------------------------------------------
            for remaining in range(WARMUP_SECONDS, 0, -1):
                print(
                    f"\r[WARM-UP] {remaining:02d} seconds remaining",
                    end="   ",
                    flush=True,
                )
                sleep(1)

            print("\n[INFO] Warm-up completed.")
            print("[INFO] Waiting for sensor output to return LOW.")

            # ------------------------------------------
            # 2. WAIT FOR AN IDLE SENSOR BEFORE ARMING
            # ------------------------------------------
            # Prevents a HIGH signal at startup from being
            # immediately reported as a new intrusion.
            low_since = None
            last_wait_update = 0.0

            while True:
                now = monotonic()

                if not pir.value:
                    if low_since is None:
                        low_since = now

                    if now - low_since >= IDLE_CONFIRM_SECONDS:
                        break
                else:
                    low_since = None

                led.off()

                if now - last_wait_update >= STATUS_INTERVAL:
                    print(
                        "\r[WAIT] PIR output HIGH; waiting for idle. "
                        "Check sensor settings if the area is empty.",
                        end="   ",
                        flush=True,
                    )
                    last_wait_update = now

                sleep(POLL_INTERVAL)

            # ------------------------------------------
            # 3. CONTINUOUS MONITORING
            # ------------------------------------------
            print("\n[ARMED] Monitoring for movement.")
            print("[INFO] Press Ctrl+C to stop.")

            motion_state = False
            candidate_state = False
            candidate_since = monotonic()
            last_status_update = 0.0

            while True:
                now = monotonic()
                raw_motion = bool(pir.value)

                # Filter brief electrical fluctuations.
                if raw_motion == motion_state:
                    candidate_state = motion_state
                    candidate_since = now

                else:
                    if raw_motion != candidate_state:
                        candidate_state = raw_motion
                        candidate_since = now

                    elif now - candidate_since >= DEBOUNCE_SECONDS:
                        motion_state = candidate_state

                        if motion_state:
                            led.on()
                            print(
                                f"\n\n[ALERT] MOTION DETECTED! "
                                f"| {timestamp()}"
                            )
                            print("[LED] ON")

                        else:
                            led.off()
                            print(
                                f"\n\n[SAFE] NO MOTION DETECTED "
                                f"| {timestamp()}"
                            )
                            print("[LED] OFF")

                        last_status_update = 0.0

                # Show current state continuously.
                if now - last_status_update >= STATUS_INTERVAL:
                    if motion_state:
                        status = (
                            f"[GPIO{PIR_GPIO}=1] "
                            f"MOTION DETECTED | {timestamp()}"
                        )
                    else:
                        status = (
                            f"[GPIO{PIR_GPIO}=0] "
                            f"NO MOTION DETECTED | {timestamp()}"
                        )

                    print(
                        f"\r{status:<90}",
                        end="",
                        flush=True,
                    )
                    last_status_update = now

                sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\n\n[STOPPED] Monitoring stopped.")

    except Exception as error:
        print(f"\n[ERROR] {type(error).__name__}: {error}")

    finally:
        print("[INFO] Program terminated.")


if __name__ == "__main__":
    main()
