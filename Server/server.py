import zmq
from database import db  # requires project_root/database/__init__.py
from flask import Flask, jsonify
import threading
from datetime import datetime

app = Flask(__name__, static_folder='static')

# Initialize database
db.create_tables()

# ---------- Flask API endpoints ----------

# Allow CORS for all routes
@app.after_request
def add_cors_headers(response):
    """Allow browser dashboard to connect"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    return response

# MAIN DASHBOARD (NEW)
@app.route('/')
def index():
    return app.send_static_file("index.html")

@app.route('/getMeasures/sensor/<int:sensor_id>', methods=['GET'])
def get_measurements_by_sensor(sensor_id):
    """Get all measurements by sensor ID."""
    try:
        measurements = db.get_measurements_by_sensor(sensor_id)
        return jsonify({
            "sensor_id": sensor_id,
            "measurements": measurements,
            "count": len(measurements)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/getMeasures/city/<string:city>', methods=['GET'])
def get_measurements_by_city(city):
    """Get all measurements by city."""
    try:
        measurements = db.get_measurements_by_city(city)
        return jsonify({
            "city": city,
            "measurements": measurements,
            "count": len(measurements)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/sensors', methods=['GET'])
def get_all_sensors():
    """Get all sensors."""
    try:
        sensors = db.get_all_sensors()
        return jsonify({
            "sensors": sensors,
            "count": len(sensors)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/hello', methods=['GET'])
def hello_world():
    return jsonify(message="Hello, World!")

# ---------- ZMQ Server ----------

def zmq_server():
    """ZMQ server function that receives sensor data and stores it."""
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:6000")

    print("Air Quality Server running on port 6000...")
    print("Waiting for sensor data...\n")

    while True:
        try:
            msg = socket.recv_string()
            sensor_id_str, location, pm25, no2, o3, timestamp = msg.split(",")

            # "Sensor1" -> 1
            try:
                sid = int(sensor_id_str.replace("Sensor", ""))
            except ValueError:
                print(f"Invalid sensor_id format: {sensor_id_str}")
                continue

            print(
                f"[{timestamp}] {sensor_id_str} ({location}) → "
                f"PM2.5={pm25}  NO2={no2}  O3={o3}"
            )
            
            # Ensure sensor exists (by numeric ID)
            sensor = db.get_sensor_by_id(sid)
            if not sensor:
                print(f"Registering new sensor ID={sid}, City={location}")
                db.create_sensor(location)

            # Store measurements correctly
            db.create_measurement(float(pm25), "PM2.5", sid, timestamp)
            db.create_measurement(float(no2),  "NO2",   sid, timestamp)
            db.create_measurement(float(o3),   "O3",    sid, timestamp)

        except KeyboardInterrupt:
            print("\nServer stopped by user.")
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
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=False
    )

if __name__ == "__main__":
    main()