"""
Module: auth.py
Defines API endpoints related to user authentication.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, database
from app.services.users import get_user_by_email, create_user, pwd_context

router = APIRouter()

@router.post("/signup/", response_model=schemas.User)
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """
    Create a new user account.

    Args:
        user (schemas.UserCreate): User creation details.
        db (Session, optional): Database session dependency. Defaults to Depends(database.get_db).

    Raises:
        HTTPException: If the email is already registered.

    Returns:
        schemas.User: Created user details.
    """
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

@router.get("/login/")
def login_endpoint(email: str, password: str, db: Session = Depends(database.get_db)):
    """
    User login endpoint.

    Args:
        email (str): User's email address.
        password (str): User's password.
        db (Session, optional): Database session dependency. Defaults to Depends(database.get_db).

    Raises:
        HTTPException: If credentials are invalid.

    Returns:
        dict: Message indicating login success.
    """
    user = get_user_by_email(db, email=email)
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful"}
