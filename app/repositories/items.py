from typing import Dict, List, Optional

from app.schemas.item import Item, ItemCreate, ItemUpdate

_items: Dict[int, Item] = {}
_next_id = 1


def reset() -> None:
    global _next_id
    _items.clear()
    _next_id = 1


def list_items(min_strength: Optional[int] = None) -> List[Item]:
    items = list(_items.values())
    if min_strength is not None:
        items = [item for item in items if item.strength >= min_strength]
    return items


def get_item(item_id: int) -> Optional[Item]:
    return _items.get(item_id)


def create_item(payload: ItemCreate) -> Item:
    global _next_id
    item = Item(id=_next_id, **payload.model_dump())
    _items[_next_id] = item
    _next_id += 1
    return item


def update_item(item_id: int, payload: ItemUpdate) -> Optional[Item]:
    if item_id not in _items:
        return None
    item = Item(id=item_id, **payload.model_dump())
    _items[item_id] = item
    return item


def delete_item(item_id: int) -> bool:
    return _items.pop(item_id, None) is not None
