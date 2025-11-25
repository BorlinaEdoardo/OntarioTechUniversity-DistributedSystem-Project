# Air Quality Monitoring Server

This is the server component of the distributed air quality monitoring system. It handles sensor data collection via ZeroMQ and provides REST API endpoints for data access.

## Architecture

The server consists of two main components:
- **ZMQ Server**: Receives sensor data on port 5000
- **Flask API**: Provides HTTP endpoints on port 5000

Both run concurrently using Python threading.

## Dependencies

Install required packages:
```bash
pip install -r requirements.txt
```

Required packages:
- `flask>=2.0.0` - Web framework for REST API
- `pyzmq>=24.0.0` - ZeroMQ Python bindings for sensor communication

Note: `sqlite3` is included with Python by default.

## Database Schema

The system uses SQLite database with two tables:

### SENSOR Table
```sql
CREATE TABLE SENSOR(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    City TEXT NOT NULL,
    Pollutant TEXT NOT NULL
)
```

### MEASUREMENT Table
```sql
CREATE TABLE MEASUREMENT(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Measure REAL NOT NULL,
    Timestamp DATETIME NOT NULL,
    Sensor_id INTEGER,
    FOREIGN KEY (Sensor_id) REFERENCES SENSOR(Id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
)
```

## Project Structure

```
Server/
├── server.py          # Main server application
├── readme.md          # This documentation
└── database/
    ├── db.py           # Database operations and CRUD functions
    └── sensors.db      # SQLite database (created automatically)
```

## API Endpoints

### 1. Get All Sensors
- **URL**: `GET /sensors`
- **Description**: Retrieve all registered sensors
- **Response**:
```json
{
    "sensors": [
        [1, "Toronto", "PM2.5"],
        [2, "Vancouver", "NO2"]
    ],
    "count": 2
}
```

### 2. Get Measurements by Sensor
- **URL**: `GET /getMeasures/<sensor_id>`
- **Description**: Retrieve all measurements for a specific sensor
- **Parameters**: 
  - `sensor_id` (integer): The ID of the sensor
- **Response**:
```json
{
    "sensor_id": 1,
    "measurements": [
        [1, 25.3, "2023-11-13 10:30:00", 1],
        [2, 28.7, "2023-11-13 10:35:00", 1]
    ],
    "count": 2
}
```

### 3. Health Check
- **URL**: `GET /hello`
- **Description**: Simple health check endpoint
- **Response**:
```json
{
    "message": "Hello, World!"
}
```

## Database Operations

The `database/db.py` module provides complete CRUD operations:

### Sensor Operations
- `create_sensor(city, pollutant)` - Create new sensor
- `get_sensor_by_id(sensor_id)` - Get sensor by ID
- `get_all_sensors()` - Get all sensors
- `update_sensor(sensor_id, city, pollutant)` - Update sensor
- `delete_sensor(sensor_id)` - Delete sensor

### Measurement Operations
- `create_measurement(measure, sensor_id, timestamp=None)` - Create measurement
- `get_measurement_by_id(measurement_id)` - Get measurement by ID
- `get_measurements_by_sensor(sensor_id)` - Get all measurements for sensor
- `get_all_measurements()` - Get all measurements
- `update_measurement(measurement_id, measure, timestamp=None)` - Update measurement
- `delete_measurement(measurement_id)` - Delete measurement

### Helper Functions
- `get_sensor_with_measurements(sensor_id)` - Get sensor with all its measurements
- `create_tables()` - Initialize database tables

## ZMQ Message Format

The server expects sensor data in CSV format:
```
sensor_id,location,pm25,no2,o3,timestamp
```

Example:
```
1,Toronto,25.3,42.1,35.8,2023-11-13 10:30:00
```

## Running the Server

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the server**:
```bash
cd Server
python server.py
```

3. **Server endpoints will be available at**:
- ZMQ Server: `tcp://localhost:5000` (for sensor data)
- REST API: `http://localhost:5000` (for HTTP requests)

## Key Features

- **Concurrent Processing**: ZMQ and HTTP servers run simultaneously
- **Automatic Threading**: Flask handles multiple HTTP connections automatically
- **Database Integration**: Automatic sensor registration and measurement storage
- **Error Handling**: Comprehensive exception handling for all operations
- **Cross-platform**: Uses `os.path.join()` for database path compatibility

## Modifications Made

1. **Fixed Import Issues**: Corrected database import path
2. **Enhanced SQL Schema**: Added proper foreign key constraints
3. **Complete CRUD Operations**: Implemented all database operations with parameterized queries
4. **Concurrent Server Architecture**: ZMQ and Flask servers run simultaneously using threading
5. **API Route Fixes**: Corrected Flask route syntax and parameter handling
6. **Error Handling**: Added comprehensive exception handling
7. **Database Auto-initialization**: Tables created automatically on startup
8. **Virtual Environment Support**: Compatible with Python virtual environments

## Testing the API

### Using curl:
```bash
# Get all sensors
curl http://localhost:5000/sensors

# Get measurements for sensor ID 1
curl http://localhost:5000/getMeasures/1

# Health check
curl http://localhost:5000/hello
```

### Using browser:
- Visit: `http://localhost:5000/hello`
- Visit: `http://localhost:5000/sensors`
- Visit: `http://localhost:5000/getMeasures/1`

## Troubleshooting

### Common Issues:

1. **ModuleNotFoundError: No module named 'zmq'**
   - Install in virtual environment: `pip install pyzmq`

2. **Database path issues**
   - Database uses relative path with `os.path.join()` for cross-platform compatibility

3. **Port conflicts**
   - ZMQ: port 5000
   - Flask: port 5000
   - Ensure ports are available

4. **Virtual Environment Issues**
   - Make sure to install packages in the correct virtual environment
   - Use: `C:/Users/edoar/.virtualenvs/edoar-L_NQZpTx/Scripts/pip install pyzmq flask`
