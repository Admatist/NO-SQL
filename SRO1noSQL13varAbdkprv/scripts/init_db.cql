CREATE KEYSPACE IF NOT EXISTS transport_tracking 
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE transport_tracking;

CREATE TABLE IF NOT EXISTS vehicle_gps_tracks (
    vehicle_id text,
    date text,
    timestamp timestamp,
    latitude double,
    longitude double,
    speed double,
    altitude double,
    status text,
    PRIMARY KEY ((vehicle_id, date), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);