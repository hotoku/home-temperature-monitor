import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .types import Observation


def connect() -> sqlite3.Connection:
    return sqlite3.connect("db.sqlite")


def create_table():
    with open(Path(__file__).parent / "create_table.sql") as f:
        ddl = f.read()
    with connect() as conn:
        conn.execute(ddl)


def insert_observation(observation: Observation):
    jst = timezone(timedelta(hours=9))
    cur = datetime.now(jst)
    with connect() as conn:
        conn.execute(
            "INSERT INTO observations (battery, device_id, device_type, humidity, temperature, version, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (observation.battery, observation.deviceId, observation.deviceType, observation.humidity,
             observation.temperature, observation.version, cur.isoformat())
        )
