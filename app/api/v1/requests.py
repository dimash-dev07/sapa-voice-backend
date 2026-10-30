import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.request import RequestStatus, VoiceRequest
from app.schemas.request import RequestCreate, RequestList, RequestRead
from app.services.queue import enqueue_request

router = APIRouter(prefix="/requests", tags=["requests"])


@router.post("", response_model=RequestRead, status_code=status.HTTP_201_CREATED)
async def create_request(
    payload: RequestCreate,
    session: AsyncSession = Depends(get_session),
) -> VoiceRequest:
    req = VoiceRequest(client_phone=payload.client_phone, text=payload.text)
    session.add(req)
    await session.commit()
    await session.refresh(req)
    await enqueue_request(str(req.id))
    return req


@router.get("/{request_id}", response_model=RequestRead)
async def get_request(
    request_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> VoiceRequest:
    req = await session.get(VoiceRequest, request_id)
    if req is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return req


@router.get("", response_model=RequestList)
async def list_requests(
    status_filter: RequestStatus | None = Query(default=None, alias="status"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
) -> RequestList:
    stmt = select(VoiceRequest)
    count_stmt = select(func.count()).select_from(VoiceRequest)

    if status_filter is not None:
        stmt = stmt.where(VoiceRequest.status == status_filter)
        count_stmt = count_stmt.where(VoiceRequest.status == status_filter)

    stmt = stmt.order_by(VoiceRequest.created_at.desc()).limit(limit).offset(offset)

    items = (await session.scalars(stmt)).all()
    total = await session.scalar(count_stmt)

    return RequestList(total=total or 0, items=list(items))