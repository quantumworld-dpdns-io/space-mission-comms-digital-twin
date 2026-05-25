from pathlib import Path

QASM_DIR = Path(__file__).parent

CIRCUIT_REGISTRY: dict[str, str] = {}


def load_circuit(name: str) -> str:
    if not CIRCUIT_REGISTRY:
        _load_all()
    return CIRCUIT_REGISTRY[name]


def _load_all() -> None:
    for qasm_file in QASM_DIR.glob("*.qasm"):
        CIRCUIT_REGISTRY[qasm_file.stem] = qasm_file.read_text()


def list_circuits() -> list[str]:
    if not CIRCUIT_REGISTRY:
        _load_all()
    return list(CIRCUIT_REGISTRY.keys())
