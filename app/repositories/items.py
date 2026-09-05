from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.item import ItemModel
from app.schemas.item import Item, ItemCreate, ItemUpdate


def _to_schema(row: ItemModel) -> Item:
    return Item.model_validate(row)


def list_items(db: Session, min_strength: Optional[int] = None) -> List[Item]:
    statement = select(ItemModel).order_by(ItemModel.id)
    if min_strength is not None:
        statement = statement.where(ItemModel.strength >= min_strength)
    return [_to_schema(row) for row in db.scalars(statement).all()]


def get_item(db: Session, item_id: int) -> Optional[Item]:
    row = db.get(ItemModel, item_id)
    if row is None:
        return None
    return _to_schema(row)


def create_item(db: Session, payload: ItemCreate, owner_id: int) -> Item:
    row = ItemModel(**payload.model_dump(), owner_id=owner_id)
    db.add(row)
    db.commit()
    db.refresh(row)
    return _to_schema(row)


def update_item(db: Session, item_id: int, payload: ItemUpdate) -> Optional[Item]:
    row = db.get(ItemModel, item_id)
    if row is None:
        return None
    for field, value in payload.model_dump().items():
        setattr(row, field, value)
    db.commit()
    db.refresh(row)
    return _to_schema(row)


def delete_item(db: Session, item_id: int) -> bool:
    row = db.get(ItemModel, item_id)
    if row is None:
        return False
    db.delete(row)
    db.commit()
    return True
