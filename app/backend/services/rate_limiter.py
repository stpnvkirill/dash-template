"""Rate limiting module for authentication protection.

This module provides rate limiting functionality to protect against
brute-force attacks on authentication endpoints.
"""

from collections import defaultdict
from dataclasses import dataclass, field
import time


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting.

    Attributes:
        max_attempts: Maximum number of attempts allowed.
        window_seconds: Time window in seconds.
        block_duration_seconds: How long to block after exceeding limit.
    """

    max_attempts: int = 5
    window_seconds: int = 300  # 5 minutes
    block_duration_seconds: int = 900  # 15 minutes


@dataclass
class AttemptRecord:
    """Record of authentication attempts.

    Attributes:
        timestamps: List of attempt timestamps.
        blocked_until: Timestamp when block expires (0 if not blocked).
    """

    timestamps: list[float] = field(default_factory=list)
    blocked_until: float = 0.0


class RateLimiter:
    """Rate limiter for authentication attempts.

    Tracks authentication attempts per identifier (email, IP) and
    enforces rate limits to prevent brute-force attacks.
    """

    def __init__(self, config: RateLimitConfig | None = None) -> None:
        """Initialize rate limiter.

        Args:
            config: Rate limit configuration (uses defaults if not provided).
        """
        self.config = config or RateLimitConfig()
        self._records: defaultdict[str, AttemptRecord] = defaultdict(AttemptRecord)

    def _clean_old_attempts(self, record: AttemptRecord, now: float) -> None:
        """Remove attempts outside the current time window.

        Args:
            record: Attempt record to clean.
            now: Current timestamp.
        """
        cutoff = now - self.config.window_seconds
        record.timestamps = [ts for ts in record.timestamps if ts > cutoff]

    def is_blocked(self, identifier: str) -> bool:
        """Check if identifier is currently blocked.

        Args:
            identifier: Unique identifier (email or IP).

        Returns:
            True if blocked, False otherwise.
        """
        record = self._records[identifier]
        now = time.time()

        if record.blocked_until > now:
            return True

        # Block expired, reset
        if record.blocked_until > 0 and record.blocked_until <= now:
            record.blocked_until = 0.0
            record.timestamps.clear()

        return False

    def record_attempt(self, identifier: str) -> None:
        """Record an authentication attempt.

        Args:
            identifier: Unique identifier (email or IP).
        """
        record = self._records[identifier]
        now = time.time()

        # Clean old attempts
        self._clean_old_attempts(record, now)

        # Record new attempt
        record.timestamps.append(now)

        # Check if limit exceeded
        if len(record.timestamps) > self.config.max_attempts:
            record.blocked_until = now + self.config.block_duration_seconds

    def get_remaining_attempts(self, identifier: str) -> int:
        """Get remaining attempts for identifier.

        Args:
            identifier: Unique identifier (email or IP).

        Returns:
            Number of remaining attempts, 0 if blocked.
        """
        if self.is_blocked(identifier):
            return 0

        record = self._records[identifier]
        now = time.time()
        self._clean_old_attempts(record, now)

        return max(0, self.config.max_attempts - len(record.timestamps))

    def get_retry_after(self, identifier: str) -> int | None:
        """Get seconds until retry is allowed.

        Args:
            identifier: Unique identifier (email or IP).

        Returns:
            Seconds to wait, None if not blocked.
        """
        record = self._records[identifier]
        now = time.time()

        if record.blocked_until > now:
            return int(record.blocked_until - now)

        return None

    def reset(self, identifier: str) -> None:
        """Reset rate limit for identifier (e.g., after successful login).

        Args:
            identifier: Unique identifier (email or IP).
        """
        if identifier in self._records:
            record = self._records[identifier]
            record.timestamps.clear()
            record.blocked_until = 0.0


# Global rate limiter instance for authentication
_auth_rate_limiter: RateLimiter | None = None


def get_auth_rate_limiter() -> RateLimiter:
    """Get global authentication rate limiter.

    Returns:
        RateLimiter instance.
    """
    global _auth_rate_limiter  # noqa: PLW0603
    if _auth_rate_limiter is None:
        _auth_rate_limiter = RateLimiter()
    return _auth_rate_limiter


def reset_auth_rate_limiter() -> None:
    """Reset global rate limiter (useful for testing)."""
    global _auth_rate_limiter  # noqa: PLW0603
    _auth_rate_limiter = None
