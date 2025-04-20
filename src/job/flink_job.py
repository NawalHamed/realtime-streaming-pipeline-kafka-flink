# flink_job.py
from pyflink.table import TableEnvironment, EnvironmentSettings
import os

# Step 1: Set up Flink Table Environment
env_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(env_settings)

#Step 2: Define Kafka Source Table
source_ddl = f"""
    CREATE TABLE kafka_posts (
        id INT,
        title STRING,
        body STRING,
        userId INT
    ) WITH (
        'connector' = 'kafka',
        'topic' = '{os.environ.get("KAFKA_TOPIC", "posts")}',
        'properties.bootstrap.servers' = '{os.environ.get("KAFKA_BROKER", "kafka:9092")}',
        'properties.group.id' = 'flink-consumer-group',
        'format' = 'json',
        'scan.startup.mode' = 'latest-offset'
    )
"""
t_env.execute_sql(source_ddl)

#Step 3: Define PostgreSQL Sink Table
sink_ddl = f"""
    CREATE TABLE posts (
        id INT,
        title VARCHAR,
        body VARCHAR,
        userId INT
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

#Step 4: Submit the job
t_env.execute_sql("""
    INSERT INTO posts
    SELECT id, title, body, userId
    FROM kafka_posts
""")