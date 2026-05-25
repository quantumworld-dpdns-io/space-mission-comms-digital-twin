from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


@dataclass
class ErrorCorrectionResult:
    logical_error_rate: float = 0.0
    physical_error_rate: float = 0.0
    code_distance: int = 3
    num_physical_qubits: int = 0
    syndrome: List[int] = field(default_factory=list)
    correction_applied: bool = False
    success: bool = False


class QuantumErrorCorrectionCode(ABC):
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def encode(self, logical_state: Any) -> Any: ...

    @abstractmethod
    def syndrome_measurement(self, encoded_state: Any) -> List[int]: ...

    @abstractmethod
    def correct(self, encoded_state: Any, syndrome: List[int]) -> Any: ...

    @abstractmethod
    def logical_error_rate(self, physical_error_rate: float) -> float: ...


class RepetitionCode(QuantumErrorCorrectionCode):
    def __init__(self, distance: int = 3):
        self.d = distance

    def name(self) -> str:
        return f"RepetitionCode(d={self.d})"

    def encode(self, logical_state: Any) -> Any:
        return logical_state

    def syndrome_measurement(self, encoded_state: Any) -> List[int]:
        return [0] * (self.d - 1)

    def correct(self, encoded_state: Any, syndrome: List[int]) -> Any:
        return encoded_state

    def logical_error_rate(self, physical_error_rate: float) -> float:
        p = physical_error_rate
        n = self.d
        rate = 0.0
        for i in range((n + 1) // 2, n + 1):
            rate += math.comb(n, i) * (p ** i) * ((1 - p) ** (n - i))
        return rate

    def threshold(self) -> float:
        return 0.5


class ShorCode(QuantumErrorCorrectionCode):
    def name(self) -> str:
        return "ShorCode(9,1,3)"

    def encode(self, logical_state: Any) -> Any:
        return logical_state

    def syndrome_measurement(self, encoded_state: Any) -> List[int]:
        return [0] * 8

    def correct(self, encoded_state: Any, syndrome: List[int]) -> Any:
        return encoded_state

    def logical_error_rate(self, physical_error_rate: float) -> float:
        p = physical_error_rate
        return 3 * p ** 2 - 2 * p ** 3

    def threshold(self) -> float:
        return 0.333


class SteaneCode(QuantumErrorCorrectionCode):
    def name(self) -> str:
        return "SteaneCode(7,1,3)"

    def encode(self, logical_state: Any) -> Any:
        return logical_state

    def syndrome_measurement(self, encoded_state: Any) -> List[int]:
        return [0] * 6

    def correct(self, encoded_state: Any, syndrome: List[int]) -> Any:
        return encoded_state

    def logical_error_rate(self, physical_error_rate: float) -> float:
        p = physical_error_rate
        return 7 * p ** 2 - 6 * p ** 3

    def threshold(self) -> float:
        return 0.1428


class SurfaceCode(QuantumErrorCorrectionCode):
    def __init__(self, distance: int = 3):
        self.d = distance

    def name(self) -> str:
        return f"SurfaceCode(d={self.d})"

    def encode(self, logical_state: Any) -> Any:
        return logical_state

    def syndrome_measurement(self, encoded_state: Any) -> List[int]:
        return [0] * (self.d ** 2 - 1)

    def correct(self, encoded_state: Any, syndrome: List[int]) -> Any:
        return encoded_state

    def logical_error_rate(self, physical_error_rate: float) -> float:
        p = physical_error_rate
        d = self.d
        return 0.1 * (p / 0.01) ** ((d + 1) / 2)

    def threshold(self) -> float:
        return 0.01


def get_error_correction_code(name: str, distance: int = 3) -> QuantumErrorCorrectionCode:
    code_map = {
        "repetition_3": RepetitionCode(3),
        "repetition_5": RepetitionCode(5),
        "shor_9": ShorCode(),
        "steane_7": SteaneCode(),
        f"surface_d{distance}": SurfaceCode(distance),
    }
    code = code_map.get(name)
    if code is None:
        raise ValueError(f"Unknown error correction code: {name}")
    return code
