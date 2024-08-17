import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .types import Observation, SensorInfo


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


def read_record() -> SensorInfo:
    with connect() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""
select
  battery,
  humidity,
  temperature,
  created_at                    
from
  observations                    
order by
  created_at desc
limit 1
""")
        row = cur.fetchone()
        return SensorInfo(
            battery=row["battery"],
            humidity=row["humidity"],
            temperature=row["temperature"],
            created_at=datetime.fromisoformat(row["created_at"])
        )
