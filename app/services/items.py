from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.repositories import items as items_repository
from app.schemas.item import Item, ItemCreate, ItemUpdate


def list_items(db: Session, min_strength: Optional[int] = None) -> List[Item]:
    return items_repository.list_items(db, min_strength=min_strength)


def get_item(db: Session, item_id: int) -> Item:
    item = items_repository.get_item(db, item_id)
    if item is None:
        raise NotFoundError("Item not found")
    return item


def create_item(db: Session, payload: ItemCreate) -> Item:
    return items_repository.create_item(db, payload)


def update_item(db: Session, item_id: int, payload: ItemUpdate) -> Item:
    item = items_repository.update_item(db, item_id, payload)
    if item is None:
        raise NotFoundError("Item not found")
    return item


def delete_item(db: Session, item_id: int) -> None:
    if not items_repository.delete_item(db, item_id):
        raise NotFoundError("Item not found")
