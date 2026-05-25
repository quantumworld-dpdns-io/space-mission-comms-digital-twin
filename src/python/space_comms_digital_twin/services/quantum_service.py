from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from space_comms_digital_twin.quantum.comms.qkd_protocol import BB84, DecoyStateQKD, CVQKD
from space_comms_digital_twin.quantum.comms.teleportation import QuantumTeleportation
from space_comms_digital_twin.quantum.comms.error_correction import (
    RepetitionCode,
    ShorCode,
    SteaneCode,
    SurfaceCode,
)
from space_comms_digital_twin.quantum.simulation.hybrid_simulator import HybridSimulator


@dataclass
class QuantumJob:
    id: str = ""
    status: str = "pending"
    backend: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class QuantumService:
    def __init__(self):
        self.jobs: Dict[str, QuantumJob] = {}
        self.hybrid = HybridSimulator()

    def run_circuit(self, circuit: Dict[str, Any],
                    backend: str = "qiskit", shots: int = 1024) -> QuantumJob:
        job_id = str(uuid.uuid4())
        job = QuantumJob(id=job_id, status="running", backend=backend)
        self.jobs[job_id] = job

        try:
            if backend == "all":
                results = self.hybrid.run_on_all(circuit, shots=shots)
                job.result = {name: r.counts for name, r in results.items()}
            else:
                b = self.hybrid.get_backend(backend)
                if b is None:
                    raise ValueError(f"Backend not found: {backend}")
                result = b.run_circuit(circuit, shots=shots)
                job.result = {"counts": result.counts, "backend": backend}

            job.status = "completed"
        except Exception as e:
            job.status = "failed"
            job.error = str(e)

        return job

    def run_qkd(self, protocol: str = "BB84", num_bits: int = 256) -> QuantumJob:
        job_id = str(uuid.uuid4())
        job = QuantumJob(id=job_id, status="running", backend="classical")
        self.jobs[job_id] = job

        try:
            if protocol == "BB84":
                qkd = BB84(num_bits=num_bits)
            elif protocol == "decoy_state":
                qkd = DecoyStateQKD(num_bits=num_bits)
            elif protocol == "CVQKD":
                qkd = CVQKD()
            else:
                raise ValueError(f"Unknown protocol: {protocol}")

            result = qkd.run()
            job.result = {
                "key_length": result.key_length,
                "qber": result.qber,
                "key_rate": result.key_rate,
            }
            job.status = "completed"
        except Exception as e:
            job.status = "failed"
            job.error = str(e)

        return job

    def run_teleportation(self, noise_params: Optional[Dict[str, float]] = None) -> QuantumJob:
        job_id = str(uuid.uuid4())
        job = QuantumJob(id=job_id, status="running")
        self.jobs[job_id] = job

        try:
            tp = QuantumTeleportation(noise_model=noise_params)
            result = tp.run()
            job.result = {
                "success": result.success,
                "fidelity": result.fidelity,
            }
            job.status = "completed"
        except Exception as e:
            job.status = "failed"
            job.error = str(e)

        return job

    def list_backends(self) -> List[Dict[str, Any]]:
        return self.hybrid.list_backends()

    def get_job(self, job_id: str) -> Optional[QuantumJob]:
        return self.jobs.get(job_id)
