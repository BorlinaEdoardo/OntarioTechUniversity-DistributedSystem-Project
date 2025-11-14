from datetime import datetime
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "sensors.db")

connection = sqlite3.connect(DB_PATH)

cursor = connection.cursor()

def get_connection():
    """Get a database connection"""
    return sqlite3.connect(DB_PATH)

def create_tables():
    """Create the database tables"""
    connection = get_connection()
    cursor = connection.cursor()
    
    # Create table Sensor
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SENSOR(
                   Id INTEGER PRIMARY KEY AUTOINCREMENT,
                   City TEXT NOT NULL
                   )
     """)
    
    # Create table Measurement
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS MEASUREMENT(
                   Id INTEGER PRIMARY KEY AUTOINCREMENT,
                   Measure REAL NOT NULL,
                   Timestamp DATETIME NOT NULL,
                   Pollutant TEXT NOT NULL,
                   Sensor_id INTEGER,
                   FOREIGN KEY (Sensor_id) REFERENCES SENSOR(Id)
                   ON UPDATE CASCADE
                   ON DELETE CASCADE
                   )
     """)
    
    connection.commit()
    connection.close()
# SENSOR CRUD Operations
def create_sensor(city):
    """Create a new sensor"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO SENSOR (City) VALUES (?)", (city))
    sensor_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return sensor_id

def get_sensor_by_id(sensor_id):
    """Get a sensor by ID"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM SENSOR WHERE Id = ?", (sensor_id,))
    sensor = cursor.fetchone()
    connection.close()
    return sensor

def get_all_sensors():
    """Get all sensors"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM SENSOR")
    sensors = cursor.fetchall()
    connection.close()
    return sensors

def update_sensor(sensor_id, city):
    """Update a sensor"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE SENSOR SET City = ? WHERE Id = ?", 
                   (city, sensor_id))
    rows_affected = cursor.rowcount
    connection.commit()
    connection.close()
    return rows_affected

def delete_sensor(sensor_id):
    """Delete a sensor"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM SENSOR WHERE Id = ?", (sensor_id,))
    rows_affected = cursor.rowcount
    connection.commit()
    connection.close()
    return rows_affected

# MEASUREMENT CRUD Operations
def create_measurement(measure, pollutant, sensor_id, timestamp=None):
    """Create a new measurement"""
    if timestamp is None:
        timestamp = datetime.now()
    
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO MEASUREMENT (Pollutant, Measure, Timestamp, Sensor_id) VALUES (?,?, ?, ?)", 
                   (measure, pollutant, timestamp, sensor_id))
    measurement_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return measurement_id

def get_measurement_by_id(measurement_id):
    """Get a measurement by ID"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM MEASUREMENT WHERE Id = ?", (measurement_id,))
    measurement = cursor.fetchone()
    connection.close()
    return measurement

def get_measurements_by_sensor(sensor_id):
    """Get all measurements for a specific sensor"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM MEASUREMENT WHERE Sensor_id = ?", (sensor_id,))
    measurements = cursor.fetchall()
    connection.close()
    return measurements

def get_all_measurements():
    """Get all measurements"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM MEASUREMENT")
    measurements = cursor.fetchall()
    connection.close()
    return measurements

def update_measurement(measurement_id, measure, pollutant, timestamp=None):
    """Update a measurement"""
    if timestamp is None:
        timestamp = datetime.now()
    
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE MEASUREMENT SET Measure = ?, Timestamp = ?, Pollutant=?  WHERE Id = ?", 
                   (measure, timestamp, measurement_id))
    rows_affected = cursor.rowcount
    connection.commit()
    connection.close()
    return rows_affected

def delete_measurement(measurement_id):
    """Delete a measurement"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM MEASUREMENT WHERE Id = ?", (measurement_id,))
    rows_affected = cursor.rowcount
    connection.commit()
    connection.close()
    return rows_affected

# Helper function to get sensor with measurements
def get_sensor_with_measurements(sensor_id):
    """Get sensor with all its measurements"""
    sensor = get_sensor_by_id(sensor_id)
    if sensor:
        measurements = get_measurements_by_sensor(sensor_id)
        return {
            'sensor': sensor,
            'measurements': measurements
        }
    return None
