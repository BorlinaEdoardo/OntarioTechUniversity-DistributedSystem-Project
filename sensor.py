import zmq, time, random, sys
from datetime import datetime

LOCATIONS = ["Oshawa", "Pickering", "Ajax", "Whitby", "Toronto"]

def sensor_main():
    sensor_id = sys.argv[1] if len(sys.argv) > 1 else "Sensor-1"
    sensor_num = int(sensor_id.replace("Sensor", "")) - 1
    location = LOCATIONS[sensor_num % len(LOCATIONS)]

    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.connect("tcp://localhost:6000")

    print(f"{sensor_id} assigned to {location}")

    while True:
        pm25 = round(random.uniform(5, 55), 2)
        no2  = round(random.uniform(10, 50), 2)
        o3   = round(random.uniform(20, 80), 2)
        ts   = datetime.now().isoformat()

        message = f"{sensor_id},{location},{pm25},{no2},{o3},{ts}"
        socket.send_string(message)
        print("Sent:", message)

        time.sleep(2)

if __name__ == "__main__":
    sensor_main()