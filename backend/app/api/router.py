from fastapi import APIRouter

from app.api.endpoints.apis import router as url_router
from app.api.endpoints.health import router as health_router

router = APIRouter()
router.include_router(health_router)
router.include_router(url_router)
