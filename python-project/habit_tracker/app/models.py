from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class User(Base):
    """
    SQLAlchemy User model representing users in the application.

    Attributes:
        __tablename__ (str): Name of the database table for users.
        id (int): Primary key identifier for the user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        email (str): Email address of the user (unique).
        hashed_password (str): Hashed password of the user.

    Relationships:
        habits (relationship): One-to-many relationship with Habit model via owner_id.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    habits = relationship("Habit", back_populates="owner")


class Habit(Base):
    """
    SQLAlchemy Habit model representing habits tracked by users.

    Attributes:
        __tablename__ (str): Name of the database table for habits.
        id (int): Primary key identifier for the habit.
        name (str): Name of the habit.
        description (str): Description of the habit.
        periodicity (str): Frequency of the habit (e.g., daily, weekly).
        created_at (DateTime): Timestamp of when the habit was created.
        owner_id (int): Foreign key linking to the User who owns this habit.

    Relationships:
        owner (relationship): Many-to-one relationship with User model via owner_id.
        events (relationship): One-to-many relationship with HabitEvent model via habit_id.
    """
    __tablename__ = "habits"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    periodicity = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="habits")
    events = relationship("HabitEvent", back_populates="habit")


class HabitEvent(Base):
    """
    SQLAlchemy HabitEvent model representing events or check-offs for habits.

    Attributes:
        __tablename__ (str): Name of the database table for habit events.
        id (int): Primary key identifier for the event.
        habit_id (int): Foreign key linking to the Habit associated with this event.
        timestamp (DateTime): Timestamp of when the event occurred.

    Relationships:
        habit (relationship): Many-to-one relationship with Habit model via habit_id.
    """
    __tablename__ = "habit_events"
    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)

    habit = relationship("Habit", back_populates="events")
