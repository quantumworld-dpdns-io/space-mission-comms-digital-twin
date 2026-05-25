from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from space_comms_digital_twin.classical.models.link_budget import (
    LinkBudgetCalculator,
    LinkBudgetParams,
)
from space_comms_digital_twin.classical.models.satellite import Satellite
from space_comms_digital_twin.classical.simulation.visibility_engine import contact_window


@dataclass
class SimulationJob:
    id: str = ""
    status: str = "pending"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class SimulationService:
    def __init__(self):
        self.jobs: Dict[str, SimulationJob] = {}

    def run_classical_simulation(self, params: Dict[str, Any]) -> SimulationJob:
        job_id = str(uuid.uuid4())
        job = SimulationJob(id=job_id, status="running")
        self.jobs[job_id] = job

        try:
            lb_calc = LinkBudgetCalculator()
            lb_params = LinkBudgetParams(
                tx_power_watts=params.get("tx_power", 10.0),
                tx_gain_dbi=params.get("tx_gain", 40.0),
                rx_gain_dbi=params.get("rx_gain", 30.0),
                frequency_ghz=params.get("frequency", 8.0),
                distance_m=params.get("distance", 1000000.0),
                bandwidth_hz=params.get("bandwidth", 100e6),
            )
            result = lb_calc.compute(lb_params)

            job.status = "completed"
            job.completed_at = datetime.now(timezone.utc)
            job.result = {
                "type": "link_budget",
                "snr_db": result.snr_db,
                "link_margin_db": result.link_margin_db,
                "eirp_dbw": result.eirp_dbw,
                "total_path_loss_db": result.total_path_loss_db,
            }
        except Exception as e:
            job.status = "failed"
            job.error = str(e)

        return job

    def get_simulation_status(self, job_id: str) -> Optional[SimulationJob]:
        return self.jobs.get(job_id)

    def get_simulation_result(self, job_id: str) -> Optional[Dict[str, Any]]:
        job = self.jobs.get(job_id)
        if job and job.status == "completed":
            return job.result
        return None

    def cancel_simulation(self, job_id: str) -> bool:
        job = self.jobs.get(job_id)
        if job and job.status == "running":
            job.status = "cancelled"
            return True
        return False

    def list_simulations(self) -> List[Dict[str, Any]]:
        return [
            {"id": j.id, "status": j.status, "created_at": j.created_at.isoformat()}
            for j in self.jobs.values()
        ]
