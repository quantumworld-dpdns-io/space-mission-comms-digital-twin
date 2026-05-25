from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException

from space_comms_digital_twin.services.simulation_service import SimulationService

router = APIRouter()
service = SimulationService()


@router.post("/run")
async def run_simulation(params: Dict[str, Any]):
    job = service.run_classical_simulation(params)
    return {"job_id": job.id, "status": job.status}


@router.get("/status/{job_id}")
async def get_simulation_status(job_id: str):
    job = service.get_simulation_status(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job.id, "status": job.status, "created_at": job.created_at.isoformat()}


@router.get("/result/{job_id}")
async def get_simulation_result(job_id: str):
    result = service.get_simulation_result(job_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Result not found")
    return result


@router.post("/cancel/{job_id}")
async def cancel_simulation(job_id: str):
    success = service.cancel_simulation(job_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found or already completed")
    return {"status": "cancelled"}


@router.get("/history")
async def list_simulations():
    return {"simulations": service.list_simulations()}
