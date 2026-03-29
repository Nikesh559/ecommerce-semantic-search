# from kafka import KafkaConsumer
# import json

# # Create consumer
# consumer = KafkaConsumer(
#     'products',
#     bootstrap_servers='localhost:9092',
#     auto_offset_reset='latest',   # read from beginning
#     enable_auto_commit=True,
#     group_id='my-group',
#     value_deserializer=lambda x: json.loads(x.decode('utf-8'))
# )

# print("Listening for messages...")

# # Consume messages
# for message in consumer:
#     print("Received:", message.value)

from fastapi import FastAPI
from kafka import KafkaConsumer
import threading
import json

app = FastAPI()

def consume_messages():
    consumer = KafkaConsumer(
        'products',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    print("Kafka consumer started...")
    for message in consumer:
        print("Received :", message.value)

# Start consumer in background thread
@app.on_event("startup")
def start_kafka_consumer():
    thread = threading.Thread(target=consume_messages, daemon=True)
    thread.start()