import re


class PasswordPolicy:

    MIN_LENGTH = 12
    MAX_LENGTH = 128

    @classmethod
    def validate(
            cls,
            password: str,
    ) -> tuple[bool, str]:

        if len(password) < cls.MIN_LENGTH:
            return (
                False,
                "Password must be at least 12 characters long.",
            )

        if len(password) > cls.MAX_LENGTH:
            return (
                False,
                "Password must not exceed 128 characters.",
            )

        if not re.search(r"[A-Z]", password):
            return (
                False,
                "Password must contain an uppercase letter.",
            )

        if not re.search(r"[a-z]", password):
            return (
                False,
                "Password must contain a lowercase letter.",
            )

        if not re.search(r"\d", password):
            return (
                False,
                "Password must contain a number.",
            )

        if not re.search(r"[^\w\s]", password):
            return (
                False,
                "Password must contain a special character.",
            )

        return True, "Password is valid."