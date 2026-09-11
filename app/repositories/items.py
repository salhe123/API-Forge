from typing import List, Optional, Union

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.models.item import ItemModel
from app.schemas.item import Item, ItemCreate, ItemPatch, ItemUpdate

_SORT_COLUMNS = {
    "id": ItemModel.id,
    "strength": ItemModel.strength,
}


def _to_schema(row: ItemModel) -> Item:
    return Item.model_validate(row)


def _apply_item_filters(
    statement: Select,
    min_strength: Optional[int] = None,
    max_strength: Optional[int] = None,
    q: Optional[str] = None,
    owner_id: Optional[int] = None,
) -> Select:
    if min_strength is not None:
        statement = statement.where(ItemModel.strength >= min_strength)
    if max_strength is not None:
        statement = statement.where(ItemModel.strength <= max_strength)
    if q:
        statement = statement.where(ItemModel.name.ilike("%{0}%".format(q)))
    if owner_id is not None:
        statement = statement.where(ItemModel.owner_id == owner_id)
    return statement


def list_items(
    db: Session,
    min_strength: Optional[int] = None,
    max_strength: Optional[int] = None,
    q: Optional[str] = None,
    sort: str = "id",
    owner_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 20,
) -> List[Item]:
    descending = sort.startswith("-")
    column_name = sort[1:] if descending else sort
    column = _SORT_COLUMNS.get(column_name, ItemModel.id)
    order = column.desc() if descending else column.asc()
    statement = _apply_item_filters(
        select(ItemModel).order_by(order),
        min_strength=min_strength,
        max_strength=max_strength,
        q=q,
        owner_id=owner_id,
    )
    statement = statement.offset(skip).limit(limit)
    return [_to_schema(row) for row in db.scalars(statement).all()]


def count_items(
    db: Session,
    min_strength: Optional[int] = None,
    max_strength: Optional[int] = None,
    q: Optional[str] = None,
    owner_id: Optional[int] = None,
) -> int:
    statement = _apply_item_filters(
        select(func.count()).select_from(ItemModel),
        min_strength=min_strength,
        max_strength=max_strength,
        q=q,
        owner_id=owner_id,
    )
    return db.scalar(statement) or 0


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


def update_item(db: Session, item_id: int, payload: Union[ItemUpdate, ItemPatch]) -> Optional[Item]:
    row = db.get(ItemModel, item_id)
    if row is None:
        return None
    for field, value in payload.model_dump(exclude_unset=True).items():
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
