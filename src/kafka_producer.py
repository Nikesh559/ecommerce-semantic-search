from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Kafka producer initialized")

def send_product_message(product):
    try:
        print("Sending message to Kafka...", product)

        future = producer.send('products', value=product)
        metadata = future.get(timeout=10)

        print("Message sent successfully!")
        print("Topic:", metadata.topic, "Partition:", metadata.partition)

    except Exception as e:
        print("Error sending message:", str(e))