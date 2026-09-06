from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    strength: int = Field(default=1, ge=1, le=100)


class ItemUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    strength: int = Field(ge=1, le=100)


class ItemPatch(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    strength: Optional[int] = Field(default=None, ge=1, le=100)

    @model_validator(mode="after")
    def at_least_one_field(self) -> "ItemPatch":
        if self.name is None and self.description is None and self.strength is None:
            raise ValueError("At least one field is required")
        return self


class Item(ItemCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
