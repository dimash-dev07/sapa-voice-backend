import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.deps import get_current_user, require_role
from app.models.client import Client
from app.models.user import User, UserRole
from app.schemas.client import ClientCreate, ClientList, ClientRead, ClientUpdate

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("", response_model=ClientRead, status_code=status.HTTP_201_CREATED)
async def create_client(
    payload: ClientCreate,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(get_current_user),
) -> Client:
    client = Client(**payload.model_dump())
    session.add(client)
    await session.commit()
    await session.refresh(client)
    return client


@router.get("", response_model=ClientList)
async def list_clients(
    q: str | None = Query(default=None, description="Іздеу: аты, телефон, email"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
    _: User = Depends(get_current_user),
) -> ClientList:
    stmt = select(Client)
    count_stmt = select(func.count()).select_from(Client)

    if q:
        pattern = f"%{q}%"
        cond = or_(
            Client.full_name.ilike(pattern),
            Client.phone.ilike(pattern),
            Client.email.ilike(pattern),
        )
        stmt = stmt.where(cond)
        count_stmt = count_stmt.where(cond)

    stmt = stmt.order_by(Client.created_at.desc()).limit(limit).offset(offset)
    items = (await session.scalars(stmt)).all()
    total = await session.scalar(count_stmt)
    return ClientList(total=total or 0, items=list(items))


@router.get("/{client_id}", response_model=ClientRead)
async def get_client(
    client_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(get_current_user),
) -> Client:
    client = await session.get(Client, client_id)
    if client is None:
        raise HTTPException(404, "Client not found")
    return client


@router.patch("/{client_id}", response_model=ClientRead)
async def update_client(
    client_id: uuid.UUID,
    payload: ClientUpdate,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(get_current_user),
) -> Client:
    client = await session.get(Client, client_id)
    if client is None:
        raise HTTPException(404, "Client not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(client, field, value)
    await session.commit()
    await session.refresh(client)
    return client


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(require_role(UserRole.ADMIN)),
) -> None:
    client = await session.get(Client, client_id)
    if client is None:
        raise HTTPException(404, "Client not found")
    await session.delete(client)
    await session.commit()