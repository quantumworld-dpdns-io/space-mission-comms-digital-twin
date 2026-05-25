from __future__ import annotations

from typing import Dict, List, Optional

import numpy as np


class BandwidthAllocator:
    def __init__(self, total_capacity_bps: float):
        self.total_capacity = total_capacity_bps

    def proportional_fair_allocation(self, demands: Dict[str, float]) -> Dict[str, float]:
        total_demand = sum(demands.values())
        if total_demand <= self.total_capacity:
            return dict(demands)
        scale = self.total_capacity / total_demand
        return {k: v * scale for k, v in demands.items()}

    def max_min_fair_allocation(self, demands: Dict[str, float]) -> Dict[str, float]:
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

    def water_filling_allocation(self, demands: Dict[str, float], weights: Optional[Dict[str, float]] = None) -> Dict[str, float]:
        if weights is None:
            weights = {k: 1.0 for k in demands}
        total_weight = sum(weights.values())
        allocations = {}
        remaining = self.total_capacity
        sorted_users = sorted(demands.keys(), key=lambda k: weights[k], reverse=True)
        for user in sorted_users:
            share = self.total_capacity * weights[user] / total_weight
            allocations[user] = min(demands[user], share)
            remaining -= allocations[user]
        if remaining > 0:
            deficit = [u for u in demands if allocations[u] < demands[u]]
            if deficit:
                extra = remaining / len(deficit)
                for user in deficit:
                    allocations[user] += extra
        return allocations

    def demand_based_allocation(self, demands: Dict[str, float], sla_weights: Optional[Dict[str, float]] = None) -> Dict[str, float]:
        return self.proportional_fair_allocation(demands)

    def compute_fairness(self, allocations: List[float]) -> float:
        n = len(allocations)
        if n == 0:
            return 0.0
        total = sum(allocations)
        sum_sq = sum(a ** 2 for a in allocations)
        if sum_sq == 0:
            return 0.0
        return (total ** 2) / (n * sum_sq)

    def compute_efficiency(self, allocations: List[float]) -> float:
        return sum(allocations) / self.total_capacity if self.total_capacity > 0 else 0.0
