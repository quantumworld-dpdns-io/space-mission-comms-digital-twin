
SPEED_OF_LIGHT: float = 299792458.0

EARTH_RADIUS: float = 6371000.0
EARTH_MU: float = 3.986004418e14
EARTH_ROTATION_RATE: float = 7.2921159e-5

PLANCK_CONSTANT: float = 6.62607015e-34
BOLTZMANN_CONSTANT: float = 1.380649e-23

FREQUENCY_BANDS: dict[str, tuple[float, float]] = {
    "S": (2.0, 4.0),
    "C": (4.0, 8.0),
    "X": (8.0, 12.0),
    "Ku": (12.0, 18.0),
    "K": (18.0, 27.0),
    "Ka": (27.0, 40.0),
    "Q": (33.0, 50.0),
    "V": (40.0, 75.0),
    "W": (75.0, 110.0),
}

SIMULATION_DEFAULTS = {
    "time_step": 1.0,
    "duration": 86400.0,
    "max_range": 1e9,
    "min_elevation": 5.0,
    "default_shots": 1024,
    "max_qubits": 20,
}

ERROR_CODES = {
    "INVALID_INPUT": "ERR-001",
    "SIMULATION_FAILED": "ERR-002",
    "QUANTUM_BACKEND_ERROR": "ERR-003",
    "VISIBILITY_FAILED": "ERR-004",
    "NOT_FOUND": "ERR-404",
    "RATE_LIMITED": "ERR-429",
    "AUTH_FAILED": "ERR-401",
    "FORBIDDEN": "ERR-403",
}

CCSDS_HEADER_SIZE: int = 6
CFDP_MAX_PDU_SIZE: int = 65536
DEFAULT_MTU_SIZE: int = 1500

ORBIT_TYPES = ["LEO", "MEO", "GEO", "HEO", "SSO"]
POLARIZATION_TYPES = ["linear_h", "linear_v", "rhcp", "lhcp"]
MODULATION_TYPES = ["BPSK", "QPSK", "8PSK", "16QAM", "64QAM", "GMSK"]
CODING_TYPES = ["uncoded", "convolutional", "ldpc", "turbo", "reed_solomon"]

QUANTUM_GATE_SET = ["H", "X", "Y", "Z", "S", "T", "CNOT", "CZ", "SWAP", "TOFFOLI", "RX", "RY", "RZ", "CRX", "CRY", "CRZ"]

ERROR_CORRECTION_CODES = ["repetition_3", "repetition_5", "shor_9", "steane_7", "surface_d3", "surface_d5", "color_d3"]

QKD_PROTOCOLS = ["BB84", "E91", "decoy_state", "MDI_QKD", "TF_QKD", "CV_QKD"]

TEST_MARKERS = {
    "unit": "Unit tests for individual functions",
    "integration": "Integration tests across components",
    "quantum": "Tests requiring quantum SDKs",
    "security": "Security and OWASP tests",
    "slow": "Slow tests (>30s)",
    "benchmark": "Performance benchmarks",
    "gpu": "Tests requiring GPU acceleration",
}
