from typing import Generator, Optional

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.exceptions import AuthenticationError
from app.core.security import decode_access_token
from app.db.session import SessionLocal
from app.repositories import users as users_repository
from app.schemas.user import User

bearer_scheme = HTTPBearer(auto_error=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> User:
    if credentials is None:
        raise AuthenticationError("Could not validate credentials")
    user_id = decode_access_token(credentials.credentials)
    if user_id is None:
        raise AuthenticationError("Could not validate credentials")
    try:
        parsed_id = int(user_id)
    except ValueError:
        raise AuthenticationError("Could not validate credentials")
    user = users_repository.get_user(db, parsed_id)
    if user is None or not user.is_active:
        raise AuthenticationError("Could not validate credentials")
    return User.model_validate(user)
