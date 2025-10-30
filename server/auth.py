import re
from typing import Tuple


def is_valid_email(email: str) -> bool:
    if not email or not isinstance(email, str):
        return False
    return bool(re.match(r"^\S+@\S+\.\S+$", email))


def is_strong_password(password: str) -> Tuple[bool, list]:
    errors = []
    if not isinstance(password, str):
        errors.append("password must be a string")
        return False, errors
    if len(password) < 12:
        errors.append("password must be at least 12 characters")
    if not re.search(r"\d", password):
        errors.append("password must contain a number")
    if not re.search(r"[^A-Za-z0-9]", password):
        errors.append("password must contain a special character")
    return len(errors) == 0, errors
