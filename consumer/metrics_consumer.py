# consumer/test_consumer.py
from kafka import KafkaConsumer
consumer = KafkaConsumer('test-topic', bootstrap_servers='localhost:9092', auto_offset_reset='earliest')
for msg in consumer:
    print(msg.value)
