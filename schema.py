import sqlite3

def init_db():
    conn = sqlite3.connect('lifeline.db')
    cursor = conn.cursor()

    # Table: Patients
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        patient_id TEXT PRIMARY KEY,
        full_name TEXT NOT NULL,
        age INTEGER,
        cardiac_medical_id TEXT
    )''')

    # Table: Emergency Contacts
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS emergency_contacts (
        contact_id TEXT PRIMARY KEY,
        patient_id TEXT,
        contact_name TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
    )''')

    # Table: Fall Events
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fall_events (
        event_id TEXT PRIMARY KEY,
        patient_id TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        gps_latitude REAL,
        gps_longitude REAL,
        battery_level INTEGER,
        event_status TEXT,
        FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
    )''')

    # Table: IMU Telemetry (50 Hz Window)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS imu_telemetry (
        telemetry_id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id TEXT,
        time_offset_ms INTEGER,
        accel_x REAL,
        accel_y REAL,
        accel_z REAL,
        gyro_x REAL,
        gyro_y REAL,
        gyro_z REAL,
        svm REAL,
        FOREIGN KEY (event_id) REFERENCES fall_events (event_id)
    )''')

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()