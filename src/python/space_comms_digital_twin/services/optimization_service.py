from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from space_comms_digital_twin.classical.optimization.antenna_scheduler import AntennaScheduler
from space_comms_digital_twin.classical.optimization.route_optimizer import RouteOptimizer
from space_comms_digital_twin.quantum.optimization.qaoa import QAOA
from space_comms_digital_twin.quantum.optimization.vqe import VQE


@dataclass
class OptimizationJob:
    id: str = ""
    status: str = "pending"
    algorithm: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class OptimizationService:
    def __init__(self):
        self.jobs: Dict[str, OptimizationJob] = {}

    def run_antenna_scheduling(self, tasks: List[Dict],
                                 antennas: List[Dict]) -> OptimizationJob:
        job_id = str(uuid.uuid4())
        job = OptimizationJob(id=job_id, status="running", algorithm="classical_antenna")
        self.jobs[job_id] = job

        try:
            scheduler = AntennaScheduler(antennas)
            schedule = scheduler.greedy_schedule(tasks)
            job.result = {
                "scheduled": len(schedule.tasks),
                "unscheduled": len(schedule.unscheduled),
                "metrics": schedule.metrics,
            }
            job.status = "completed"
        except Exception as e:
            job.status = "failed"
            job.error = str(e)

        return job

    def run_quantum_optimization(self, problem_type: str = "qaoa",
                                   n_qubits: int = 4) -> OptimizationJob:
        job_id = str(uuid.uuid4())
        job = OptimizationJob(id=job_id, status="running", algorithm=problem_type)
        self.jobs[job_id] = job

        try:
            if problem_type == "qaoa":
                optimizer = QAOA(n_layers=1)
                edges = [(0, 1), (0, 2), (1, 2)]
                H = optimizer.build_maxcut_hamiltonian(edges, n_qubits)
                result = optimizer.solve(H)
                job.result = {
                    "optimal_value": result.optimal_value,
                    "approximation_ratio": result.approximation_ratio,
                }
            elif problem_type == "vqe":
                optimizer = VQE(n_qubits=n_qubits)
                pauli_terms = [
                    ("ZZII", -1.0),
                    ("IIZZ", -1.0),
                    ("ZIZI", -0.5),
                ]
                H = optimizer.build_hamiltonian(pauli_terms)
                result = optimizer.solve(H)
                job.result = {
                    "optimal_energy": result.optimal_energy,
                    "n_iterations": result.n_iterations,
                }
            else:
                raise ValueError(f"Unknown problem type: {problem_type}")

            job.status = "completed"
        except Exception as e:
            job.status = "failed"
            job.error = str(e)

        return job

    def run_route_optimization(self, graph: Dict[str, Dict[str, float]],
                                 source: str, target: str) -> OptimizationJob:
        job_id = str(uuid.uuid4())
        job = OptimizationJob(id=job_id, status="running", algorithm="classical_route")
        self.jobs[job_id] = job

        try:
            optimizer = RouteOptimizer(graph)
            path, cost = optimizer.dijkstra_shortest_path(source, target)
            job.result = {
                "path": path,
                "cost": cost,
                "algorithm": "dijkstra",
            }
            job.status = "completed"
        except Exception as e:
            job.status = "failed"
            job.error = str(e)

        return job

    def get_job(self, job_id: str) -> Optional[OptimizationJob]:
        return self.jobs.get(job_id)

    def list_jobs(self) -> List[Dict[str, Any]]:
        return [
            {"id": j.id, "status": j.status, "algorithm": j.algorithm}
            for j in self.jobs.values()
        ]
