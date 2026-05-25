from __future__ import annotations

from typing import Any, Dict, List, Optional

import numpy as np

from space_comms_digital_twin.quantum.simulation.backend_interface import (
    BackendResult,
    QuantumBackend,
)


class QuTiPBackend(QuantumBackend):
    def name(self) -> str:
        return "qutip"

    def supports_simulation(self) -> bool:
        return True

    def max_qubits(self) -> int:
        return 12

    def gate_set(self) -> List[str]:
        return ["H", "X", "Y", "Z", "S", "T", "CNOT", "CZ", "SWAP", "RX", "RY", "RZ"]

    def run_circuit(self, circuit: Any, shots: int = 1024, **kwargs: Any) -> BackendResult:
        try:
            import qutip as qt
            n_qubits = circuit.get("qubits", 2)
            ops = circuit.get("operations", [])
            state = qt.basis(2 ** n_qubits, 0)
            for op in ops:
                gate = op.get("gate", "")
                targets = op.get("qubits", [0])
                if gate == "H":
                    state = qt.gates.hadamard_transform() * state
                elif gate == "X":
                    state = qt.sigmax() * state
                elif gate == "CNOT":
                    state = qt.gates.cnot(N=2, control=targets[0], target=targets[1]) * state
            probs = np.abs(state.full().flatten()) ** 2
            str_probs = {format(i, f'0{n_qubits}b'): float(p) for i, p in enumerate(probs)}
            return BackendResult(
                probabilities=str_probs,
                state_vector=state,
                shots=0,
                backend_name=self.name(),
                metadata={"solver": "qutip", "n_qubits": n_qubits},
            )
        except ImportError:
            raise ImportError("QuTiP not installed. Install with: pip install qutip")

    def get_noise_model(self) -> Optional[Any]:
        try:
            import qutip as qt
            return {"collapse_operators": [qt.sigmaz()], "T1": 1e3, "T2": 1e3}
        except ImportError:
            return None

    def run_master_equation(self, H: Any, psi0: Any, tlist: List[float],
                            c_ops: List[Any] = None, **kwargs: Any) -> Dict[str, Any]:
        try:
            import qutip as qt
            if c_ops is None:
                c_ops = []
            result = qt.mesolve(H, psi0, tlist, c_ops, [])
            return {
                "states": result.states,
                "times": tlist,
                "expectation_values": result.expect if hasattr(result, 'expect') else [],
            }
        except ImportError:
            raise ImportError("QuTiP not installed. Install with: pip install qutip")
