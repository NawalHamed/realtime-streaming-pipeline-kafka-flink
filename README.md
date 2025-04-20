# 🌀 Realtime Streaming Pipeline: Kafka + Flink (PyFlink)

This project sets up a real-time streaming data pipeline using **Apache Flink (PyFlink)**, **Apache Kafka**, **Zookeeper**, and a **custom JSON data producer**. It ingests data from a mocked external API, sends it to Kafka, and processes it using PyFlink. Optionally, the processed data can be stored in a PostgreSQL database.

---

## 🧱 Stack Overview

| Component                  | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| **JobManager**            | Flink JobManager to coordinate task execution.                              |
| **TaskManager**           | Flink TaskManager for parallel stream processing.                           |
| **Kafka**                 | Message broker used to receive and distribute data.                         |
| **Zookeeper**             | Manages Kafka cluster state.                                                |
| **json_placeholder_generate** | Python script that fetches data from a public API and sends it to Kafka.     |
| **PostgreSQL**            | External database assumed to be accessible via `host.docker.internal`.      |

---

## 📁 Project Structure

. ├── Dockerfile # For building the PyFlink image ├── Dockerfile.fetch # For building the JSON producer image ├── docker-compose.yml # Main Docker Compose setup ├── src/ # Source code for Flink jobs ├── fetch_and_produce/ # Python script that fetches and sends data to Kafka ├── kafka_scripts/ # Kafka-related scripts/configs ├── flink-env.env # Flink environment variables
---

## ⚙️ How to Run

### ✅ Prerequisites

Make sure you have installed the following:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- PostgreSQL running locally or externally, accessible via `host.docker.internal`

---

### 🔧 Step-by-Step Instructions

#### 1. Create External Docker Network

This allows different containers across projects to communicate.

```bash
docker network create shared_network

2. Build & Start All Services
Run the following command from the root of the project:

docker compose up --build

This command will:

Build Docker images for PyFlink and the JSON data producer.

Start Kafka, Zookeeper, Flink JobManager, and TaskManager.

Start the JSON producer that fetches fake API data and sends it to Kafka.


🔁 Data Flow Overview
JSON Producer (json_placeholder_generate) fetches data from JSONPlaceholder.

The producer pushes the data into a Kafka topic.

Apache Flink (PyFlink) reads from Kafka, processes the stream.

(Optional) Flink can write results into a PostgreSQL database.


🔐 Environment Variables
Environment values can be placed in the flink-env.env file or defined in docker-compose.yml.

Variable | Default Value | Description
POSTGRES_URL | jdbc:postgresql://host.docker.internal:5432/postgres | JDBC connection string
POSTGRES_USER | postgres | PostgreSQL username
POSTGRES_PASSWORD | postgres | PostgreSQL password
POSTGRES_DB | postgres | Database name


🔎 Useful URLs & Ports
Service | URL/Port
Flink UI | http://localhost:8081
Kafka | localhost:9092
Zookeeper | localhost:2181
JSON API | http://localhost:8000

📝 Notes
This setup is intended for local development only.

PostgreSQL is not included in this Compose file. Ensure it is running locally or externally, and accessible via host.docker.internal.

Volumes are mapped, and ports are exposed to allow debugging and experimentation.






