from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


def _strip_name(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    stripped = value.strip()
    if not stripped:
        raise ValueError("name cannot be blank")
    return stripped


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    strength: int = Field(default=1, ge=1, le=100)

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        stripped = _strip_name(value)
        assert stripped is not None
        return stripped


class ItemUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    strength: int = Field(ge=1, le=100)

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        stripped = _strip_name(value)
        assert stripped is not None
        return stripped


class ItemPatch(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    strength: Optional[int] = Field(default=None, ge=1, le=100)

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: Optional[str]) -> Optional[str]:
        return _strip_name(value)

    @model_validator(mode="after")
    def at_least_one_field(self) -> "ItemPatch":
        if self.name is None and self.description is None and self.strength is None:
            raise ValueError("At least one field is required")
        return self


class Item(ItemCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
