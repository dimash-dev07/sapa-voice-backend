from app.core.config import settings
from app.core.redis_client import redis


async def enqueue_request(request_id: str) -> None:
    """Сұраныс ID-ін Redis кезегіне қосады."""
    await redis.lpush(settings.queue_name, request_id)


async def dequeue_request() -> str | None:
    """Кезектен келесі сұранысты алады."""
    result = await redis.brpop(settings.queue_name, timeout=settings.worker_poll_timeout)
    if result is None:
        return None
    _, request_id = result
    return request_id