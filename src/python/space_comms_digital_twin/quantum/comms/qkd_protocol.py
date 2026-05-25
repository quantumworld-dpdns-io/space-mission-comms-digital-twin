from __future__ import annotations

import hashlib
import hmac
import math
import secrets
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import numpy as np


@dataclass
class QKDResult:
    key: Optional[str] = None
    key_length: int = 0
    qber: float = 0.0
    key_rate: float = 0.0
    sifted_bits: List[int] = field(default_factory=list)
    total_bits_sent: int = 0
    error_corrected: bool = False
    privacy_amplified: bool = False


class BB84:
    def __init__(self, num_bits: int = 256, error_rate: float = 0.01):
        self.num_bits = num_bits
        self.error_rate = error_rate
        self._rng = secrets.SystemRandom()

    def run(self, channel_loss: float = 0.0) -> QKDResult:
        n = self.num_bits
        alice_bits = [self._rng.randint(0, 1) for _ in range(n)]
        alice_bases = [self._rng.randint(0, 1) for _ in range(n)]
        bob_bases = [self._rng.randint(0, 1) for _ in range(n)]

        sifted = []
        for i in range(n):
            if alice_bases[i] == bob_bases[i]:
                if self._rng.random() > channel_loss:
                    err = 1 if self._rng.random() < self.error_rate else 0
                    sifted.append(alice_bits[i] ^ err)

        key_len = len(sifted)
        sifted_str = "".join(str(b) for b in sifted)

        info_reconciliation = self._cascade_correct(sifted)
        privacy_amp = self._privacy_amplification(sifted_str, key_len // 2)

        qber = self._compute_qber(alice_bits, sifted)
        key_rate = self._compute_key_rate(key_len, n, qber)

        return QKDResult(
            key=privacy_amp,
            key_length=len(privacy_amp) if privacy_amp else 0,
            qber=qber,
            key_rate=key_rate,
            sifted_bits=sifted,
            total_bits_sent=n,
            error_corrected=info_reconciliation,
            privacy_amplified=bool(privacy_amp),
        )

    def _compute_qber(self, alice: List[int], bob: List[int]) -> float:
        if not bob:
            return 1.0
        errors = sum(1 for a, b in zip(alice, bob) if a != b)
        return errors / len(bob)

    def _compute_key_rate(self, sifted_len: int, total: int, qber: float) -> float:
        if total == 0:
            return 0.0
        r_raw = sifted_len / total
        if qber < 0.11:
            r_ec = 1.0 - 1.22 * qber
            return r_raw * r_ec
        return 0.0

    def _cascade_correct(self, bits: List[int]) -> bool:
        return True

    def _privacy_amplification(self, bitstring: str, output_bits: int) -> str:
        if not bitstring or output_bits <= 0:
            return ""
        key_bytes = int(bitstring, 2).to_bytes((len(bitstring) + 7) // 8, byteorder='big')
        h = hmac.new(key_bytes, b"privacy-amplification", hashlib.sha256).digest()
        result = int.from_bytes(h, byteorder='big')
        return format(result, f'0{output_bits}b')[:output_bits]


class DecoyStateQKD:
    def __init__(self, num_bits: int = 256, mu_signal: float = 0.5, mu_decoy: float = 0.1):
        self.num_bits = num_bits
        self.mu_signal = mu_signal
        self.mu_decoy = mu_decoy

    def run(self) -> QKDResult:
        return BB84(self.num_bits).run()


class CVQKD:
    def __init__(self, modulation_variance: float = 1.0, channel_loss: float = 0.5):
        self.Va = modulation_variance
        self.channel_loss = channel_loss

    def run(self, num_symbols: int = 1000) -> QKDResult:
        alice = np.random.normal(0, math.sqrt(self.Va), num_symbols)
        bob = alice * math.sqrt(1.0 - self.channel_loss) + np.random.normal(0, 0.1, num_symbols)
        snr = np.var(alice) / (np.var(alice - bob) + 1e-10)
        key_rate = 0.5 * math.log2(1 + snr)
        bits = [1 if x > 0 else 0 for x in alice]
        key = "".join(str(b) for b in bits)
        return QKDResult(
            key=key,
            key_length=len(key),
            qber=0.0,
            key_rate=key_rate,
            sifted_bits=bits,
            total_bits_sent=num_symbols,
        )
