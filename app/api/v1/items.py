from typing import List, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.schemas.item import Item, ItemCreate, ItemPatch, ItemUpdate
from app.schemas.user import User
from app.services import items as items_service

router = APIRouter()


@router.get("/", response_model=List[Item])
def list_items(
    response: Response,
    min_strength: Optional[int] = Query(default=None, ge=1, le=100),
    max_strength: Optional[int] = Query(default=None, ge=1, le=100),
    q: Optional[str] = Query(default=None, min_length=1, max_length=100),
    sort: Literal["id", "-id", "strength", "-strength"] = Query(default="id"),
    owner_id: Optional[int] = Query(default=None, ge=1),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> List[Item]:
    if (
        min_strength is not None
        and max_strength is not None
        and min_strength > max_strength
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="min_strength cannot be greater than max_strength",
        )
    items = items_service.list_items(
        db,
        min_strength=min_strength,
        max_strength=max_strength,
        q=q,
        sort=sort,
        owner_id=owner_id,
        skip=skip,
        limit=limit,
    )
    total = items_service.count_items(
        db,
        min_strength=min_strength,
        max_strength=max_strength,
        q=q,
        owner_id=owner_id,
    )
    response.headers["X-Total-Count"] = str(total)
    return items


@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    return items_service.get_item(db, item_id)


@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(
    payload: ItemCreate,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Item:
    item = items_service.create_item(db, payload, current_user)
    response.headers["Location"] = "/api/v1/items/{0}".format(item.id)
    return item


@router.put("/{item_id}", response_model=Item)
def update_item(
    item_id: int,
    payload: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Item:
    return items_service.update_item(db, item_id, payload, current_user)


@router.patch("/{item_id}", response_model=Item)
def patch_item(
    item_id: int,
    payload: ItemPatch,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Item:
    return items_service.patch_item(db, item_id, payload, current_user)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    items_service.delete_item(db, item_id, current_user)
