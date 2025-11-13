import sqlite3
connection = sqlite3.connect("Server\database\sensors.db")

cursor = connection.cursor()

# Create table Sensor
cursor.execute("""
    CREATE TABLE IF NOT EXISTS SENSOR(
               Id INTEGER PRIMARY KEY AUTOINCREMENT,
               City TEXT NOT NULL,
               Pollutant TEXT NOT NULL
               )
 """)


# Create table Measurement
cursor.execute("""
    CREATE TABLE IF NOT EXISTS MEASUREMENT(
               Id INTEGER PRIMARY KEY AUTOINCREMENT,
               Measure FLOAT NOT NULL,
               Timestamp DATETIME NOT NULL,
               Sensor_id INTEGER,
               FOREIGN KEY (Sensor_id) REFERENCES SENSOR(Id)
               ON UPDATE CASCADE
               ON DELETE CASCADE
               )
 """)

connection.commit()
connection.close()
