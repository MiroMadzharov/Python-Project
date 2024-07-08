from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True

class HabitCreate(BaseModel):
    name: str
    description: str
    periodicity: str
    
    
    
class HabitUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    periodicity: Optional[str]



class Habit(BaseModel):
    id: int
    name: str
    description: str
    periodicity: str
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True

class HabitEventCreate(BaseModel):
    habit_id: int

class HabitEvent(BaseModel):
    id: int
    habit_id: int
    timestamp: datetime

    class Config:
        from_attributes = True
