"""Password validation module.

This module provides password validation functionality to ensure
passwords meet security requirements.
"""

from dataclasses import dataclass
import re


@dataclass(slots=True)
class PasswordValidationResult:
    """Result of password validation.

    Attributes:
        is_valid: Whether the password is valid.
        error_message: Error message if password is invalid, None otherwise.
    """

    is_valid: bool
    error_message: str | None = None


class PasswordValidator:
    """Password validator with configurable requirements.

    Requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character
    """

    MIN_LENGTH = 8
    SPECIAL_CHARS = re.compile(r"[!@#$%^&*(),.?\":{}|<>]")

    @classmethod
    def validate(cls, password: str) -> PasswordValidationResult:
        """Validate password against security requirements.

        Args:
            password: Password to validate.

        Returns:
            PasswordValidationResult with validation status and error message.
        """
        if len(password) < cls.MIN_LENGTH:
            return PasswordValidationResult(
                is_valid=False,
                error_message=f"Password must be at least {cls.MIN_LENGTH} characters",
            )

        if not re.search(r"[A-Z]", password):
            return PasswordValidationResult(
                is_valid=False,
                error_message="Password must contain at least one uppercase letter",
            )

        if not re.search(r"[a-z]", password):
            return PasswordValidationResult(
                is_valid=False,
                error_message="Password must contain at least one lowercase letter",
            )

        if not re.search(r"\d", password):
            return PasswordValidationResult(
                is_valid=False,
                error_message="Password must contain at least one digit",
            )

        if not cls.SPECIAL_CHARS.search(password):
            return PasswordValidationResult(
                is_valid=False,
                error_message="Password must contain at least one special character",
            )

        return PasswordValidationResult(is_valid=True)
