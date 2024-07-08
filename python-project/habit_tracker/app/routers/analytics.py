from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import database, schemas, models
from app.services.habits import create_habit, get_habit, get_habits, update_habit, checkoff_habit, delete_habit, create_habit_event, get_habit_events
from app.services.users import get_user_by_email, create_user
from typing import List
from datetime import timedelta

router = APIRouter()

@router.get("/habits/", response_model=List[schemas.Habit])
def get_all_habits_endpoint(user_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve all habits for a specific user.

    Args:
        user_id (int): The ID of the user whose habits are to be retrieved.
        db (Session, optional): SQLAlchemy database session dependency. Defaults to Depends(database.get_db).

    Returns:
        List[schemas.Habit]: A list of habits belonging to the user.
    """
    return get_habits(db, user_id=user_id)

@router.get("/habits/periodicity/{periodicity}", response_model=List[schemas.Habit])
def get_habits_by_periodicity_endpoint(user_id: int, periodicity: str, db: Session = Depends(database.get_db)):
    """
    Retrieve habits for a specific user filtered by periodicity.

    Args:
        user_id (int): The ID of the user whose habits are to be filtered.
        periodicity (str): The periodicity (e.g., 'daily', 'weekly') to filter habits by.
        db (Session, optional): SQLAlchemy database session dependency. Defaults to Depends(database.get_db).

    Returns:
        List[schemas.Habit]: A list of habits belonging to the user filtered by periodicity.
    """
    return [habit for habit in get_habits(db, user_id=user_id) if habit.periodicity == periodicity]

@router.get("/habits/longest_streak/", response_model=int)
def get_longest_streak_endpoint(db: Session = Depends(database.get_db)):
    """
    Retrieve the longest streak among all habits for all users.

    Args:
        db (Session, optional): SQLAlchemy database session dependency. Defaults to Depends(database.get_db).

    Returns:
        int: The longest streak across all habits.
    """
    all_habits = db.query(models.Habit).all()
    max_streak = 0
    for habit in all_habits:
        max_streak = max(max_streak, get_streak_for_habit_endpoint(habit.id, db))
    return max_streak

@router.get("/habits/{habit_id}/longest_streak/", response_model=int)
def get_longest_streak_for_habit_endpoint(habit_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve the longest streak for a specific habit.

    Args:
        habit_id (int): The ID of the habit for which the longest streak is to be retrieved.
        db (Session, optional): SQLAlchemy database session dependency. Defaults to Depends(database.get_db).

    Returns:
        int: The longest streak for the specified habit.
    """
    return get_streak_for_habit_endpoint(habit_id, db)

def get_streak_for_habit_endpoint(habit_id: int, db: Session):
    """
    Helper function to calculate the longest streak for a habit.

    Args:
        habit_id (int): The ID of the habit for which the longest streak is to be calculated.
        db (Session): SQLAlchemy database session.

    Returns:
        int: The longest streak for the specified habit.
    """
    events = get_habit_events(db, habit_id)
    events.sort(key=lambda x: x.timestamp)
    streak = 0
    max_streak = 0
    last_date = None
    for event in events:
        if last_date and event.timestamp.date() == (last_date + timedelta(days=1)):
            streak += 1
        else:
            streak = 1
        last_date = event.timestamp.date()
        max_streak = max(max_streak, streak)
    return max_streak
