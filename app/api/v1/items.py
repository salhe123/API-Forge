from typing import List, Optional

from fastapi import APIRouter, Query, status

from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.services import items as items_service

router = APIRouter()


@router.get("/", response_model=List[Item])
def list_items(
    min_strength: Optional[int] = Query(default=None, ge=1, le=100),
) -> List[Item]:
    return items_service.list_items(min_strength=min_strength)


@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    return items_service.get_item(item_id)


@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate) -> Item:
    return items_service.create_item(payload)


@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, payload: ItemUpdate) -> Item:
    return items_service.update_item(item_id, payload)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int) -> None:
    items_service.delete_item(item_id)
