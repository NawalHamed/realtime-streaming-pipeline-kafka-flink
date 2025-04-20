# realtime-streaming-pipeline-kafka-flink
PyFlink with Kafka and PostgreSQL Pipeline
This project sets up a streaming data pipeline using Apache Flink (PyFlink), Kafka, Zookeeper, and a custom JSON data producer. It is designed to ingest data from a mocked external API, send it to Kafka, and process it using PyFlink.

🧱 Stack Overview

Component	Description
JobManager	Flink JobManager to coordinate task execution.
TaskManager	Flink TaskManager for parallel stream processing.
Kafka	Message broker used to receive and distribute data.
Zookeeper	Manages Kafka cluster state.
json_placeholder_generate	Custom Python script that fetches data from a public API and produces it to Kafka.
PostgreSQL	External database assumed to be accessible via host.docker.internal.

📁 Project Structure

bash
Copy
Edit
.
├── Dockerfile             # For building the PyFlink image
├── Dockerfile.fetch       # For building the JSON producer image
├── docker-compose.yml     # Main Docker Compose setup
├── src/                   # Source code for Flink jobs
├── fetch_and_produce/     # Python script that fetches and sends data to Kafka
├── kafka_scripts/         # Kafka-related scripts/configs
├── flink-env.env          # Flink environment variables

⚙️ How to Run

1. Ensure External Network
Create the shared external Docker network if not already created:

bash
Copy
Edit
docker network create shared_network
2. Build & Start Services
bash
Copy
Edit
docker compose up --build
This will:

Build custom Docker images for Flink and the JSON producer.

Start Kafka, Zookeeper, Flink JobManager, and TaskManager.

Start the JSON producer to send API data to Kafka.

🔁 Data Flow

json_placeholder_generate fetches dummy JSON data from JSONPlaceholder.

The data is sent to a Kafka topic.

Flink (PyFlink) processes the streaming data from Kafka.

Optional: Flink sinks the data into PostgreSQL (configured via environment variables).

🔐 Environment Variables
Set in flink-env.env or passed directly in docker-compose.yml.


Variable	Default Value	Description
POSTGRES_URL	jdbc:postgresql://host.docker.internal:5432/postgres	PostgreSQL JDBC connection URL
POSTGRES_USER	postgres	PostgreSQL username
POSTGRES_PASSWORD	postgres	PostgreSQL password
POSTGRES_DB	postgres	PostgreSQL database name

🔎 Useful URLs

Service	URL
Flink UI	http://localhost:8081
Kafka Port	localhost:9092
Zookeeper	localhost:2181
JSON API	http://localhost:8000

📌 Notes

This setup is for local development. It maps volumes and exposes ports for debugging and testing.

PostgreSQL is not included in this Compose file. Ensure it's running and accessible via host.docker.internal.


