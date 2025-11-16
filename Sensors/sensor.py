import zmq
import time
import random
import sys
from datetime import datetime

LOCATIONS = ["Oshawa", "Pickering", "Ajax", "Whitby", "Toronto"]

def sensor_main():
    # Sensor ID is passed in (e.g., "Sensor1"); default if not given.
    sensor_id = sys.argv[1] if len(sys.argv) > 1 else "Sensor1"

    # Extract numeric part: "Sensor1" -> 1 -> index 0
    try:
        sensor_num = int(sensor_id.replace("Sensor", "")) - 1
    except ValueError:
        sensor_num = 0  # fallback

    location = LOCATIONS[sensor_num % len(LOCATIONS)]

    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.connect("tcp://localhost:6000")

    print(f"{sensor_id} assigned to {location}")

    try:
        while True:
            pm25 = round(random.uniform(5, 55), 2)
            no2  = round(random.uniform(10, 50), 2)
            o3   = round(random.uniform(20, 80), 2)
            ts   = datetime.now().isoformat()

            message = f"{sensor_id},{location},{pm25},{no2},{o3},{ts}"
            socket.send_string(message)
            print("Sent:", message)

            time.sleep(2)
    except KeyboardInterrupt:
        print(f"\n{sensor_id} stopped by user.")

if __name__ == "__main__":
    sensor_main()