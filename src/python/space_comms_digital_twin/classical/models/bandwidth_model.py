from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional


def shannon_capacity(bandwidth_hz: float, snr: float) -> float:
    return bandwidth_hz * math.log2(1.0 + snr)


def spectral_efficiency(capacity_bps: float, bandwidth_hz: float) -> float:
    if bandwidth_hz <= 0:
        return 0.0
    return capacity_bps / bandwidth_hz


def adaptive_modulation_thresholds(snr_values: List[float]) -> Dict[str, float]:
    thresholds = {
        "BPSK": 3.0,
        "QPSK": 6.0,
        "8PSK": 10.0,
        "16QAM": 14.0,
        "64QAM": 18.5,
    }
    return thresholds


def coding_overhead(code_rate: float, interleaving: bool = False) -> float:
    overhead = 1.0 / code_rate - 1.0
    if interleaving:
        overhead *= 1.1
    return overhead


def contention_model(num_users: int, traffic_intensity: float) -> float:
    if traffic_intensity >= 1.0:
        return 1.0
    return 1.0 - (1.0 - traffic_intensity) ** (num_users - 1)


def fairness_index(allocations: List[float]) -> float:
    n = len(allocations)
    if n == 0:
        return 0.0
    sum_alloc = sum(allocations)
    sum_sq = sum(a ** 2 for a in allocations)
    if sum_sq == 0:
        return 0.0
    return (sum_alloc ** 2) / (n * sum_sq)


def compute_available_bandwidth(total_capacity: float, overhead: float, contention: float) -> float:
    return total_capacity * (1.0 - overhead) * (1.0 - contention)


@dataclass
class QoSClass:
    name: str
    priority: int
    min_bandwidth_bps: float
    max_delay_ms: float
    packet_loss_rate: float


class BandwidthAllocator:
    def __init__(self, total_capacity_bps: float):
        self.total_capacity = total_capacity_bps

    def proportional_fair(self, demands: Dict[str, float]) -> Dict[str, float]:
        total_demand = sum(demands.values())
        if total_demand <= self.total_capacity:
            return dict(demands)
        scale = self.total_capacity / total_demand
        return {k: v * scale for k, v in demands.items()}

    def max_min_fair(self, demands: Dict[str, float]) -> Dict[str, float]:
        n = len(demands)
        remaining = self.total_capacity
        active = set(demands.keys())
        allocations = {k: 0.0 for k in demands}

        while active and remaining > 0:
            fair_share = remaining / len(active)
            saturated = set()
            for user in active:
                if demands[user] <= fair_share:
                    allocations[user] = demands[user]
                    remaining -= demands[user]
                    saturated.add(user)
            if not saturated:
                for user in active:
                    allocations[user] = fair_share
                    remaining -= fair_share
                break
            active -= saturated

        return allocations

    def water_filling(self, demands: Dict[str, float], weights: Optional[Dict[str, float]] = None) -> Dict[str, float]:
        if weights is None:
            weights = {k: 1.0 for k in demands}

        total_weight = sum(weights.values())
        allocated = {}
        remaining = self.total_capacity

        sorted_users = sorted(demands.keys(), key=lambda k: weights[k], reverse=True)
        for user in sorted_users:
            share = self.total_capacity * weights[user] / total_weight
            allocated[user] = min(demands[user], share)
            remaining -= allocated[user]

        if remaining > 0:
            deficit_users = [u for u in demands if allocated[u] < demands[u]]
            if deficit_users:
                extra = remaining / len(deficit_users)
                for user in deficit_users:
                    allocated[user] += extra

        return allocated

    def demand_based(self, demands: Dict[str, float], sla_weights: Optional[Dict[str, float]] = None) -> Dict[str, float]:
        return self.proportional_fair(demands)
