import zmq
from database import db  # Fixed import - use 'from database import db'
from flask import Flask, jsonify, request
import threading

app = Flask(__name__)

# Initialize database
db.create_tables()

# API endpoints
@app.route('/getMeasures/<int:sensor_id>', methods=['GET'])  
def get_measurements_by_sensor(sensor_id):  # Fixed function name and added parameter
    """Get all measurements by sensor ID"""
    try:
        measurements = db.get_measurements_by_sensor(sensor_id)
        return jsonify({
            'sensor_id': sensor_id,
            'measurements': measurements,
            'count': len(measurements)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sensors', methods=['GET'])
def get_all_sensors():
    """Get all sensors"""
    try:
        sensors = db.get_all_sensors()
        return jsonify({
            'sensors': sensors,
            'count': len(sensors)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/hello', methods=['GET'])
def hello_world():
    return jsonify(message="Hello, World!")

def zmq_server():
    """ZMQ server function"""
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:5000")

    print("Air Quality Server running on port 5000...")
    print("Waiting for sensor data...\n")

    while True:
        try:
            msg = socket.recv_string()
            sensor_id, location, pm25, no2, o3, timestamp = msg.split(",")

            print(
                f"[{timestamp}] {sensor_id} ({location}) → "
                f"PM2.5={pm25}  NO2={no2}  O3={o3}"
            )
            
            # Store data in database
            # Create sensor if it doesn't exist
            existing_sensors = db.get_all_sensors()
            sensor_exists = any(s[0] == int(sensor_id) for s in existing_sensors if s)
            
            if not sensor_exists:
                db.create_sensor(location, "PM2.5")  # You can modify this logic
            
            # Store measurements (you might want to store each pollutant separately)
            db.create_measurement(float(pm25), int(sensor_id), timestamp)

        except KeyboardInterrupt:
            print("Server stopped by user.")
            break
        except Exception as e:
            print(f"Error processing message: {e}")

    socket.close()
    context.term()

def main():
    # Run ZMQ server in a separate thread
    zmq_thread = threading.Thread(target=zmq_server, daemon=True)
    zmq_thread.start()
    
    # Run Flask API server
    print("Starting Flask API on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)



if __name__ == "__main__":
    main()