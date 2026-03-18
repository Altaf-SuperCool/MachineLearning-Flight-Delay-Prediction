import time
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter("inference_requests_total", "Total inference requests")
REQUEST_ERRORS = Counter("inference_request_errors_total", "Total failed requests")
LATENCY = Histogram("inference_latency_seconds", "Inference latency in seconds")

def observe_latency(start_time: float):
    LATENCY.observe(time.time() - start_time)
