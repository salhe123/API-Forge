from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    strength: int = Field(default=1, ge=1, le=100)


class ItemUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    strength: int = Field(ge=1, le=100)


class Item(ItemCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
