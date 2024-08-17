create table if not exists observations (
    battery integer,
    device_id text,
    device_type text,
    humidity real,
    temperature real,
    version text,
    created_at text
);
