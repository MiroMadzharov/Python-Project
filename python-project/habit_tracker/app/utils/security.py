# habit_tracker/app/utils/security.py

from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    """
    Generate a bcrypt hash for the given password.

    Args:
        password (str): Plain-text password to hash

    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)  # Hash the provided password

def verify_password(plain_password, hashed_password):
    """
    Verify if the provided plain password matches the hashed password.

    Args:
        plain_password (str): Plain-text password to verify
        hashed_password (str): Hashed password to compare against

    Returns:
        bool: True if passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)  # Verify if plain password matches hashed password
