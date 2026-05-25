from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from space_comms_digital_twin.services.optimization_service import OptimizationService

router = APIRouter()
service = OptimizationService()


@router.post("/antenna-schedule")
async def optimize_antenna_schedule(tasks: List[Dict], antennas: List[Dict]):
    job = service.run_antenna_scheduling(tasks, antennas)
    return {"job_id": job.id, "status": job.status, "result": job.result}


@router.post("/quantum")
async def run_quantum_optimization(problem_type: str = "qaoa", n_qubits: int = 4):
    job = service.run_quantum_optimization(problem_type=problem_type, n_qubits=n_qubits)
    return {"job_id": job.id, "status": job.status, "result": job.result}


@router.post("/route")
async def optimize_route(params: Dict[str, Any]):
    graph = params.get("graph", {})
    source = params.get("source", "")
    target = params.get("target", "")
    job = service.run_route_optimization(graph, source, target)
    return {"job_id": job.id, "status": job.status, "result": job.result}


@router.get("/jobs/{job_id}")
async def get_optimization_job(job_id: str):
    job = service.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job.id, "status": job.status, "result": job.result}


@router.get("/jobs")
async def list_optimization_jobs():
    return {"jobs": service.list_jobs()}
