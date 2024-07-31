# pip install kafka-python-ng
import six
import sys
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import json
import time

# Configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'test_topic'

# Producer: Send a message
def produce_message():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    import time 
    message = {'message': f'Hello, Kafka! {time.localtime()}'}
    try:
        # Send message to Kafka
        producer.send(TOPIC_NAME, message)
        producer.flush()  # Ensure all messages are sent
        print(f"Message sent: {message}")
    except KafkaError as e:
        print(f"Failed to send message: {e}")
    finally:
        producer.close()

# Consumer: Consume messages
def consume_messages():
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset='earliest',
        enable_auto_commit=True,  # Enable automatic offset committing
        group_id='GROUP_ID',  # Group ID for tracking offsets
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    print(f"Subscribed to topic: {TOPIC_NAME}")
    for message in consumer:
        print(f"Received message: {message.value}")
        # break  # For demonstration, just consume one message
    consumer.close()

if __name__ == "__main__":
    # Produce and consume messages
    produce_message()
    time.sleep(1)  # Give Kafka some time to process
    consume_messages()
