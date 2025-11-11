# consumer/test_consumer.py
# from kafka import KafkaConsumer
# consumer = KafkaConsumer('test-topic', bootstrap_servers='localhost:9092', auto_offset_reset='earliest')
# for msg in consumer:
#     print(msg.value)

from kafka import KafkaConsumer
import json
import time
from collections import defaultdict
import random
from prometheus_client import start_http_server, Gauge

# --- Stream Metrics Storage ---
page_views = defaultdict(int)
clicks = defaultdict(int)
session_duration = defaultdict(list)
user_sessions = defaultdict(set)

# --- Kafka Consumer Setup ---
consumer = KafkaConsumer(
    'user-events',
    bootstrap_servers=['localhost:29092', 'kafka:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    group_id=f'analytics-group-{random.randint(1,9999)}',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("📊 Metrics Consumer started...")

def compute_metrics(event):
    """Update in-memory metrics based on incoming event"""
    user = event["user_id"]
    session = event["session_id"]
    action = event["action"]
    page = event["page"]
    duration = event["duration"]

    # Track unique session visits per user
    user_sessions[user].add(session)

    if action == "page_view":
        page_views[page] += 1
        session_duration[session].append(duration)
    elif action == "click":
        clicks[session] += 1

def print_summary():
    """Display aggregated metrics"""
    avg_duration = {
        s: round(sum(v) / len(v), 2) for s, v in session_duration.items() if v
    }
    bounce_rate = compute_bounce_rate()

    print("\n===== LIVE METRICS =====")
    print("Page Views:", dict(page_views))
    print("Clicks per Session:", dict(clicks))
    print("Avg Duration per Session:", avg_duration)
    print(f"Bounce Rate: {bounce_rate:.2f}%")
    print("=========================\n")

def compute_bounce_rate():
    """Sessions with only one page_view = bounce"""
    total_sessions = len(session_duration)
    if total_sessions == 0:
        return 0.0
    bounces = sum(1 for s, v in session_duration.items() if len(v) == 1)
    return (bounces / total_sessions) * 100

# --- Consume Events ---
# last_print = time.time()
# for msg in consumer:
#     event = msg.value
#     compute_metrics(event)

#     if time.time() - last_print > 5:  # print every 5 sec
#         print_summary()
#         last_print = time.time()

# --- Prometheus Metrics ---
page_views_gauge = Gauge('page_views_total', 'Total number of page views')
clicks_gauge = Gauge('clicks_total', 'Total number of clicks')
avg_duration_gauge = Gauge('average_session_duration_seconds', 'Average session duration in seconds')
bounce_rate_gauge = Gauge('bounce_rate_percent', 'Percentage of bounced sessions')

def update_prometheus_metrics():
    total_views = sum(page_views.values())
    total_clicks = sum(clicks.values())
    total_sessions = len(session_duration)

    avg_duration = (
        sum(sum(v) / len(v) for v in session_duration.values() if v) / total_sessions
        if total_sessions > 0 else 0
    )

    bounce_rate = compute_bounce_rate()

    page_views_gauge.set(total_views)
    clicks_gauge.set(total_clicks)
    avg_duration_gauge.set(avg_duration)
    bounce_rate_gauge.set(bounce_rate)

if __name__ == "__main__":
    print("📊 Metrics Consumer started with Prometheus exporter...")
    start_http_server(8000)  # Exposes metrics at http://localhost:8000/metrics
    last_print = time.time()

    for msg in consumer:
        event = msg.value
        compute_metrics(event)

        if time.time() - last_print > 5:
            print_summary()
            update_prometheus_metrics()  # Push to Prometheus
            last_print = time.time()
