from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class ScheduleTask:
    id: str
    satellite_id: str
    ground_station_id: str
    start_time: float
    end_time: float
    priority: int = 0
    bandwidth_required: float = 0.0
    assigned_antenna: Optional[str] = None


@dataclass
class ScheduleResult:
    tasks: List[ScheduleTask] = field(default_factory=list)
    unscheduled: List[ScheduleTask] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)


class AntennaScheduler:
    def __init__(self, antennas: List[Dict[str, Any]]):
        self.antennas = antennas

    def greedy_schedule(self, tasks: List[ScheduleTask]) -> ScheduleResult:
        sorted_tasks = sorted(tasks, key=lambda t: t.priority, reverse=True)
        result = ScheduleResult()
        antenna_schedule: Dict[str, List[Tuple[float, float]]] = {a["id"]: [] for a in self.antennas}

        for task in sorted_tasks:
            assigned = False
            for antenna in self.antennas:
                aid = antenna["id"]
                if self._is_available(aid, task.start_time, task.end_time, antenna_schedule):
                    antenna_schedule[aid].append((task.start_time, task.end_time))
                    task.assigned_antenna = aid
                    result.tasks.append(task)
                    assigned = True
                    break
            if not assigned:
                result.unscheduled.append(task)

        result.metrics = {
            "scheduled": len(result.tasks),
            "unscheduled": len(result.unscheduled),
            "utilization": self._utilization(antenna_schedule),
        }
        return result

    def window_based_schedule(self, tasks: List[ScheduleTask], windows: Dict[str, List[Tuple[float, float]]]) -> ScheduleResult:
        result = ScheduleResult()
        antenna_windows: Dict[str, List[Tuple[float, float, bool]]] = {
            a["id"]: [(w[0], w[1], False) for w in windows.get(a["id"], [])] for a in self.antennas
        }

        sorted_tasks = sorted(tasks, key=lambda t: t.priority, reverse=True)
        for task in sorted_tasks:
            assigned = False
            for antenna in self.antennas:
                aid = antenna["id"]
                for i, (ws, we, used) in enumerate(antenna_windows[aid]):
                    if used:
                        continue
                    if ws <= task.start_time and task.end_time <= we:
                        antenna_windows[aid][i] = (ws, we, True)
                        task.assigned_antenna = aid
                        result.tasks.append(task)
                        assigned = True
                        break
                if assigned:
                    break
            if not assigned:
                result.unscheduled.append(task)

        result.metrics = {"scheduled": len(result.tasks), "unscheduled": len(result.unscheduled)}
        return result

    def priority_schedule(self, tasks: List[ScheduleTask]) -> ScheduleResult:
        return self.greedy_schedule(tasks)

    def constraint_propagation(self, schedule: ScheduleResult, constraints: List[Dict]) -> ScheduleResult:
        violated = []
        valid = []
        for task in schedule.tasks:
            passes = True
            for constraint in constraints:
                if not self._check_constraint(task, constraint):
                    passes = False
                    break
            if passes:
                valid.append(task)
            else:
                violated.append(task)

        schedule.tasks = valid
        schedule.unscheduled.extend(violated)
        return schedule

    def conflict_resolution(self, conflicts: List[Tuple[ScheduleTask, ScheduleTask]], strategy: str = "priority") -> List[ScheduleTask]:
        resolved = []
        seen = set()
        for t1, t2 in conflicts:
            if t1.id in seen and t2.id in seen:
                continue
            if strategy == "priority":
                winner = t1 if t1.priority > t2.priority else t2
                resolved.append(winner)
                seen.add(winner.id)
            elif strategy == "first_come":
                winner = t1 if t1.start_time < t2.start_time else t2
                resolved.append(winner)
                seen.add(winner.id)
        return resolved

    def _is_available(self, antenna_id: str, start: float, end: float,
                      schedule: Dict[str, List[Tuple[float, float]]]) -> bool:
        for s, e in schedule.get(antenna_id, []):
            if not (end <= s or start >= e):
                return False
        return True

    def _utilization(self, schedule: Dict[str, List[Tuple[float, float]]]) -> float:
        total = 0.0
        for slots in schedule.values():
            for s, e in slots:
                total += e - s
        return total / max(len(self.antennas), 1) / 86400.0

    def _check_constraint(self, task: ScheduleTask, constraint: Dict) -> bool:
        ctype = constraint.get("type", "")
        if ctype == "max_duration":
            return (task.end_time - task.start_time) <= constraint.get("value", float('inf'))
        if ctype == "min_gap":
            return True
        return True
