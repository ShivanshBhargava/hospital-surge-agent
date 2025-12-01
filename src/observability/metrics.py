# src/observability/metrics.py
import time

class Metrics:
    def __init__(self):
        self.data = {}

    def start(self, label):
        self.data[label] = time.time()

    def end(self, label):
        if label in self.data:
            duration = time.time() - self.data[label]
            self.data[label] = duration
            return duration
        return None

metrics = Metrics()
