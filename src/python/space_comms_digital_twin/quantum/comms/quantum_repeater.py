from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class RepeaterResult:
    end_to_end_fidelity: float = 0.0
    secret_key_rate: float = 0.0
    entanglement_rate_hz: float = 0.0
    num_segments: int = 0
    total_distance_km: float = 0.0
    per_segment_fidelity: float = 0.0
    required_memory_time_ms: float = 0.0


class QuantumRepeater:
    def __init__(self, fiber_loss_db_per_km: float = 0.2,
                 detector_efficiency: float = 0.8,
                 memory_coherence_ms: float = 100.0):
        self.fiber_loss = fiber_loss_db_per_km
        self.detector_eff = detector_efficiency
        self.memory_coherence = memory_coherence_ms

    def simulate_first_gen(self, total_distance_km: float,
                           segment_length_km: float = 20.0) -> RepeaterResult:
        num_segments = max(1, int(total_distance_km / segment_length_km))
        seg_dist = total_distance_km / num_segments
        transmissivity = 10.0 ** (-self.fiber_loss * seg_dist / 10.0)
        prob_per_seg = transmissivity * self.detector_eff

        p_success = prob_per_seg ** num_segments
        if p_success > 0:
            memory_time = 2.0 * seg_dist * 1e3 / (2e8)
            decoherence = math.exp(-memory_time / self.memory_coherence)
            fidelity = 0.5 * (1.0 + decoherence ** num_segments)
        else:
            fidelity = 0.0

        return RepeaterResult(
            end_to_end_fidelity=fidelity,
            secret_key_rate=-math.log2(1.0 - fidelity) if fidelity > 0.5 else 0.0,
            entanglement_rate_hz=prob_per_seg * 1e6 / num_segments,
            num_segments=num_segments,
            total_distance_km=total_distance_km,
            per_segment_fidelity=fidelity ** (1.0 / num_segments) if num_segments > 0 else 0.0,
            required_memory_time_ms=memory_time,
        )

    def simulate_second_gen(self, total_distance_km: float,
                            num_repeaters: int = 5) -> RepeaterResult:
        num_segments = num_repeaters + 1
        seg_dist = total_distance_km / num_segments
        transmissivity = 10.0 ** (-self.fiber_loss * seg_dist / 10.0)
        prob_per_seg = transmissivity * self.detector_eff

        memory_time = seg_dist * 1000.0 / (2e8 / 3)
        decoherence_factor = math.exp(-memory_time / self.memory_coherence)
        per_seg_fidelity = 0.5 * (1.0 + decoherence_factor)

        e2e_fidelity = 0.5 * (1.0 + decoherence_factor ** num_segments)

        rate = prob_per_seg * self.memory_coherence / (memory_time * 1000)
        key_rate = max(0, rate * (1.0 - 1.22 * (1.0 - e2e_fidelity)))

        return RepeaterResult(
            end_to_end_fidelity=e2e_fidelity,
            secret_key_rate=key_rate,
            entanglement_rate_hz=rate,
            num_segments=num_segments,
            total_distance_km=total_distance_km,
            per_segment_fidelity=per_seg_fidelity,
            required_memory_time_ms=memory_time,
        )

    def simulate_third_gen(self, total_distance_km: float,
                           code_distance: int = 3) -> RepeaterResult:
        seg_dist = total_distance_km / 3.0
        transmissivity = 10.0 ** (-self.fiber_loss * seg_dist / 10.0)
        raw_fidelity = 0.5 * (1.0 + transmissivity * self.detector_eff)

        logical_error = 0.1 * ((1 - raw_fidelity) / 0.01) ** ((code_distance + 1) / 2)
        e2e_fidelity = 1.0 - 3 * logical_error

        return RepeaterResult(
            end_to_end_fidelity=max(e2e_fidelity, 0.0),
            secret_key_rate=max(0, 1.0 - 1.22 * (1.0 - e2e_fidelity)),
            entanglement_rate_hz=1e6 * transmissivity ** 3,
            num_segments=3,
            total_distance_km=total_distance_km,
            per_segment_fidelity=raw_fidelity,
            required_memory_time_ms=0.1,
        )

    def optimal_spacing(self, total_distance_km: float) -> float:
        for seg in range(1, 101):
            d = total_distance_km / seg
            result = self.simulate_first_gen(total_distance_km, d)
            if result.end_to_end_fidelity > 0.5:
                return d
        return total_distance_km / 10.0
