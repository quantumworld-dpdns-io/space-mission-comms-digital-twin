from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


class ReportGenerator:
    def generate_simulation_report(self, results: list[dict[str, Any]]) -> str:
        return f"Simulation Report - {datetime.now(UTC).isoformat()}\n" + \
               f"Results: {len(results)} simulations\n"

    def generate_quantum_report(self, result: dict[str, Any]) -> str:
        return f"Quantum Report\nBackend: {result.get('backend', 'N/A')}\n"

    def generate_comparison_report(self, classical: dict, quantum: dict) -> str:
        return f"Comparison Report\nClassical: {classical}\nQuantum: {quantum}\n"
