from sqlalchemy.orm import Session

from app.core.exceptions import AuthenticationError, ConflictError
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.repositories import users as users_repository
from app.schemas.user import Token, User, UserCreate


def register_user(db: Session, payload: UserCreate) -> User:
    existing = users_repository.get_user_by_email(db, payload.email)
    if existing is not None:
        raise ConflictError("Email already registered")
    user = users_repository.create_user(
        db,
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    return User.model_validate(user)


def authenticate_user(db: Session, email: str, password: str) -> Token:
    user = users_repository.get_user_by_email(db, email)
    if user is None or not verify_password(password, user.hashed_password):
        raise AuthenticationError("Incorrect email or password")
    if not user.is_active:
        raise AuthenticationError("Inactive user")
    token = create_access_token(str(user.id))
    return Token(access_token=token)
