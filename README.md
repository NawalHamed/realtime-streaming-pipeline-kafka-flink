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

