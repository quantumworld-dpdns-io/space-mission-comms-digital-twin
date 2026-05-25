from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from numpy.typing import NDArray


@dataclass
class QSVMResult:
    accuracy: float = 0.0
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0
    support_vectors: List[int] = field(default_factory=list)
    n_features: int = 0
    n_support_vectors: int = 0
    kernel_type: str = "quantum"


class QSVM:
    def __init__(self, kernel_type: str = "quantum", n_qubits: int = 4):
        self.kernel_type = kernel_type
        self.n_qubits = n_qubits
        self.support_vectors_: List = []
        self.support_labels_: List = []
        self.alphas_: NDArray = np.array([])
        self.b_: float = 0.0

    def _quantum_kernel(self, x1: NDArray, x2: NDArray) -> float:
        from scipy.spatial.distance import pdist, squareform
        diff = x1 - x2
        kernel_val = np.exp(-0.5 * np.dot(diff, diff))
        return float(kernel_val)

    def _kernel_matrix(self, X1: NDArray, X2: NDArray) -> NDArray:
        n1, n2 = len(X1), len(X2)
        K = np.zeros((n1, n2))
        for i in range(n1):
            for j in range(n2):
                K[i, j] = self._quantum_kernel(X1[i], X2[j])
        return K

    def fit(self, X: NDArray, y: NDArray, C: float = 1.0) -> QSVMResult:
        from scipy.optimize import minimize

        n = len(X)
        K = self._kernel_matrix(X, X)

        def objective(alphas: NDArray) -> float:
            return 0.5 * np.sum(alphas[:, None] * alphas[None, :] * y[:, None] * y[None, :] * K) - np.sum(alphas)

        constraints = [{"type": "eq", "fun": lambda a: np.dot(a, y)}]
        bounds = [(0, C) for _ in range(n)]
        initial = np.zeros(n)

        result = minimize(objective, initial, bounds=bounds, constraints=constraints,
                          method="SLSQP", options={"maxiter": 200, "ftol": 1e-6})

        alphas = result.x
        sv_idx = alphas > 1e-5
        self.support_vectors_ = [X[i] for i in range(n) if sv_idx[i]]
        self.support_labels_ = [y[i] for i in range(n) if sv_idx[i]]
        self.alphas_ = alphas[sv_idx]
        self.b_ = np.mean([y[i] - np.sum(alphas[sv_idx] * y[sv_idx] * K[sv_idx, i])
                           for i in range(n) if sv_idx[i]])

        predictions = self.predict(X)
        accuracy = np.mean(predictions == y)

        return QSVMResult(
            accuracy=float(accuracy),
            n_features=X.shape[1],
            n_support_vectors=len(self.support_vectors_),
            kernel_type=self.kernel_type,
        )

    def predict(self, X: NDArray) -> NDArray:
        if not self.support_vectors_:
            return np.zeros(len(X))
        sv = np.array(self.support_vectors_)
        sv_labels = np.array(self.support_labels_)
        K_test = self._kernel_matrix(X, sv)
        decision = K_test @ (self.alphas_ * sv_labels) + self.b_
        return np.sign(decision)

    def decision_function(self, X: NDArray) -> NDArray:
        if not self.support_vectors_:
            return np.zeros(len(X))
        sv = np.array(self.support_vectors_)
        sv_labels = np.array(self.support_labels_)
        K_test = self._kernel_matrix(X, sv)
        return K_test @ (self.alphas_ * sv_labels) + self.b_

    def score(self, X: NDArray, y: NDArray) -> float:
        predictions = self.predict(X)
        return float(np.mean(predictions == y))
