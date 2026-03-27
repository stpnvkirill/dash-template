"""Unit tests for PasswordValidator."""

from app.backend.domain.validators.password import (
    PasswordValidationResult,
    PasswordValidator,
)


class TestPasswordValidationResult:
    """Tests for PasswordValidationResult."""

    def test_valid_password(self) -> None:
        """Test valid password result."""
        result = PasswordValidationResult(is_valid=True)
        assert result.is_valid is True
        assert result.error_message is None

    def test_invalid_password(self) -> None:
        """Test invalid password result."""
        result = PasswordValidationResult(
            is_valid=False,
            error_message="Password too short",
        )
        assert result.is_valid is False
        assert result.error_message == "Password too short"


class TestPasswordValidator:
    """Tests for PasswordValidator."""

    def test_valid_password(self) -> None:
        """Test valid password passes all requirements."""
        result = PasswordValidator.validate("StrongP@ss123")
        assert result.is_valid is True
        assert result.error_message is None

    def test_too_short_password(self) -> None:
        """Test password shorter than minimum length."""
        result = PasswordValidator.validate("Short1!")
        assert result.is_valid is False
        assert "at least 8 characters" in result.error_message

    def test_exactly_minimum_length(self) -> None:
        """Test password with exactly minimum length."""
        result = PasswordValidator.validate("Strong1!")
        assert result.is_valid is True

    def test_no_uppercase(self) -> None:
        """Test password without uppercase letter."""
        result = PasswordValidator.validate("lowercase123!")
        assert result.is_valid is False
        assert "uppercase" in result.error_message.lower()

    def test_no_lowercase(self) -> None:
        """Test password without lowercase letter."""
        result = PasswordValidator.validate("UPPERCASE123!")
        assert result.is_valid is False
        assert "lowercase" in result.error_message.lower()

    def test_no_digit(self) -> None:
        """Test password without digit."""
        result = PasswordValidator.validate("NoDigitsHere!")
        assert result.is_valid is False
        assert "digit" in result.error_message.lower()

    def test_no_special_character(self) -> None:
        """Test password without special character."""
        result = PasswordValidator.validate("NoSpecialChar123")
        assert result.is_valid is False
        assert "special character" in result.error_message.lower()

    def test_special_characters_variety(self) -> None:
        """Test various special characters are accepted."""
        special_chars = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"]
        for char in special_chars:
            password = f"Test{char}123"
            result = PasswordValidator.validate(password)
            assert result.is_valid is True, f"Special char {char} should be accepted"

    def test_multiple_violations(self) -> None:
        """Test password with multiple violations returns first error."""
        result = PasswordValidator.validate("weak")
        assert result.is_valid is False
        # Should report first violation (length)
        assert "at least 8 characters" in result.error_message

    def test_empty_password(self) -> None:
        """Test empty password."""
        result = PasswordValidator.validate("")
        assert result.is_valid is False
        assert "at least 8 characters" in result.error_message

    def test_whitespace_only_password(self) -> None:
        """Test password with only whitespace."""
        result = PasswordValidator.validate("        ")
        assert result.is_valid is False
        # Should fail uppercase, lowercase, and digit requirements

    def test_password_with_spaces(self) -> None:
        """Test password containing spaces."""
        result = PasswordValidator.validate("Strong P@ss 123")
        assert result.is_valid is True

    def test_very_long_password(self) -> None:
        """Test very long password."""
        result = PasswordValidator.validate("A" * 100 + "a1!")  # Added lowercase
        assert result.is_valid is True

    def test_boundary_length(self) -> None:
        """Test password at boundary lengths."""
        # 7 characters - should fail
        result = PasswordValidator.validate("Aa1!aaa")
        assert result.is_valid is False

        # 8 characters - should pass (if other requirements met)
        result = PasswordValidator.validate("Aa1!aaaa")
        assert result.is_valid is True

    def test_all_requirements_minimal(self) -> None:
        """Test minimal password meeting all requirements."""
        # 8 chars: 1 upper, 1 lower, 1 digit, 1 special, 4 more chars
        result = PasswordValidator.validate("Aa1!bbbb")
        assert result.is_valid is True
