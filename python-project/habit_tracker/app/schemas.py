from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class UserCreate(BaseModel):
    """
    Pydantic model for creating a new user.

    Attributes:
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        email (str): Email address of the user.
        password (str): Password for the user.
    """
    first_name: str
    last_name: str
    email: str
    password: str


class User(BaseModel):
    """
    Pydantic model for user data.

    Attributes:
        id (int): Identifier for the user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        email (str): Email address of the user.

    Config:
        from_attributes (bool): Enables automatic creation from attributes.
    """
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True


class HabitCreate(BaseModel):
    """
    Pydantic model for creating a new habit.

    Attributes:
        name (str): Name of the habit.
        description (str): Description of the habit.
        periodicity (str): Frequency of the habit (e.g., daily, weekly).
    """
    name: str
    description: str
    periodicity: str


class HabitUpdate(BaseModel):
    """
    Pydantic model for updating an existing habit.

    Attributes:
        name (str, optional): Updated name of the habit.
        description (str, optional): Updated description of the habit.
        periodicity (str, optional): Updated frequency of the habit.
    """
    name: Optional[str]
    description: Optional[str]
    periodicity: Optional[str]


class Habit(BaseModel):
    """
    Pydantic model for habit data.

    Attributes:
        id (int): Identifier for the habit.
        name (str): Name of the habit.
        description (str): Description of the habit.
        periodicity (str): Frequency of the habit.
        created_at (datetime): Timestamp of when the habit was created.
        owner_id (int): Identifier of the owner user.

    Config:
        from_attributes (bool): Enables automatic creation from attributes.
    """
    id: int
    name: str
    description: str
    periodicity: str
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True


class HabitEventCreate(BaseModel):
    """
    Pydantic model for creating a new habit event.

    Attributes:
        habit_id (int): Identifier of the habit associated with the event.
    """
    habit_id: int


class HabitEvent(BaseModel):
    """
    Pydantic model for habit event data.

    Attributes:
        id (int): Identifier for the habit event.
        habit_id (int): Identifier of the habit associated with the event.
        timestamp (datetime): Timestamp of when the event occurred.

    Config:
        from_attributes (bool): Enables automatic creation from attributes.
    """
    id: int
    habit_id: int
    timestamp: datetime

    class Config:
        from_attributes = True


class LongestStreakResponse(BaseModel):
    longest_streak: int
    habit_ids: List[int]
