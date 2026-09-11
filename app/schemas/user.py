from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


def _strip_email(value):
    if isinstance(value, str):
        return value.strip()
    return value


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

    @field_validator("email", mode="before")
    @classmethod
    def strip_email(cls, value):
        return _strip_email(value)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

    @field_validator("email", mode="before")
    @classmethod
    def strip_email(cls, value):
        return _strip_email(value)


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
