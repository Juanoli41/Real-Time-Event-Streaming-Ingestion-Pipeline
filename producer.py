import json
import time
import random
from kafka import KafkaProducer
from faker import Faker
from datetime import datetime

fake = Faker()

# Initialize Kafka producer by pointing it to the container
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC_NAME = 'user_events'
categories = ['sports', 'politics', 'entertainment', 'technology', 'health']

print('Starting producer... Press Ctrl+C to exit')
try:
    while True:
        event = {
            'user_id': fake.uuid4(),
            'event_type': random.choice(['click', 'view', 'purchase']),
            'category': random.choice(categories),
            'timestamp': datetime.now().isoformat()
        }
        # Fixed to use the TOPIC_NAME variable consistently
        producer.send(TOPIC_NAME, value=event)
        print(f'Sent event: {event}')
        time.sleep(random.uniform(0.5, 2))  # Random delay between events
except KeyboardInterrupt:
    print('Stopping producer...')
    producer.close()