from __future__ import annotations

import html
import re
from typing import Any


def validate_satellite_id(norad_id: int) -> bool:
    if not isinstance(norad_id, int):
        return False
    return not (norad_id <= 0 or norad_id > 99999)


def validate_frequency(freq_ghz: float) -> bool:
    if not isinstance(freq_ghz, (int, float)):
        return False
    return not (freq_ghz <= 0.0 or freq_ghz > 1000.0)


def validate_orbit_elements(elements: dict[str, Any]) -> bool:
    required = {"inclination", "raan", "eccentricity", "arg_perigee", "mean_anomaly", "mean_motion"}
    if not all(k in elements for k in required):
        return False
    ecc = elements["eccentricity"]
    if not (0.0 <= ecc < 1.0):
        return False
    incl = elements["inclination"]
    return 0.0 <= incl <= 180.0


def validate_quantum_circuit(circuit: dict[str, Any]) -> bool:
    if "qubits" not in circuit or "operations" not in circuit:
        return False
    qubits = circuit.get("qubits", 0)
    if not isinstance(qubits, int) or qubits < 1 or qubits > 100:
        return False
    ops = circuit.get("operations", [])
    if not isinstance(ops, list):
        return False
    valid_gates = {"H", "X", "Y", "Z", "S", "T", "CNOT", "CZ", "SWAP",
                   "TOFFOLI", "RX", "RY", "RZ", "CRX", "CRY", "CRZ", "MEASURE"}
    return all(not ("gate" not in op or op["gate"] not in valid_gates) for op in ops)


def sanitize_input(value: str) -> str:
    return html.escape(value)


def validate_id_pattern(value: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9_-]{1,64}$", value))
