import os

import paho.mqtt.client as mqtt
import psycopg
import redis
from dotenv import load_dotenv

load_dotenv()


def test_postgres_extensions():
    dsn = (
        f"host=localhost dbname={os.environ['POSTGRES_DB']} "
        f"user={os.environ['POSTGRES_USER']} password={os.environ['POSTGRES_PASSWORD']}"
    )
    with psycopg.connect(dsn) as conn:
        names = {r[0] for r in conn.execute("SELECT extname FROM pg_extension")}
    assert {"timescaledb", "vector"} <= names


def test_mqtt_connects():
    c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    assert c.connect("localhost", 1883) == 0
    c.disconnect()


def test_redis_ping():
    assert redis.from_url(os.environ["REDIS_URL"]).ping()
