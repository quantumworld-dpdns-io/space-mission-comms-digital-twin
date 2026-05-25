from __future__ import annotations

from typing import Any

import numpy as np


class TelemetryService:
    def __init__(self):
        self.telemetry_buffer: dict[str, list[dict[str, Any]]] = {}

    def ingest(self, source: str, data: dict[str, Any]) -> bool:
        if source not in self.telemetry_buffer:
            self.telemetry_buffer[source] = []
        self.telemetry_buffer[source].append(data)
        return True

    def get_latest(self, source: str, n: int = 10) -> list[dict[str, Any]]:
        buf = self.telemetry_buffer.get(source, [])
        return buf[-n:]

    def compute_statistics(self, source: str, field: str) -> dict[str, float]:
        buf = self.telemetry_buffer.get(source, [])
        values = [d.get(field, 0.0) for d in buf if field in d]
        if not values:
            return {"min": 0, "max": 0, "mean": 0, "std": 0}
        arr = np.array(values)
        return {
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
            "mean": float(np.mean(arr)),
            "std": float(np.std(arr)),
            "last": float(arr[-1]),
        }

    def check_anomaly(self, source: str, field: str, threshold: float = 3.0) -> list[int]:
        buf = self.telemetry_buffer.get(source, [])
        values = [d.get(field, 0.0) for d in buf if field in d]
        if len(values) < 10:
            return []
        arr = np.array(values)
        mean, std = np.mean(arr), np.std(arr)
        if std == 0:
            return []
        anomalies = np.where(np.abs(arr - mean) > threshold * std)[0]
        return [int(i) for i in anomalies]
