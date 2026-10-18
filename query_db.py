import sqlite3

def query_database():
    conn = sqlite3.connect('lifeline.db')
    cursor = conn.cursor()

    print("\n=== PROJECT LIFELINE: EMERGENCY DISPATCH LOG ===")

    # 1. Get the latest fall event
    cursor.execute('''
        SELECT event_id, patient_id, timestamp, gps_latitude, gps_longitude, battery_level, event_status
        FROM fall_events ORDER BY timestamp DESC LIMIT 1
    ''')
    event = cursor.fetchone()

    if not event:
        print("No events found in the database.")
        return

    event_id, patient_id, timestamp, lat, lon, battery, status = event
    print(f"Timestamp : {timestamp}")
    print(f"Status    : {status}")
    print(f"Location  : {lat}, {lon} (Battery: {battery}%)")

    # 2. Get Patient & Contact Info
    cursor.execute('''
        SELECT p.full_name, p.cardiac_medical_id, e.contact_name, e.phone_number
        FROM patients p
        JOIN emergency_contacts e ON p.patient_id = e.patient_id
        WHERE p.patient_id = ?
    ''', (patient_id,))
    patient_info = cursor.fetchone()

    if patient_info:
        p_name, med_id, c_name, c_phone = patient_info
        print(f"Patient   : {p_name} | Medical ID: {med_id}")
        print(f"Notified  : {c_name} at {c_phone}")

    # 3. Get IMU Telemetry Data
    print("\n--- KINEMATIC TELEMETRY (12-Second Window) ---")
    cursor.execute('''
        SELECT time_offset_ms, svm, gyro_x
        FROM imu_telemetry
        WHERE event_id = ?
        ORDER BY time_offset_ms ASC
    ''', (event_id,))
    telemetry = cursor.fetchall()

    print("Time(ms) | SVM (g) | Tilt/Gyro X")
    print("--------------------------------")
    for t in telemetry:
        print(f"{t[0]:<8} | {t[1]:<7} | {t[2]}")

    print("================================================\n")

    conn.close()

if __name__ == '__main__':
    query_database()