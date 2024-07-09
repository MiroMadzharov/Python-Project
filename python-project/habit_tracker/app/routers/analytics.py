from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import database, schemas, models
from app.services.habits import (
    get_habits, get_habit_events
)
from typing import List
from datetime import timedelta

# Create a new API router instance
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


@router.get("/habits/longest_streak/", response_model=schemas.LongestStreakResponse)
def get_longest_streak_endpoint(user_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve the longest streak among all habits for a specific user, including the habit IDs.

    Args:
        user_id (int): The ID of the current user.
        db (Session, optional): SQLAlchemy database session dependency. Defaults to Depends(database.get_db).

    Returns:
        schemas.LongestStreakResponse: The longest streak and corresponding habit IDs.
    """
    user_habits = db.query(models.Habit).filter(
        models.Habit.owner_id == user_id).all()
    max_streak = 0
    habit_ids = []

    for habit in user_habits:
        current_streak = get_streak_for_habit(habit.id, db)
        if current_streak > max_streak:
            max_streak = current_streak
            habit_ids = [habit.id]
        elif current_streak == max_streak:
            habit_ids.append(habit.id)

    return schemas.LongestStreakResponse(longest_streak=max_streak, habit_ids=habit_ids)


def get_streak_for_habit(habit_id: int, db: Session):
    """
    Helper function to calculate the longest streak for a habit.

    Args:
        habit_id (int): The ID of the habit for which the longest streak is to be calculated.
        db (Session): SQLAlchemy database session.

    Returns:
        int: The longest streak for the specified habit.
    """
    # Retrieve habit events from the database
    events = get_habit_events(db, habit_id)
    # Sort events by timestamp
    events.sort(key=lambda x: x.timestamp)
    streak = 0
    max_streak = 0
    last_date = None

    # Calculate streaks based on consecutive dates
    for event in events:
        if last_date and event.timestamp.date() == (last_date + timedelta(days=1)):
            streak += 1
        else:
            streak = 1
        last_date = event.timestamp.date()
        max_streak = max(max_streak, streak)

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
    return get_streak_for_habit(habit_id, db)


def get_streak_for_habit_endpoint(habit_id: int, db: Session):
    """
    Helper function to calculate the longest streak for a habit.

    Args:
        habit_id (int): The ID of the habit for which the longest streak is to be calculated.
        db (Session): SQLAlchemy database session.

    Returns:
        int: The longest streak for the specified habit.
    """
    # Retrieve habit events from the database
    events = get_habit_events(db, habit_id)
    # Sort events by timestamp
    events.sort(key=lambda x: x.timestamp)
    streak = 0
    max_streak = 0
    last_date = None

    # Calculate streaks based on consecutive dates
    for event in events:
        if last_date and event.timestamp.date() == (last_date + timedelta(days=1)):
            streak += 1
        else:
            streak = 1
        last_date = event.timestamp.date()
        max_streak = max(max_streak, streak)

    return max_streak
