import sqlite3
import uuid
from datetime import datetime

def simulate_event():
    conn = sqlite3.connect('lifeline.db')
    cursor = conn.cursor()

    # 1. Register a dummy patient
    patient_id = str(uuid.uuid4())
    cursor.execute('''
        INSERT INTO patients (patient_id, full_name, age, cardiac_medical_id)
        VALUES (?, ?, ?, ?)
    ''', (patient_id, 'Ahmad Bin Ali', 65, 'MED-CARDIAC-8899'))

    # 2. Add an emergency contact
    contact_id = str(uuid.uuid4())
    cursor.execute('''
        INSERT INTO emergency_contacts (contact_id, patient_id, contact_name, phone_number)
        VALUES (?, ?, ?, ?)
    ''', (contact_id, patient_id, 'Siti Binti Ali', '+60123456789'))

    # 3. Log a fall event (Phase 2 Impact triggered)
    event_id = str(uuid.uuid4())
    cursor.execute('''
        INSERT INTO fall_events (event_id, patient_id, timestamp, gps_latitude, gps_longitude, battery_level, event_status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (event_id, patient_id, datetime.now(), 4.3536, 100.9754, 42, 'Dispatched'))

    # 4. Insert dummy IMU telemetry matching your research dossier parameters
    telemetry_data = [
        # Phase 1: Free-Fall dip (0.2g)
        (event_id, 0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.2),    
        # Phase 2: Impact spike (3.4g) with >60 degree tilt rotation
        (event_id, 200, 0.0, 0.0, 3.4, 120.0, 50.0, 0.0, 3.4), 
        # Phase 4: Post-Fall Immobility (1.0g flatline)
        (event_id, 10000, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0)  
    ]
    
    cursor.executemany('''
        INSERT INTO imu_telemetry (event_id, time_offset_ms, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, svm)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', telemetry_data)

    conn.commit()
    conn.close()
    print("Simulated fall event inserted successfully!")

if __name__ == '__main__':
    simulate_event()