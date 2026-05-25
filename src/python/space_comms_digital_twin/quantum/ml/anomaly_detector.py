from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray

from space_comms_digital_twin.quantum.ml.qsvm import QSVM


@dataclass
class AnomalyResult:
    n_anomalies: int = 0
    anomaly_scores: list[float] = field(default_factory=list)
    anomaly_indices: list[int] = field(default_factory=list)
    threshold: float = 0.0
    precision: float = 0.0
    recall: float = 0.0


class QuantumAnomalyDetector:
    def __init__(self, kernel: str = "quantum", n_qubits: int = 4, nu: float = 0.1):
        self.kernel = kernel
        self.n_qubits = n_qubits
        self.nu = nu
        self.qsvm = QSVM(kernel_type=kernel, n_qubits=n_qubits)
        self.rho_: float = 0.0

    def _encode_telemetry(self, telemetry: NDArray) -> NDArray:
        features = []
        for sample in telemetry:
            encoded = []
            for _i, val in enumerate(sample):
                angle = np.arctan(val) / (np.pi / 2)
                encoded.append(angle)
            features.append(encoded)
        return np.array(features)

    def fit(self, X: NDArray) -> AnomalyResult:
        encoded = self._encode_telemetry(X)
        y = np.ones(len(encoded))
        self.qsvm.fit(encoded, y, C=1.0 / self.nu)
        scores = self.qsvm.decision_function(encoded)
        self.rho_ = np.percentile(scores, int(self.nu * 100))
        return AnomalyResult(
            n_anomalies=0,
            anomaly_scores=list(scores),
            anomaly_indices=[],
            threshold=float(self.rho_),
        )

    def predict(self, X: NDArray) -> NDArray:
        encoded = self._encode_telemetry(X)
        scores = self.qsvm.decision_function(encoded)
        scores = np.nan_to_num(scores, nan=0.0)
        return (scores < self.rho_).astype(int)

    def detect(self, X: NDArray) -> AnomalyResult:
        predictions = self.predict(X)
        anomaly_idx = [int(i) for i in range(len(predictions)) if predictions[i] == 1]
        encoded = self._encode_telemetry(X)
        scores = np.nan_to_num(self.qsvm.decision_function(encoded), nan=0.0)
        return AnomalyResult(
            n_anomalies=len(anomaly_idx),
            anomaly_scores=list(scores),
            anomaly_indices=anomaly_idx,
            threshold=float(np.nan_to_num(self.rho_, nan=0.0)),
        )

    def compute_threshold(self, X: NDArray, contamination: float = 0.1) -> float:
        encoded = self._encode_telemetry(X)
        scores = self.qsvm.decision_function(encoded)
        scores = scores[~np.isnan(scores)]
        if len(scores) == 0:
            return 0.0
        return float(np.percentile(scores, max(1, int(contamination * 100))))
