import subprocess
import time
import sys
import os

NUM_SENSORS = 5  # change this to spawn more sensors

def main():
    for i in range(1, NUM_SENSORS + 1):
        sensor_id = f"Sensor{i}"
        print(f"Starting {sensor_id}...")

        # On Windows: opens each sensor in a new console window
        creationflags = 0
        if os.name == "nt":  # nt = Windows
            creationflags = subprocess.CREATE_NEW_CONSOLE

        subprocess.Popen(
            [sys.executable, "sensor.py", sensor_id],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

        time.sleep(0.3)  # small delay so windows open cleanly

if __name__ == "__main__":
    main()