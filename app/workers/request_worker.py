"""
Redis кезегін тыңдайтын background worker.
Бөлек container ретінде іске қосылады.
"""
import asyncio
import logging

from app.core.database import SessionLocal
from app.models.request import RequestStatus, VoiceRequest
from app.services.processor import generate_response
from app.services.queue import dequeue_request

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("worker")


async def handle(request_id: str) -> None:
    async with SessionLocal() as session:
        req = await session.get(VoiceRequest, request_id)
        if req is None:
            log.warning("Request %s not found, skipping", request_id)
            return

        req.status = RequestStatus.PROCESSING
        await session.commit()

        try:
            await asyncio.sleep(0.5)
            req.response = generate_response(req.text)
            req.status = RequestStatus.PROCESSED
            log.info("Processed %s", request_id)
        except Exception as exc:
            req.status = RequestStatus.FAILED
            log.exception("Failed %s: %s", request_id, exc)

        await session.commit()


async def main() -> None:
    log.info("Worker started, waiting for requests...")
    while True:
        request_id = await dequeue_request()
        if request_id:
            await handle(request_id)


if __name__ == "__main__":
    asyncio.run(main())