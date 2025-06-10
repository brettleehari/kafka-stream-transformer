import time
import json
import random
import os
from kafka import KafkaProducer

# Configuration
KAFKA_SERVER = os.environ.get('KAFKA_SERVER', 'localhost:9092')  # Use 'kafka:9092' in Docker Compose, 'localhost:9092' on host
TOPIC = os.environ.get('KAFKA_TOPIC', 'test_topic')

# Sample messages
MESSAGES = [
    {"username": "alice", "age": 30, "email": "alice@example.com"},
    {"username": "bob", "age": 25, "email": "bob@example.com"},
    {"username": "carol", "age": 28, "email": "carol@example.com"},
    {"username": "dave", "age": 35, "email": "dave@example.com"},
    {"username": "eve", "age": 22, "email": "eve@example.com"}
]

def main():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    print(f"Producing messages to topic '{TOPIC}' every 10 seconds. Press Ctrl+C to stop.")
    try:
        while True:
            msg = random.choice(MESSAGES)
            producer.send(TOPIC, msg)
            print(f"Sent: {msg}")
            time.sleep(10)
    except KeyboardInterrupt:
        print("Stopped producer.")
    finally:
        producer.close()

if __name__ == "__main__":
    main()
