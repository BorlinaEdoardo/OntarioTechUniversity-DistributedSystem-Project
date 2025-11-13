import zmq

def main():
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:6000")

    print("Air Quality Server running on port 6000...")
    print("Waiting for sensor data...\n")

    while True:
        try:
            msg = socket.recv_string()
            sensor_id, location, pm25, no2, o3, timestamp = msg.split(",")

            print(
                f"[{timestamp}] {sensor_id} ({location}) → "
                f"PM2.5={pm25}  NO2={no2}  O3={o3}"
            )

        except KeyboardInterrupt:
            print("Server stopped by user.")
            break

    socket.close()
    context.term()

if __name__ == "__main__":
    main()