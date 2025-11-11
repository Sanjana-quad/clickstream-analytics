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
| Stream Processing | Kafka Cnsumer + Python |
| Metrics Export | Prometheus Client |
| Storage / Visualization | Grafana |
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
- DockerFile.consumer
- grafana_dashboard.json
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
The consumer should output aggregated metrics in the console every few seconds.

## 📈 Learning Outcome

~ Kafka cluster setup using Docker
~ Basic producer–consumer pipeline validation
~ Project skeleton ready for stream processing

## 🛰️ Milestone 2 – Producer: Simulate Clickstream Events
 
Script: `producer/event_producer.py`
Continuously generates synthetic user interaction events.
Publishes JSON events to Kafka topic user-events.
Run locally:
    ```bash
    python producer/event_producer.py

Each event looks like:
    ```json
    {
    "event_id": "5d34b89c-3a34-44a8-9dc0-2b9abcf5f7d5",
    "user_id": 1432,
    "session_id": 32,
    "page": "/products",
    "action": "click",
    "duration": 2.4,
    "timestamp": 1731283897.211
    }

## 🧮 Milestone 3 – Consumer: Real-Time Metric Aggregation

Script: `consumer/metrics_consumer.py`
- Consumes data from the same Kafka topic (user-events).
- Computes engagement metrics such as:
-- page_views_total
-- clicks_total
-- average_session_duration_seconds
-- bounce_rate_percent
- Exposes them via Prometheus at http://localhost:8000/metrics

Run inside container (auto):
    ```bash
    docker compose up -d consumer

Run locally (manual mode):
    ```bash
    python consumer/metrics_consumer.py

Sample output:
    ```yaml
    📊 Metrics Consumer started with Prometheus exporter...
    ===== LIVE METRICS =====
    Page Views: {'/home': 12, '/cart': 3}
    Clicks per Session: {1: 5, 2: 2}
    Avg Duration per Session: {1: 5.23, 2: 3.14}
    Bounce Rate: 25.00%
    =========================

## 📊 Milestone 4 – Monitoring with Prometheus & Grafana

### Prometheus (prometheus.yml)

Run Prometheus:
    ```bash
    docker compose up -d prometheus
Access at → http://localhost:9090

### Grafana Dashboard Setup

1. Go to → http://localhost:3000
2. Default login → admin / admin
3. Add data source → Prometheus, URL: http://prometheus:9090
4. Create a new dashboard with these panels:

| Panel Title | PromQL Query |
| Page Views Over Time | page_views_total |
| Clicks Over Time | clicks_total |
| Avg Session Duration | average_session_duration_seconds |
| Bounce Rate | bounce_rate_percent |

💡 Tip: Set refresh interval to 5s for a live analytics effect.

## 🧠 Learning Outcomes

✅ Kafka cluster setup using Docker
✅ Producer–consumer data streaming
✅ Real-time metrics aggregation
✅ Prometheus monitoring integration
✅ Grafana dashboard visualization
✅ Understanding event-driven architecture end to end

## 🌐 Future Extensions

Deploy Kafka on Confluent Cloud or AWS MSK
Add Streamz/Faust for windowed aggregations
Push processed data to Elasticsearch or PostgreSQL
Containerize the producer
Integrate alerting in Prometheus (threshold breaches)