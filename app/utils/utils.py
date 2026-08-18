import re
from pydantic import TypeAdapter, EmailStr, ValidationError
from pydantic_extra_types.phone_numbers import PhoneNumber

# from phonenumbers import NumberParseException

USERNAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_]{2,29}$")


def validate_username(username: str) -> str:
    username = username.strip()

    if not USERNAME_PATTERN.fullmatch(username):
        raise ValueError(
            "Username must be 3-30 characters long, start with a letter, "
            "and contain only letters, numbers, and underscores."
        )

    return username


def is_valid_email(email: str) -> bool:
    try:
        TypeAdapter(EmailStr).validate_python(email)
        return True
    except ValidationError:
        return False