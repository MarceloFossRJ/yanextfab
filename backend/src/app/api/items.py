import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.models.item import Item
from app.models.user import User
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate
from app.users import current_active_user

router = APIRouter(prefix="/items", tags=["items"])


async def _get_owned_item(item_id: uuid.UUID, user: User, session: AsyncSession) -> Item:
    item = await session.get(Item, item_id)
    if item is None or item.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("", response_model=list[ItemRead])
async def list_items(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
) -> list[Item]:
    result = await session.execute(select(Item).where(Item.owner_id == user.id))
    return list(result.scalars().all())


@router.post("", response_model=ItemRead, status_code=201)
async def create_item(
    payload: ItemCreate,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
) -> Item:
    item = Item(owner_id=user.id, title=payload.title, description=payload.description)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


@router.get("/{item_id}", response_model=ItemRead)
async def get_item(
    item_id: uuid.UUID,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
) -> Item:
    return await _get_owned_item(item_id, user, session)


@router.patch("/{item_id}", response_model=ItemRead)
async def update_item(
    item_id: uuid.UUID,
    payload: ItemUpdate,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
) -> Item:
    item = await _get_owned_item(item_id, user, session)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    await session.commit()
    await session.refresh(item)
    return item


@router.delete("/{item_id}", status_code=204)
async def delete_item(
    item_id: uuid.UUID,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
) -> None:
    item = await _get_owned_item(item_id, user, session)
    await session.delete(item)
    await session.commit()
