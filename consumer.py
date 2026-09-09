import os
import json
from kafka import KafkaConsumer
import psycopg2

# Connect to PostgreSQL via environment variables
db_password = os.getenv("DB_PASSWORD")
if not db_password:
    raise RuntimeError("DB_PASSWORD is not set")

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME", "streaming_db"),
    user=os.getenv("DB_USER", "postgres"),
    password=db_password,
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432")
)
cursor = conn.cursor()

# Ensure target table exists to match the event payload
cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_events (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR(50),
        event_type VARCHAR(50),
        category VARCHAR(50),
        timestamp VARCHAR(50)
    );
""")
conn.commit()

# Initialize Kafka Consumer listening to 'user_events'
consumer = KafkaConsumer(
    'user_events',
    bootstrap_servers=[os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id=os.getenv("KAFKA_GROUP_ID", "user-events-group-1"),
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Listening for streaming events...")

try:
    for message in consumer:
        event = message.value
        print(f"Received raw message: {event}")

        user_id = event['user_id']
        event_type = event['event_type']
        category = event['category']
        timestamp = event['timestamp']

        cursor.execute("""
            INSERT INTO user_events (user_id, event_type, category, timestamp)
            VALUES (%s, %s, %s, %s);
        """, (user_id, event_type, category, timestamp))

        conn.commit()
        print("Successfully inserted row into PostgreSQL!")

except KeyboardInterrupt:
    print("Stopping consumer...")
finally:
    cursor.close()
    conn.close()
    consumer.close()