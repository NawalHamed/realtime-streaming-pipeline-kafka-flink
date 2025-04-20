# fetch_and_produce.py
from kafka import KafkaProducer
import requests
import json
import os
import time

def fetch_posts():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch posts: {response.status_code}")

def publish_to_kafka(posts):
    producer = KafkaProducer(
        bootstrap_servers=os.environ.get("KAFKA_BROKER", "kafka:9092"),
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    topic = os.environ.get("KAFKA_TOPIC", "posts")
    for post in posts:
        producer.send(topic, post)
    producer.flush()

while True:
    posts = fetch_posts()
    publish_to_kafka(posts)
    print(f"Published {len(posts)} posts to Kafka.")
    time.sleep(1)  # Sleep for 1 minute
