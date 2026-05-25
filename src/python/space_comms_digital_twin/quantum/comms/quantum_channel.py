from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import Any

import numpy as np
from numpy.typing import NDArray


class QuantumChannel(ABC):
    @abstractmethod
    def apply(self, state: Any) -> Any: ...

    @abstractmethod
    def channel_matrix(self) -> NDArray: ...

    @abstractmethod
    def capacity(self) -> float: ...

    @abstractmethod
    def name(self) -> str: ...


class PureLossChannel(QuantumChannel):
    def __init__(self, transmissivity: float = 0.5):
        self.eta = transmissivity

    def apply(self, state: Any) -> Any:
        return state * self.eta

    def channel_matrix(self) -> NDArray:
        return np.array([[self.eta, 0], [0, self.eta]])

    def capacity(self) -> float:
        eta = max(self.eta, 1e-10)
        return math.log2(1.0 + eta / (1.0 - eta))

    def name(self) -> str:
        return f"PureLoss(eta={self.eta})"


class DepolarizingChannel(QuantumChannel):
    def __init__(self, p: float = 0.1):
        self.p = min(max(p, 0.0), 1.0)

    def apply(self, state: Any) -> Any:
        return (1.0 - self.p) * state + self.p * np.eye(2) / 2.0

    def channel_matrix(self) -> NDArray:
        p = self.p
        return np.array([[1 - p/2, 0, 0, p/2],
                         [0, 1-p, 0, 0],
                         [0, 0, 1-p, 0],
                         [p/2, 0, 0, 1-p/2]])

    def capacity(self) -> float:
        p = self.p
        if p >= 0.75:
            return 0.0
        return 1.0 + (1.0 - p) * math.log2(1.0 - p) + p * math.log2(p / 3.0)

    def name(self) -> str:
        return f"Depolarizing(p={self.p})"


class AmplitudeDampingChannel(QuantumChannel):
    def __init__(self, gamma: float = 0.1):
        self.gamma = min(max(gamma, 0.0), 1.0)

    def apply(self, state: Any) -> Any:
        gamma = self.gamma
        K0 = np.array([[1.0, 0.0], [0.0, math.sqrt(1.0 - gamma)]])
        K1 = np.array([[0.0, math.sqrt(gamma)], [0.0, 0.0]])
        return K0 @ state @ K0.T + K1 @ state @ K1.T

    def channel_matrix(self) -> NDArray:
        return np.array([[1, 0, 0, math.sqrt(self.gamma)],
                         [0, math.sqrt(1-self.gamma), 0, 0],
                         [0, 0, math.sqrt(1-self.gamma), 0],
                         [0, 0, 0, 1-self.gamma]])

    def capacity(self) -> float:
        return 1.0 - self.gamma

    def name(self) -> str:
        return f"AmplitudeDamping(gamma={self.gamma})"


class PhaseDampingChannel(QuantumChannel):
    def __init__(self, lambd: float = 0.1):
        self.lambd = min(max(lambd, 0.0), 1.0)

    def apply(self, state: Any) -> Any:
        lambd = self.lambd
        K0 = np.array([[1.0, 0.0], [0.0, math.sqrt(1.0 - lambd)]])
        K1 = np.array([[0.0, 0.0], [0.0, math.sqrt(lambd)]])
        return K0 @ state @ K0.T + K1 @ state @ K1.T

    def channel_matrix(self) -> NDArray:
        lambd = self.lambd
        return np.array([[1, 0, 0, 0],
                         [0, math.sqrt(1-lambd), 0, 0],
                         [0, 0, math.sqrt(1-lambd), 0],
                         [0, 0, 0, 1-lambd]])

    def capacity(self) -> float:
        return 1.0 - self.lambd / 2.0

    def name(self) -> str:
        return f"PhaseDamping(lambda={self.lambd})"


class QuantumChannelFactory:
    @staticmethod
    def create(channel_type: str, **params: float) -> QuantumChannel:
        mapping = {
            "pure_loss": PureLossChannel,
            "depolarizing": DepolarizingChannel,
            "amplitude_damping": AmplitudeDampingChannel,
            "phase_damping": PhaseDampingChannel,
        }
        cls = mapping.get(channel_type.lower())
        if cls is None:
            raise ValueError(f"Unknown channel type: {channel_type}")
        return cls(**params)
