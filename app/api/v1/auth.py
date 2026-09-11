from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.schemas.user import Token, User, UserCreate, UserLogin
from app.services import users as users_service

router = APIRouter()


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(
    payload: UserCreate,
    response: Response,
    db: Session = Depends(get_db),
) -> User:
    user = users_service.register_user(db, payload)
    response.headers["Location"] = "/api/v1/auth/me"
    return user


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)) -> Token:
    return users_service.authenticate_user(
        db,
        email=payload.email,
        password=payload.password,
    )


@router.get("/me", response_model=User)
def read_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
