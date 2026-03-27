"""Unit tests for RateLimiter."""

import time

import pytest

from app.backend.services.rate_limiter import (
    RateLimitConfig,
    RateLimiter,
    get_auth_rate_limiter,
    reset_auth_rate_limiter,
)


class TestRateLimitConfig:
    """Tests for RateLimitConfig."""

    def test_default_config(self) -> None:
        """Test default configuration values."""
        config = RateLimitConfig()
        assert config.max_attempts == 5
        assert config.window_seconds == 300
        assert config.block_duration_seconds == 900

    def test_custom_config(self) -> None:
        """Test custom configuration values."""
        config = RateLimitConfig(
            max_attempts=3,
            window_seconds=60,
            block_duration_seconds=300,
        )
        assert config.max_attempts == 3
        assert config.window_seconds == 60
        assert config.block_duration_seconds == 300


class TestRateLimiter:
    """Tests for RateLimiter."""

    @pytest.fixture
    def limiter(self) -> RateLimiter:
        """Create rate limiter with test configuration."""
        return RateLimiter(
            RateLimitConfig(
                max_attempts=3,
                window_seconds=60,
                block_duration_seconds=300,
            )
        )

    def test_initial_state_not_blocked(self, limiter: RateLimiter) -> None:
        """Test that new identifier is not blocked."""
        assert not limiter.is_blocked("test@example.com")

    def test_record_attempt(self, limiter: RateLimiter) -> None:
        """Test recording authentication attempts."""
        identifier = "test@example.com"

        # Record 3 attempts (limit)
        for _ in range(3):
            limiter.record_attempt(identifier)
            assert not limiter.is_blocked(identifier)

        # 4th attempt should trigger block
        limiter.record_attempt(identifier)
        assert limiter.is_blocked(identifier)

    def test_get_remaining_attempts(self, limiter: RateLimiter) -> None:
        """Test getting remaining attempts."""
        identifier = "test@example.com"

        assert limiter.get_remaining_attempts(identifier) == 3

        limiter.record_attempt(identifier)
        assert limiter.get_remaining_attempts(identifier) == 2

        limiter.record_attempt(identifier)
        assert limiter.get_remaining_attempts(identifier) == 1

        limiter.record_attempt(identifier)
        assert limiter.get_remaining_attempts(identifier) == 0

    def test_get_retry_after(self, limiter: RateLimiter) -> None:
        """Test getting retry after time."""
        identifier = "test@example.com"

        # Not blocked - should return None
        assert limiter.get_retry_after(identifier) is None

        # Exceed limit
        for _ in range(4):
            limiter.record_attempt(identifier)

        # Should return seconds until unblock
        retry_after = limiter.get_retry_after(identifier)
        assert retry_after is not None
        assert retry_after > 0
        assert retry_after <= 300  # block_duration_seconds

    def test_reset(self, limiter: RateLimiter) -> None:
        """Test resetting rate limit."""
        identifier = "test@example.com"

        # Exceed limit
        for _ in range(4):
            limiter.record_attempt(identifier)

        assert limiter.is_blocked(identifier)

        # Reset
        limiter.reset(identifier)

        assert not limiter.is_blocked(identifier)
        assert limiter.get_remaining_attempts(identifier) == 3

    def test_window_expiration(self, limiter: RateLimiter) -> None:
        """Test that old attempts expire after window."""
        identifier = "test@example.com"

        # Record 2 attempts
        limiter.record_attempt(identifier)
        limiter.record_attempt(identifier)

        assert limiter.get_remaining_attempts(identifier) == 1

        # Wait for window to expire (simulate by cleaning old attempts)
        # In real scenario, we'd use time.sleep(), but for unit tests
        # we verify the logic through the clean method
        limiter._clean_old_attempts(
            limiter._records[identifier],
            time.time() + 61,  # Window + 1 second
        )

        assert limiter.get_remaining_attempts(identifier) == 3

    def test_multiple_identifiers(self, limiter: RateLimiter) -> None:
        """Test that different identifiers are tracked separately."""
        limiter.record_attempt("user1@example.com")
        limiter.record_attempt("user2@example.com")

        assert limiter.get_remaining_attempts("user1@example.com") == 2
        assert limiter.get_remaining_attempts("user2@example.com") == 2

        # Block user1 (need 3 more to exceed limit of 3)
        limiter.record_attempt("user1@example.com")
        limiter.record_attempt("user1@example.com")
        limiter.record_attempt("user1@example.com")

        assert limiter.is_blocked("user1@example.com")
        assert not limiter.is_blocked("user2@example.com")

    def test_ip_identifier(self, limiter: RateLimiter) -> None:
        """Test IP-based rate limiting."""
        ip_identifier = "ip:192.168.1.1"

        for _ in range(3):
            limiter.record_attempt(ip_identifier)

        assert limiter.get_remaining_attempts(ip_identifier) == 0

        limiter.record_attempt(ip_identifier)
        assert limiter.is_blocked(ip_identifier)


class TestGlobalRateLimiter:
    """Tests for global rate limiter functions."""

    def teardown_method(self) -> None:
        """Reset global rate limiter after each test."""
        reset_auth_rate_limiter()

    def test_get_auth_rate_limiter_singleton(self) -> None:
        """Test that get_auth_rate_limiter returns singleton."""
        limiter1 = get_auth_rate_limiter()
        limiter2 = get_auth_rate_limiter()

        assert limiter1 is limiter2

    def test_reset_auth_rate_limiter(self) -> None:
        """Test resetting global rate limiter."""
        limiter1 = get_auth_rate_limiter()
        reset_auth_rate_limiter()
        limiter2 = get_auth_rate_limiter()

        assert limiter1 is not limiter2


class TestRateLimiterConfig:
    """Tests for rate limiting configuration."""

    def test_rate_limiting_enabled_by_default(self) -> None:
        """Test that rate limiting is enabled by default."""
        from config import config

        assert config.server.ENABLE_RATE_LIMITING is True
