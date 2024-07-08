# habit_tracker/app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL for PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:KAKE@localhost/habit_tracker_db"

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SessionLocal class using sessionmaker to manage database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a declarative base class for SQLAlchemy models
Base = declarative_base()

def get_db():
    """
    Dependency to provide a database session.

    Yields:
        Session: Database session object
    """
    db = SessionLocal()  # Create a new session using SessionLocal
    try:
        yield db  # Yield the session to the caller
    finally:
        db.close()  # Close the session when done
