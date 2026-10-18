import os
import sys

# Перехватываем инициализацию драйвера до импорта Cluster, 
# чтобы он не пытался искать удаленный в Python 3.12+ asyncore
import cassandra.cluster
from cassandra.io.asyncioreactor import AsyncioConnection
cassandra.cluster.DEFAULT_CONNECTION_CLASS = AsyncioConnection

from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from datetime import datetime, timezone

class GPSHarness:
    def __init__(self, contact_points=['127.0.0.1'], keyspace='transport_tracking'):
        self.cluster = Cluster(contact_points, connection_class=AsyncioConnection)
        self.session = self.cluster.connect(keyspace)

    def close(self):
        self.cluster.shutdown()

    def insert_point(self, vehicle_id, date, ts, lat, lon, speed, alt, status):
        query = """
            INSERT INTO vehicle_gps_tracks (vehicle_id, date, timestamp, latitude, longitude, speed, altitude, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.session.execute(query, (vehicle_id, date, ts, lat, lon, speed, alt, status))

    def insert_batch(self, points):
        batch = BatchStatement()
        query = self.session.prepare("""
            INSERT INTO vehicle_gps_tracks (vehicle_id, date, timestamp, latitude, longitude, speed, altitude, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """)
        for p in points:
            batch.add(query, (p['vehicle_id'], p['date'], p['timestamp'], p['lat'], p['lon'], p['speed'], p['alt'], p['status']))
        self.session.execute(batch)

    def get_track_by_date(self, vehicle_id, date):
        query = "SELECT * FROM vehicle_gps_tracks WHERE vehicle_id = %s AND date = %s"
        return list(self.session.execute(query, (vehicle_id, date)))

    def get_track_by_time_range(self, vehicle_id, date, start_ts, end_ts):
        query = """
            SELECT * FROM vehicle_gps_tracks 
            WHERE vehicle_id = %s AND date = %s AND timestamp >= %s AND timestamp <= %s
        """
        return list(self.session.execute(query, (vehicle_id, date, start_ts, end_ts)))

    def get_latest_position(self, vehicle_id, date):
        query = "SELECT * FROM vehicle_gps_tracks WHERE vehicle_id = %s AND date = %s LIMIT 1"
        rows = list(self.session.execute(query, (vehicle_id, date)))
        return rows[0] if rows else None

    def get_speeding_events(self, vehicle_id, date, min_speed):
        rows = self.get_track_by_date(vehicle_id, date)
        return [row for row in rows if row.speed > min_speed]

    def insert_with_ttl(self, vehicle_id, date, ts, lat, lon, speed, alt, status, ttl_seconds):
        query = """
            INSERT INTO vehicle_gps_tracks (vehicle_id, date, timestamp, latitude, longitude, speed, altitude, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) USING TTL %s
        """
        self.session.execute(query, (vehicle_id, date, ts, lat, lon, speed, alt, status, ttl_seconds))

    def delete_daily_track(self, vehicle_id, date):
        query = "DELETE FROM vehicle_gps_tracks WHERE vehicle_id = %s AND date = %s"
        self.session.execute(query, (vehicle_id, date))