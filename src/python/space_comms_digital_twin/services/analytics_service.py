from __future__ import annotations

from typing import Any

import numpy as np


class AnalyticsService:
    def aggregate_simulation_results(self, results: list[dict[str, Any]]) -> dict[str, Any]:
        if not results:
            return {}
        snr_values = [r.get("snr_db", 0) for r in results if "snr_db" in r]
        margin_values = [r.get("link_margin_db", 0) for r in results if "link_margin_db" in r]
        return {
            "snr": {
                "min": float(np.min(snr_values)) if snr_values else 0,
                "max": float(np.max(snr_values)) if snr_values else 0,
                "avg": float(np.mean(snr_values)) if snr_values else 0,
            },
            "margin": {
                "min": float(np.min(margin_values)) if margin_values else 0,
                "avg": float(np.mean(margin_values)) if margin_values else 0,
            },
            "count": len(results),
        }

    def compare_classical_quantum(self, classical_result: dict,
                                   quantum_result: dict) -> dict[str, Any]:
        return {
            "classical_optimal": classical_result.get("optimal_value", 0),
            "quantum_optimal": quantum_result.get("optimal_value", 0),
            "quantum_approximation_ratio": quantum_result.get("approximation_ratio", 0),
            "improvement": (quantum_result.get("optimal_value", 0) -
                            classical_result.get("optimal_value", 0)),
        }

    def generate_report(self, data: dict[str, Any]) -> dict[str, Any]:
        return {
            "summary": self.aggregate_simulation_results(data.get("results", [])),
            "comparison": self.compare_classical_quantum(
                data.get("classical", {}),
                data.get("quantum", {}),
            ),
            "recommendations": self._generate_recommendations(data),
        }

    @staticmethod
    def _generate_recommendations(data: dict[str, Any]) -> list[str]:
        recs = []
        results = data.get("results", [])
        for r in results:
            if r.get("link_margin_db", 100) < 3:
                recs.append(f"Increase link margin for {r.get('id', 'unknown')}")
        return recs
