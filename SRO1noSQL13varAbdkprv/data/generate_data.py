from datetime import datetime, timedelta, timezone
from SRO1noSQL13varAbdkprv.src.queries import GPSHarness

def seed_data():
    db = GPSHarness()
    vehicle_ids = ["BUS-101", "TAXI-202", "TRUCK-303"]
    date_str = "2026-10-18"
    base_time = datetime.now(timezone.utc) - timedelta(hours=3)

    points = []
    for i in range(12):
        ts = base_time + timedelta(minutes=i*10)
        for v in vehicle_ids:
            points.append({
                'vehicle_id': v,
                'date': date_str,
                'timestamp': ts,
                'lat': 51.16 + (i * 0.002),
                'lon': 71.44 + (i * 0.002),
                'speed': 30.0 + (i * 4.5),
                'alt': 320.0,
                'status': 'MOVING' if i < 10 else 'IDLE'
            })

    db.insert_batch(points)
    print(f"Успешно добавлено {len(points)} синтетических записей в Cassandra.")
    db.close()

if __name__ == "__main__":
    seed_data()