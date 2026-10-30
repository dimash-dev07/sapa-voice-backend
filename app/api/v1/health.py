from fastapi import APIRouter
from sqlalchemy import text

from app.core.database import SessionLocal
from app.core.redis_client import redis

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict:
    db_ok = redis_ok = False
    try:
        async with SessionLocal() as s:
            await s.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        pass
    try:
        await redis.ping()
        redis_ok = True
    except Exception:
        pass
    return {"status": "ok" if (db_ok and redis_ok) else "degraded", "db": db_ok, "redis": redis_ok}