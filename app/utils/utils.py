import re
from datetime import date

import phonenumbers
from phonenumbers import NumberParseException


def validate_username(username: str) -> str:
    username_pattern = re.compile(r"^[A-Za-z][A-Za-z0-9_]{2,29}$")

    username = username.strip().lower()

    if not username_pattern.fullmatch(username):
        raise ValueError(
            "Username must be 3-30 characters long, start with a letter, "
            "and contain only letters, numbers, and underscores."
        )

    return username


def validate_phone_number(phone_number: str, default_region: str = "NG") -> str:
    try:
        number = phonenumbers.parse(phone_number, default_region)

        if not phonenumbers.is_valid_number(number):
            raise ValueError("Invalid phone number")

        return phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164,)

    except NumberParseException:
        raise ValueError("Invalid phone number")


def validate_date_of_birth(dob: date | None, minimum_age: int = 10):
    if dob is None:
        return None

    today = date.today()
    if dob > today:
        raise ValueError("Date of birth cannot be in the future")

    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    if age < minimum_age:
        raise ValueError(f"User must be at least {minimum_age} years old")

    return dob

# If an account exists for this email, you will receive an email.