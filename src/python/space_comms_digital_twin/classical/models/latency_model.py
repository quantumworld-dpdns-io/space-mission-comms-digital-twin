from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import List

import numpy as np
from space_comms_digital_twin.config import SPEED_OF_LIGHT


def propagation_delay(distance_m: float) -> float:
    return distance_m / SPEED_OF_LIGHT


def queuing_delay(packet_size_bytes: int, queue_depth_packets: int, link_rate_bps: float) -> float:
    return (queue_depth_packets * packet_size_bytes * 8.0) / link_rate_bps


def processing_delay(packet_size_bytes: int, cpu_ops_per_byte: float = 100.0,
                     cpu_speed_ops: float = 1e9) -> float:
    return (packet_size_bytes * cpu_ops_per_byte) / cpu_speed_ops


def serialization_delay(packet_size_bytes: int, link_rate_bps: float) -> float:
    return (packet_size_bytes * 8.0) / link_rate_bps


def compute_rtt(simplex_latency: float) -> float:
    return 2.0 * simplex_latency


def compute_one_way_light_time(distance_m: float) -> float:
    return distance_m / SPEED_OF_LIGHT


def jitter_model(mean_delay: float, variance: float, distribution: str = "normal") -> float:
    if distribution == "normal":
        return random.gauss(mean_delay, math.sqrt(variance))
    elif distribution == "uniform":
        return random.uniform(mean_delay - variance, mean_delay + variance)
    return mean_delay


def total_latency_component(distance_m: float, packet_size_bytes: int,
                            link_rate_bps: float, queue_depth: int = 0,
                            cpu_speed_ops: float = 1e9) -> dict:
    return {
        "propagation": propagation_delay(distance_m),
        "serialization": serialization_delay(packet_size_bytes, link_rate_bps),
        "queuing": queuing_delay(packet_size_bytes, queue_depth, link_rate_bps) if queue_depth > 0 else 0.0,
        "processing": processing_delay(packet_size_bytes, 100.0, cpu_speed_ops),
        "total": (propagation_delay(distance_m) + serialization_delay(packet_size_bytes, link_rate_bps)
                  + (queuing_delay(packet_size_bytes, queue_depth, link_rate_bps) if queue_depth > 0 else 0.0)
                  + processing_delay(packet_size_bytes, 100.0, cpu_speed_ops)),
    }


@dataclass
class LatencyProfile:
    distance_m: float
    packet_size_bytes: int = 1500
    link_rate_bps: float = 100e6
    queue_depth: int = 0
    cpu_speed_ops: float = 1e9
    components: dict = field(default_factory=dict)

    def compute(self) -> dict:
        self.components = total_latency_component(
            self.distance_m, self.packet_size_bytes,
            self.link_rate_bps, self.queue_depth, self.cpu_speed_ops,
        )
        return self.components


class LatencySimulator:
    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)

    def simulate_packet_stream(self, profile: LatencyProfile, num_packets: int,
                                jitter_variance: float = 0.0) -> List[dict]:
        results = []
        for i in range(num_packets):
            base = profile.compute()
            if jitter_variance > 0:
                jitter = jitter_model(0.0, jitter_variance, "normal")
                base["total"] += jitter
                base["jitter"] = jitter
            base["packet_id"] = i
            results.append(base)
        return results

    def compute_statistics(self, delays: List[float]) -> dict:
        arr = np.array(delays)
        return {
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
            "mean": float(np.mean(arr)),
            "median": float(np.median(arr)),
            "std": float(np.std(arr)),
            "p99": float(np.percentile(arr, 99)),
            "p95": float(np.percentile(arr, 95)),
        }
