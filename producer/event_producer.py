# producer/test_producer.py
# from kafka import KafkaProducer
# producer = KafkaProducer(bootstrap_servers='localhost:9092')
# producer.send('test-topic', b'Hello Kafka!')
# producer.flush()
# print("Message sent!")

from kafka import KafkaProducer
import json
import time
import random
import uuid

# Kafka setup
producer = KafkaProducer(
    bootstrap_servers='localhost:29092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Simulated pages and actions
PAGES = ["/home", "/products", "/cart", "/checkout", "/about"]
ACTIONS = ["page_view", "click", "scroll", "add_to_cart"]

def generate_event():
    """Simulate a user interaction event"""
    event = {
        "event_id": str(uuid.uuid4()),
        "user_id": random.randint(1000, 2000),
        "session_id": random.randint(1, 100),
        "page": random.choice(PAGES),
        "action": random.choice(ACTIONS),
        "duration": round(random.uniform(0.5, 10.0), 2),  # seconds on page
        "timestamp": time.time()
    }
    return event

if __name__ == "__main__":
    print("📡 Starting Clickstream Event Producer...")
    while True:
        event = generate_event()
        producer.send("user-events", event)
        print(f"Sent: {event}")
        time.sleep(random.uniform(0.5, 2.0))  # simulate user delay