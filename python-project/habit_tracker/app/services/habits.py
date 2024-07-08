from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_habit(db: Session, habit: schemas.HabitCreate, user_id: int):
    """
    Create a new habit for a specific user in the database.

    Args:
        db (Session): SQLAlchemy database session.
        habit (schemas.HabitCreate): Habit data to create.
        user_id (int): User ID who owns the habit.

    Returns:
        models.Habit: Created habit object.
    """
    db_habit = models.Habit(**habit.dict(), owner_id=user_id)  # Create SQLAlchemy model object
    db.add(db_habit)  # Add to session
    db.commit()  # Commit transaction to database
    db.refresh(db_habit)  # Refresh object to get updated data from database
    return db_habit  # Return created habit object

def get_habit(db: Session, habit_id: int):
    """
    Retrieve a habit by its ID.

    Args:
        db (Session): SQLAlchemy database session.
        habit_id (int): ID of the habit to retrieve.

    Returns:
        models.Habit: Habit object if found, otherwise None.
    """
    return db.query(models.Habit).filter(models.Habit.id == habit_id).first()  # Query habit by ID

def get_habits(db: Session, user_id: int):
    """
    Retrieve all habits belonging to a specific user.

    Args:
        db (Session): SQLAlchemy database session.
        user_id (int): User ID whose habits to retrieve.

    Returns:
        List[models.Habit]: List of habit objects.
    """
    return db.query(models.Habit).filter(models.Habit.owner_id == user_id).all()  # Query habits by user ID

def update_habit(db: Session, habit: schemas.HabitUpdate, habit_id: int):
    """
    Update an existing habit with new data.

    Args:
        db (Session): SQLAlchemy database session.
        habit (schemas.HabitUpdate): New habit data.
        habit_id (int): ID of the habit to update.

    Returns:
        models.Habit: Updated habit object if found, otherwise None.
    """
    db_habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()  # Query habit by ID
    if not db_habit:
        return None  # Return None if habit not found
    for key, value in habit.dict().items():
        setattr(db_habit, key, value)  # Update habit attributes
    db.commit()  # Commit transaction
    db.refresh(db_habit)  # Refresh habit object
    return db_habit  # Return updated habit object

def checkoff_habit(db: Session, habit_id: int):
    """
    Record a check-off event for a habit.

    Args:
        db (Session): SQLAlchemy database session.
        habit_id (int): ID of the habit to check off.

    Returns:
        models.Habit: Habit object if found and event recorded, otherwise None.
    """
    db_habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()  # Query habit by ID
    if not db_habit:
        return None  # Return None if habit not found
    db_event = models.HabitEvent(habit_id=habit_id, timestamp=datetime.utcnow())  # Create new habit event
    db.add(db_event)  # Add event to session
    db.commit()  # Commit transaction
    db.refresh(db_event)  # Refresh event object
    return db_habit  # Return associated habit object

def delete_habit(db: Session, habit_id: int):
    """
    Delete a habit by its ID.

    Args:
        db (Session): SQLAlchemy database session.
        habit_id (int): ID of the habit to delete.

    Returns:
        models.Habit: Deleted habit object if found, otherwise None.
    """
    db_habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()  # Query habit by ID
    if not db_habit:
        return None  # Return None if habit not found
    db.delete(db_habit)  # Delete habit
    db.commit()  # Commit transaction
    return db_habit  # Return deleted habit object

def create_habit_event(db: Session, habit_event: schemas.HabitEventCreate):
    """
    Create a new habit event in the database.

    Args:
        db (Session): SQLAlchemy database session.
        habit_event (schemas.HabitEventCreate): Habit event data to create.

    Returns:
        models.HabitEvent: Created habit event object.
    """
    db_event = models.HabitEvent(**habit_event.dict())  # Create SQLAlchemy model object
    db.add(db_event)  # Add event to session
    db.commit()  # Commit transaction
    db.refresh(db_event)  # Refresh event object
    return db_event  # Return created habit event object

def get_habit_events(db: Session, habit_id: int):
    """
    Retrieve all events associated with a habit.

    Args:
        db (Session): SQLAlchemy database session.
        habit_id (int): ID of the habit whose events to retrieve.

    Returns:
        List[models.HabitEvent]: List of habit event objects.
    """
    return db.query(models.HabitEvent).filter(models.HabitEvent.habit_id == habit_id).all()  # Query events by habit ID

def get_streak_for_habit(habit_id: int, db: Session):
    """
    Calculate the current streak (longest consecutive days) for a habit.

    Args:
        habit_id (int): ID of the habit to calculate streak for.
        db (Session): SQLAlchemy database session.

    Returns:
        int: Maximum streak of consecutive days the habit was checked off.
    """
    events = get_habit_events(db, habit_id)  # Retrieve habit events
    events.sort(key=lambda x: x.timestamp)  # Sort events by timestamp

    # Initialize variables for streak calculation
    periodicity = db.query(models.Habit).filter(models.Habit.id == habit_id).first().periodicity
    streak = 0
    max_streak = 0
    last_date = None

    for event in events:
        if periodicity == 'daily':
            if last_date and event.timestamp.date() == (last_date + timedelta(days=1)):
                streak += 1
            else:
                streak = 1
        elif periodicity == 'weekly':
            if last_date and event.timestamp.date() <= (last_date + timedelta(days=7)):
                streak += 1
            else:
                streak = 1
        last_date = event.timestamp.date()
        max_streak = max(max_streak, streak)  # Update max streak

    return max_streak  # Return maximum streak

def is_habit_broken(habit_id: int, db: Session):
    """
    Check if a habit is considered 'broken' based on its periodicity and last event date.

    Args:
        habit_id (int): ID of the habit to check.
        db (Session): SQLAlchemy database session.

    Returns:
        bool: True if the habit is broken (no recent check-off), False otherwise.
    """
    events = get_habit_events(db, habit_id)  # Retrieve habit events
    if not events:
        return True  # Return True if no events found

    # Determine last event date and current date
    last_event_date = max(event.timestamp for event in events).date()
    periodicity = db.query(models.Habit).filter(models.Habit.id == habit_id).first().periodicity
    current_date = datetime.utcnow().date()

    # Check if habit is broken based on periodicity
    if periodicity == 'daily' and (current_date - last_event_date).days > 1:
        return True
    if periodicity == 'weekly' and (current_date - last_event_date).days > 7:
        return True

    return False  # Return False if habit is not broken
