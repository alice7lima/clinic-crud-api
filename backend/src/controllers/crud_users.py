from fastapi import HTTPException
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import Session
from src.models import User
from src.schemas import UserCreate
from src.security import get_password_hash, verify_password


def create_user(db: Session, user: UserCreate):
    db_user = get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=get_password_hash(user.password),
        admin=user.admin,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(
    db: Session,
    username: str,
):
    query = db.query(User)
    query = query.filter(User.username == username)

    return query.first()

def authenticate(session: Session, username: str, password: str):
    db_user = get_user(db=session, username=username)
    if not db_user or not verify_password(password, db_user.hashed_password):
        return None
    return db_user