from fastapi import APIRouter

from space_comms_digital_twin.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.app_version, "app": settings.app_name}


@router.get("/")
async def root():
    return {"message": f"{settings.app_name} v{settings.app_version}", "docs": "/docs"}
