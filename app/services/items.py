from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenError, NotFoundError
from app.repositories import items as items_repository
from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.schemas.user import User


def list_items(
    db: Session,
    min_strength: Optional[int] = None,
    q: Optional[str] = None,
    sort: str = "id",
    skip: int = 0,
    limit: int = 20,
) -> List[Item]:
    return items_repository.list_items(
        db,
        min_strength=min_strength,
        q=q,
        sort=sort,
        skip=skip,
        limit=limit,
    )


def get_item(db: Session, item_id: int) -> Item:
    item = items_repository.get_item(db, item_id)
    if item is None:
        raise NotFoundError("Item not found")
    return item


def create_item(db: Session, payload: ItemCreate, current_user: User) -> Item:
    return items_repository.create_item(db, payload, owner_id=current_user.id)


def update_item(
    db: Session,
    item_id: int,
    payload: ItemUpdate,
    current_user: User,
) -> Item:
    item = items_repository.get_item(db, item_id)
    if item is None:
        raise NotFoundError("Item not found")
    if item.owner_id != current_user.id:
        raise ForbiddenError("Not allowed to modify this item")
    updated = items_repository.update_item(db, item_id, payload)
    if updated is None:
        raise NotFoundError("Item not found")
    return updated


def delete_item(db: Session, item_id: int, current_user: User) -> None:
    item = items_repository.get_item(db, item_id)
    if item is None:
        raise NotFoundError("Item not found")
    if item.owner_id != current_user.id:
        raise ForbiddenError("Not allowed to delete this item")
    if not items_repository.delete_item(db, item_id):
        raise NotFoundError("Item not found")
