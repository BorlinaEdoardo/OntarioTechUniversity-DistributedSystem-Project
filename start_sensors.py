import subprocess
import time

NUM_SENSORS = 5  # change this to spawn more sensors

for i in range(1, NUM_SENSORS + 1):
    sensor_id = f"Sensor{i}"

    print(f"Starting {sensor_id}...")

    subprocess.Popen(
        ["python", "sensor.py", sensor_id],
        creationflags=subprocess.CREATE_NEW_CONSOLE  # opens new terminal
    )

    time.sleep(0.3)  # small delay so windows open cleanly