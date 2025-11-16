import zmq
import time
import random
import sys
import math
from datetime import datetime

# City-specific pollution baselines (realistic)
CITY_BASELINES = {
    "Oshawa":   {"pm25": 12, "no2": 20, "o3": 30},
    "Pickering": {"pm25": 18, "no2": 32, "o3": 40},
    "Ajax":      {"pm25": 15, "no2": 25, "o3": 35},
    "Whitby":    {"pm25": 10, "no2": 18, "o3": 25},
    "Toronto":   {"pm25": 30, "no2": 45, "o3": 50},
}

LOCATIONS = list(CITY_BASELINES.keys())

def realistic_value(baseline, time_factor, drift, noise):
    """Combine components to simulate real sensor behavior."""
    return max(
        0,
        baseline
        + time_factor  # daily cycle influence
        + drift         # slow overall drift
        + noise         # random jitter
    )

def sensor_main():
    # Determine sensor ID (e.g., "Sensor1")
    sensor_id = sys.argv[1] if len(sys.argv) > 1 else "Sensor1"

    # Extract numeric portion to determine location index
    try:
        sensor_num = int(sensor_id.replace("Sensor", "")) - 1
    except ValueError:
        sensor_num = 0

    location = LOCATIONS[sensor_num % len(LOCATIONS)]
    base = CITY_BASELINES[location]

    # ZMQ setup
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.connect("tcp://localhost:6000")

    print(f"{sensor_id} assigned to {location}")

    drift_value = 0  # persistent slow drift over time

    try:
        while True:
            hour = datetime.now().hour

            # Daily patterns (sinusoidal cycles)
            time_factor_pm  = 6  * math.sin((hour / 24) * math.pi * 2)
            time_factor_no2 = 10 * math.sin(((hour - 8) / 24) * math.pi * 4)
            time_factor_o3  = 15 * math.sin(((hour - 12) / 24) * math.pi * 2)

            # Slow drift accumulates
            drift_value += random.uniform(-0.02, 0.02)

            # Noise/jitter
            noise = random.uniform(-2, 2)

            # Generate final values
            pm25 = round(realistic_value(base["pm25"], time_factor_pm, drift_value, noise), 2)
            no2  = round(realistic_value(base["no2"],  time_factor_no2, drift_value, noise), 2)
            o3   = round(realistic_value(base["o3"],   time_factor_o3, drift_value, noise), 2)

            ts = datetime.now().isoformat()

            message = f"{sensor_id},{location},{pm25},{no2},{o3},{ts}"
            socket.send_string(message)

            print(f"Sent: {message}")

            time.sleep(2)  # send every 2 seconds

    except KeyboardInterrupt:
        print(f"\n{sensor_id} stopped manually.")

    finally:
        socket.close()
        context.term()

if __name__ == "__main__":
    sensor_main()