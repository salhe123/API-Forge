from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import UserModel


def get_user(db: Session, user_id: int) -> Optional[UserModel]:
    return db.get(UserModel, user_id)


def get_user_by_email(db: Session, email: str) -> Optional[UserModel]:
    statement = select(UserModel).where(UserModel.email == email)
    return db.scalars(statement).first()


def create_user(db: Session, email: str, hashed_password: str) -> UserModel:
    row = UserModel(email=email, hashed_password=hashed_password)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
