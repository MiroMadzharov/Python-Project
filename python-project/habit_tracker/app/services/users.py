# habit_tracker/app/services/users.py

from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    """
    Retrieve a user by their email address.

    Args:
        db (Session): Database session dependency
        email (str): Email address of the user to retrieve

    Returns:
        models.User: User object corresponding to the email, or None if not found
    """
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    """
    Create a new user.

    Args:
        db (Session): Database session dependency
        user (schemas.UserCreate): User creation data

    Returns:
        models.User: Newly created user object
    """
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        first_name=user.first_name, last_name=user.last_name, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
