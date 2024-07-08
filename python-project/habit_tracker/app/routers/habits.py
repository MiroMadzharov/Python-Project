from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, database
from app.services.habits import create_habit, get_habit, get_habits, update_habit, checkoff_habit, delete_habit, create_habit_event, get_habit_events, get_streak_for_habit, is_habit_broken
from app.services.users import get_user_by_email, create_user, pwd_context
from typing import List

router = APIRouter()

@router.post("/", response_model=schemas.Habit)
def create_habit_endpoint(habit: schemas.HabitCreate, user_id: int, db: Session = Depends(database.get_db)):
    """
    Create a new habit for the user.

    Args:
        habit (schemas.HabitCreate): The data to create the habit.
        user_id (int): The ID of the user to whom the habit belongs.
        db (Session, optional): The SQLAlchemy session dependency. Defaults to Depends(database.get_db).

    Returns:
        schemas.Habit: The created habit.
    """
    return create_habit(db=db, habit=habit, user_id=user_id)


@router.get("/", response_model=List[schemas.Habit])
def read_habits_endpoint(user_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve all habits belonging to a user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        List[schemas.Habit]: List of habits belonging to the user.
    """
    return get_habits(db, user_id=user_id)


@router.put("/{habit_id}", response_model=schemas.Habit)
def update_habit_endpoint(habit_id: int, habit: schemas.HabitUpdate, db: Session = Depends(database.get_db)):
    """
    Update a specific habit.

    Args:
        habit_id (int): The ID of the habit to update.
        habit (schemas.HabitUpdate): The updated habit data.
        db (Session, optional): The SQLAlchemy session dependency. Defaults to Depends(database.get_db).

    Returns:
        schemas.Habit: The updated habit.
    
    Raises:
        HTTPException: If the habit with the given ID is not found (status_code=404).
    """
    db_habit = get_habit(db, habit_id=habit_id)
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return update_habit(db=db, habit=habit, habit_id=habit_id)


@router.put("/{habit_id}/checkoff", response_model=schemas.Habit)
def checkoff_habit_endpoint(habit_id: int, db: Session = Depends(database.get_db)):
    """
    Check off a habit for the current day.

    Args:
        habit_id (int): The ID of the habit to check off.
        db (Session, optional): The SQLAlchemy session dependency. Defaults to Depends(database.get_db).

    Returns:
        schemas.Habit: The updated habit after checking off.

    Raises:
        HTTPException: If the habit with the given ID is not found (status_code=404).
    """
    db_habit = get_habit(db, habit_id=habit_id)
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return checkoff_habit(db=db, habit_id=habit_id)


@router.delete("/{habit_id}", response_model=schemas.Habit)
def delete_habit_endpoint(habit_id: int, db: Session = Depends(database.get_db)):
    """
    Delete a specific habit.

    Args:
        habit_id (int): The ID of the habit to delete.
        db (Session, optional): The SQLAlchemy session dependency. Defaults to Depends(database.get_db).

    Returns:
        schemas.Habit: The deleted habit.

    Raises:
        HTTPException: If the habit with the given ID is not found (status_code=404).
    """
    db_habit = get_habit(db, habit_id=habit_id)
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return delete_habit(db=db, habit_id=habit_id)


@router.post("/event/", response_model=schemas.HabitEvent)
def create_habit_event_endpoint(habit_event: schemas.HabitEventCreate, db: Session = Depends(database.get_db)):
    """
    Create a new event for a habit.

    Args:
        habit_event (schemas.HabitEventCreate): The data to create the habit event.
        db (Session, optional): The SQLAlchemy session dependency. Defaults to Depends(database.get_db).

    Returns:
        schemas.HabitEvent: The created habit event.
    """
    return create_habit_event(db=db, habit_event=habit_event)


@router.get("/{habit_id}/events/", response_model=List[schemas.HabitEvent])
def read_habit_events_endpoint(habit_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve all events associated with a specific habit.

    Args:
        habit_id (int): The ID of the habit.

    Returns:
        List[schemas.HabitEvent]: List of events associated with the habit.
    """
    return get_habit_events(db, habit_id=habit_id)


@router.get("/{habit_id}/streak/", response_model=int)
def get_streak_endpoint(habit_id: int, db: Session = Depends(database.get_db)):
    """
    Get the current streak (number of consecutive days) for a habit.

    Args:
        habit_id (int): The ID of the habit.

    Returns:
        int: The current streak for the habit.
    """
    return get_streak_for_habit(habit_id=habit_id, db=db)


@router.get("/{habit_id}/is_broken/", response_model=bool)
def is_habit_broken_endpoint(habit_id: int, db: Session = Depends(database.get_db)):
    """
    Check if a habit's streak is broken (i.e., the habit was not completed yesterday).

    Args:
        habit_id (int): The ID of the habit.

    Returns:
        bool: True if the habit's streak is broken, False otherwise.
    """
    return is_habit_broken(habit_id=habit_id, db=db)
