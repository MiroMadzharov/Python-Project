# Habit Tracker App

## Project Description

Creating good habits and breaking bad ones is no easy task. To keep track of certain habits or achieve personal goals, many people rely on habit trackers to help them throughout the day. This project aims to build a basic Python backend for a habit tracking app, focusing on essential functionality using object-oriented and functional programming in Python. The application allows users to define multiple habits, complete tasks, track habit streaks, and analyze their habit data.

### Key Features:
- Define multiple habits with specific tasks and periodicities.
- Complete tasks and check them off at any point in time.
- Track and maintain habit streaks.
- Analyze habits to answer questions like the longest habit streak, current daily habits, and habits struggled with most.

## Installation

1. Clone the repository:

    ```bash
    git clone <repository-url>
    cd habit_tracker
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:

    ```bash
    alembic upgrade head
    ```

5. Run the application:

    ```bash
    uvicorn app.main:app --reload
    ```

## Usage

After starting the application, the API documentation will be available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## API Endpoints

Here are some of the key API endpoints you can use:

- **Create a new habit**: `POST /habits`
- **Get all habits**: `GET /habits`
- **Complete a task**: `POST /habits/{habit_id}/complete`
- **Get habit analysis**: `GET /habits/analysis`

Refer to the API documentation for detailed information on each endpoint.

## Testing

To run tests:

```bash
pytest
