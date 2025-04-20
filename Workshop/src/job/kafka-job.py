from pyflink.table import TableEnvironment, EnvironmentSettings, DataTypes
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table.udf import ScalarFunction, udf
import requests
import json
from kafka import KafkaProducer
import os
import time

# Fetch data from API
def fetch_posts():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch posts: {response.status_code}")

# Publish data to Kafka
def publish_to_kafka(posts):
    producer = KafkaProducer(
        bootstrap_servers=os.environ.get("KAFKA_BROKER", "kafka:9092"),
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    topic = os.environ.get("KAFKA_TOPIC", "posts")
    for post in posts:
        producer.send(topic, post)
    producer.flush()

# Set up Flink Table Environment
env_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(env_settings)

# Define Kafka Source Table
source_ddl = f"""
    CREATE TABLE kafka_posts (
        id INT,
        title STRING,
        body STRING,
        user_id INT
    ) WITH (
        'connector' = 'kafka',
        'topic' = '{os.environ.get("KAFKA_TOPIC", "posts")}',
        'properties.bootstrap.servers' = '{os.environ.get("KAFKA_BROKER", "kafka:9092")}',
        'properties.group.id' = 'flink-consumer-group',
        'format' = 'json',
        'scan.startup.mode' = 'earliest-offset'
    )
"""
t_env.execute_sql(source_ddl)

# Define PostgreSQL Sink Table
sink_ddl = f"""
    CREATE TABLE posts (
        id INT,
        title VARCHAR,
        body VARCHAR,
        user_id INT
    ) WITH (
        'connector' = 'jdbc',
        'url' = '{os.environ.get("POSTGRES_URL", "jdbc:postgresql://host.docker.internal:5432/postgres")}',
        'table-name' = 'posts',
        'username' = '{os.environ.get("POSTGRES_USER", "postgres")}',
        'password' = '{os.environ.get("POSTGRES_PASSWORD", "postgres")}',
        'driver' = 'org.postgresql.Driver'
    )
"""
t_env.execute_sql(sink_ddl)

# Define Transformation
t_env.execute_sql("""
    INSERT INTO posts
    SELECT id, title, body, user_id
    FROM kafka_posts
""")

# Continuously fetch posts and publish to Kafka
while True:
    posts = fetch_posts()
    publish_to_kafka(posts)
    print(f"Published {len(posts)} posts to Kafka.")
    time.sleep(60)  # Sleep for 1 minute before fetching the next batch of posts
