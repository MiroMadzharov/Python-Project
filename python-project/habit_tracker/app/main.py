from fastapi import FastAPI
from app.routers import auth, habits, analytics
from app.services.habits import create_habit, get_habit, get_habits, update_habit, checkoff_habit, delete_habit, create_habit_event, get_habit_events
from app.services.users import get_user_by_email, create_user
from app.database import engine, Base, SessionLocal
from app import models, schemas
from datetime import datetime, timedelta

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Predefined habits and example tracking data
def init_db():
    db = SessionLocal()

    # Create a default user if not exists
    default_user_email = "example@example.com"
    existing_user = get_user_by_email(db, email=default_user_email)
    if not existing_user:
        # Create a UserCreate object
        user_create = schemas.UserCreate(
            first_name="John",
            last_name="Doe",
            email=default_user_email,
            password="somehashedpassword"
        )
        created_user = create_user(db, user=user_create)
        user_id = created_user.id
    else:
        user_id = existing_user.id


    predefined_habits = [
        {"name": "Exercise", "description": "Daily exercise", "periodicity": "daily"},
        {"name": "Read", "description": "Read a book", "periodicity": "daily"},
        {"name": "Meditate", "description": "Meditate for 10 minutes", "periodicity": "daily"},
        {"name": "Weekly Review", "description": "Weekly review of goals", "periodicity": "weekly"},
        {"name": "Call Family", "description": "Call family members", "periodicity": "weekly"},
    ]
    for habit_data in predefined_habits:
        habit = schemas.HabitCreate(**habit_data)
        create_habit(db, habit=habit, user_id=user_id)

    # Example tracking data
    habits = get_habits(db, user_id=user_id)
    for habit in habits:
        for i in range(4):  # 4 weeks of data
            event = schemas.HabitEventCreate(habit_id=habit.id)
            event_date = datetime.utcnow() - timedelta(weeks=i)
            create_habit_event(db, habit_event=event)

    db.close()

init_db()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(habits.router, prefix="/habits", tags=["habits"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])  # Include the analytics router
