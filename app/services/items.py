from typing import List, Optional

from app.core.exceptions import NotFoundError
from app.repositories import items as items_repository
from app.schemas.item import Item, ItemCreate, ItemUpdate


def list_items(min_strength: Optional[int] = None) -> List[Item]:
    return items_repository.list_items(min_strength=min_strength)


def get_item(item_id: int) -> Item:
    item = items_repository.get_item(item_id)
    if item is None:
        raise NotFoundError("Item not found")
    return item


def create_item(payload: ItemCreate) -> Item:
    return items_repository.create_item(payload)


def update_item(item_id: int, payload: ItemUpdate) -> Item:
    item = items_repository.update_item(item_id, payload)
    if item is None:
        raise NotFoundError("Item not found")
    return item


def delete_item(item_id: int) -> None:
    if not items_repository.delete_item(item_id):
        raise NotFoundError("Item not found")
