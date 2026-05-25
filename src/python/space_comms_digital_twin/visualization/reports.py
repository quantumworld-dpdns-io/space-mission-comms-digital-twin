from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List


class ReportGenerator:
    def generate_simulation_report(self, results: List[Dict[str, Any]]) -> str:
        return f"Simulation Report - {datetime.now(timezone.utc).isoformat()}\n" + \
               f"Results: {len(results)} simulations\n"

    def generate_quantum_report(self, result: Dict[str, Any]) -> str:
        return f"Quantum Report\nBackend: {result.get('backend', 'N/A')}\n"

    def generate_comparison_report(self, classical: Dict, quantum: Dict) -> str:
        return f"Comparison Report\nClassical: {classical}\nQuantum: {quantum}\n"
