from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass
class EntanglementResult:
    fidelity: float = 0.0
    num_bell_pairs: int = 0
    success_rate: float = 0.0
    ebit_rate: float = 0.0
    distance_km: float = 0.0
    decoherence_time_ms: float = 0.0


class EntanglementDistributor:
    def __init__(self, fiber_loss_db_per_km: float = 0.2, detector_efficiency: float = 0.8):
        self.fiber_loss = fiber_loss_db_per_km
        self.detector_eff = detector_efficiency

    def distribute_bipartite(self, distance_km: float, num_pairs: int = 100,
                             memory_coherence_ms: float = 100.0) -> EntanglementResult:
        transmissivity = 10.0 ** (-self.fiber_loss * distance_km / 10.0)
        success_prob = transmissivity * self.detector_eff

        num_success = np.random.binomial(num_pairs, success_prob)
        if num_success > 0:
            decoherence_factor = math.exp(-distance_km * 3.34 / memory_coherence_ms)
            fidelity = 0.5 * (1.0 + decoherence_factor)
        else:
            fidelity = 0.0

        return EntanglementResult(
            fidelity=fidelity,
            num_bell_pairs=num_success,
            success_rate=success_prob * 100,
            ebit_rate=success_prob * 1e6,
            distance_km=distance_km,
            decoherence_time_ms=memory_coherence_ms,
        )

    def distribute_ghz(self, num_parties: int = 3, distance_km: float = 10.0) -> EntanglementResult:
        transmissivity = 10.0 ** (-self.fiber_loss * distance_km / 10.0)
        success_prob = transmissivity ** (num_parties - 1) * self.detector_eff ** num_parties
        return EntanglementResult(
            fidelity=0.9,
            num_bell_pairs=1,
            success_rate=success_prob * 100,
            ebit_rate=success_prob * 1e6,
            distance_km=distance_km,
        )

    def entanglement_swapping(self, distance_km: float,
                              segments: int = 2) -> EntanglementResult:
        per_segment = self.distribute_bipartite(distance_km / segments)
        purity_product = per_segment.fidelity ** segments
        swap_fidelity = purity_product * (1.0 + purity_product) / 2.0
        return EntanglementResult(
            fidelity=swap_fidelity,
            num_bell_pairs=per_segment.num_bell_pairs,
            success_rate=per_segment.success_rate ** segments,
            distance_km=distance_km,
        )

    def entanglement_purification(self, pairs: list[tuple[Any, Any]],
                                  protocol: str = "DEJMPS") -> EntanglementResult:
        if not pairs:
            return EntanglementResult()
        avg_fidelity = 0.9
        purified_fidelity = avg_fidelity * (avg_fidelity + 1.0) / 2.0
        num_surviving = max(len(pairs) // 2, 1)
        return EntanglementResult(
            fidelity=purified_fidelity,
            num_bell_pairs=num_surviving,
            success_rate=num_surviving / len(pairs) * 100,
        )
