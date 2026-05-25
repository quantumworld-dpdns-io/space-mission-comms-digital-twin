from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException

from space_comms_digital_twin.services.quantum_service import QuantumService

router = APIRouter()
service = QuantumService()


@router.post("/circuit")
async def submit_circuit(circuit: Dict[str, Any], backend: str = "qiskit", shots: int = 1024):
    job = service.run_circuit(circuit, backend=backend, shots=shots)
    return {"job_id": job.id, "status": job.status, "backend": backend}


@router.post("/qkd")
async def run_qkd(protocol: str = "BB84", num_bits: int = 256):
    job = service.run_qkd(protocol=protocol, num_bits=num_bits)
    return {"job_id": job.id, "status": job.status}


@router.post("/teleport")
async def run_teleportation(noise_params: Optional[Dict[str, float]] = None):
    job = service.run_teleportation(noise_params=noise_params)
    return {"job_id": job.id, "status": job.status, "fidelity": job.result.get("fidelity") if job.result else 0}


@router.get("/backends")
async def list_backends():
    return {"backends": service.list_backends()}


@router.get("/jobs/{job_id}")
async def get_quantum_job(job_id: str):
    job = service.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job.id, "status": job.status, "result": job.result}
