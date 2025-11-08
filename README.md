# 🖱️ Clickstream Analytics Pipeline (Web Domain)

## 🎯 Goal
Simulate user website events → ingest with Kafka → compute user engagement metrics in real time.

---

## 🧩 Project Overview
This project mimics real-world web analytics pipelines used in digital products.  
It captures simulated user events (page views, clicks, time spent) and processes them using **Apache Kafka** to compute metrics like:
- Total sessions
- Click-through rate (CTR)
- Bounce rate
- Average session duration

---

## ⚙️ Tech Stack
| Component | Technology |
|------------|-------------|
| Programming Language | Python |
| Message Broker | Apache Kafka (via Docker) |
| Stream Processing | Streamz / Faust |
| Storage / Visualization | Elasticsearch + Kibana / Grafana |
| Deployment | Local → Confluent Cloud |

---

## 📁 Project Structure

clickstream-analytics/
- docker-compose.yml # Kafka + Zookeeper setup
- producer/
-- event_producer.py # Python producer (user-event simulator)
- consumer/
-- metrics_consumer.py # Python consumer (aggregator)
- analytics/
-- init.py
-- metrics.py # Metrics logic
- logs/
-- analytics.log
- requirements.txt
- README.md

---

## 🚀 Milestone 1 – Kafka Setup

### Step 1. Start Kafka Cluster
Run:
    ```bash
    docker-compose up -d

Verify containers:
    ```bash
    docker ps

### Step 2. Install Dependencies
    ```bash
    pip install kafka-python streamz requests elasticsearch
    pip freeze > requirements.txt

### Step 3. Test Producer
    ```bash
    python producer/test_producer.py

### Step 4. Test Consumer
    ```bash
    python consumer/test_consumer.py

## 📈 Learning Outcome

~ Kafka cluster setup using Docker
~ Basic producer–consumer pipeline validation
~ Project skeleton ready for stream processing

