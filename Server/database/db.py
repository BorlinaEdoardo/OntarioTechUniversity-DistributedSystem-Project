from datetime import datetime
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "sensors.db")

def get_connection():
    """Get a database connection."""
    return sqlite3.connect(DB_PATH)

def create_tables():
    """Create the database tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # SENSOR table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SENSOR(
            Id   INTEGER PRIMARY KEY AUTOINCREMENT,
            City TEXT NOT NULL
        )
    """)
    
    # MEASUREMENT table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS MEASUREMENT(
            Id        INTEGER PRIMARY KEY AUTOINCREMENT,
            Measure   REAL NOT NULL,
            Timestamp DATETIME NOT NULL,
            Pollutant TEXT NOT NULL,
            Sensor_id INTEGER,
            FOREIGN KEY (Sensor_id) REFERENCES SENSOR(Id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    conn.close()

# ========== SENSOR CRUD ==========

def create_sensor(city):
    """Create a new sensor"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO SENSOR (City) VALUES (?)", (city,))
    sensor_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return sensor_id

def get_sensor_by_id(sensor_id):
    """Get a sensor by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SENSOR WHERE Id = ?", (sensor_id,))
    sensor = cursor.fetchone()
    conn.close()
    return sensor

def get_all_sensors():
    """Get all sensors."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SENSOR")
    sensors = cursor.fetchall()
    conn.close()
    return sensors

def update_sensor(sensor_id, city):
    """Update a sensor's city."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE SENSOR SET City = ? WHERE Id = ?",
        (city, sensor_id)
    )
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected

def delete_sensor(sensor_id):
    """Delete a sensor."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM SENSOR WHERE Id = ?", (sensor_id,))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected

# ========== MEASUREMENT CRUD ==========

def create_measurement(measure, pollutant, sensor_id, timestamp=None):
    """Create a new measurement."""
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO MEASUREMENT (Measure, Timestamp, Pollutant, Sensor_id) "
        "VALUES (?, ?, ?, ?)",
        (measure, timestamp, pollutant, sensor_id)
    )
    measurement_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return measurement_id

def get_measurement_by_id(measurement_id):
    """Get a measurement by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM MEASUREMENT WHERE Id = ?",
        (measurement_id,)
    )
    measurement = cursor.fetchone()
    conn.close()
    return measurement

def get_measurements_by_sensor(sensor_id):
    """Get all measurements for a specific sensor."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM MEASUREMENT WHERE Sensor_id = ?",
        (sensor_id,)
    )
    measurements = cursor.fetchall()
    conn.close()
    return measurements

def get_all_measurements():
    """Get all measurements."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MEASUREMENT")
    measurements = cursor.fetchall()
    conn.close()
    return measurements

def update_measurement(measurement_id, measure, pollutant, timestamp=None):
    """Update a measurement."""
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE MEASUREMENT "
        "SET Measure = ?, Timestamp = ?, Pollutant = ? "
        "WHERE Id = ?",
        (measure, timestamp, pollutant, measurement_id)
    )
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected

def delete_measurement(measurement_id):
    """Delete a measurement."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM MEASUREMENT WHERE Id = ?", (measurement_id,))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected

# Helper

def get_sensor_with_measurements(sensor_id):
    """Get sensor with all its measurements."""
    sensor = get_sensor_by_id(sensor_id)
    if sensor:
        measurements = get_measurements_by_sensor(sensor_id)
        return {
            "sensor": sensor,
            "measurements": measurements
        }
    return None