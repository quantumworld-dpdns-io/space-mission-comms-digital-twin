from fastapi import APIRouter

router = APIRouter()


@router.get("/metrics")
async def get_metrics():
    from space_comms_digital_twin.utils.metrics import MetricsCollector
    collector = MetricsCollector()
    return collector.snapshot()
