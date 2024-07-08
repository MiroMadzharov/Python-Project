# Habit Tracker App

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

The API documentation will be available at http://127.0.0.1:8000/docs after starting the application.

## Testing

To run tests:

```bash
pytest

```


This should give you a comprehensive guide to setting up and running your habit tracker backend with FastAPI and PostgreSQL. You can expand upon this by adding more detailed functionality, refining error handling, and enhancing your test coverage.
