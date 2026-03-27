"""Rate limiting module for authentication protection.

This module provides rate limiting functionality to protect against
brute-force attacks on authentication endpoints.
"""

from dataclasses import dataclass, field
import heapq
import threading
import time


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting.

    Attributes:
        max_attempts: Maximum number of attempts allowed.
        window_seconds: Time window in seconds.
        block_duration_seconds: How long to block after exceeding limit.
        max_records: Maximum records to keep in memory.
        cleanup_threshold: Number of records before triggering cleanup.
    """

    max_attempts: int = 5
    window_seconds: int = 300  # 5 minutes
    block_duration_seconds: int = 900  # 15 minutes
    max_records: int = 10000  # Max records in memory
    cleanup_threshold: int = 8000  # Cleanup when this many records


@dataclass
class AttemptRecord:
    """Record of authentication attempts.

    Attributes:
        timestamps: Min-heap of attempt timestamps for efficient cleanup.
        blocked_until: Timestamp when block expires (0 if not blocked).
    """

    timestamps: list[float] = field(default_factory=list)
    blocked_until: float = 0.0


class RateLimiter:
    """Rate limiter for authentication attempts.

    Tracks authentication attempts per identifier (email, IP) and
    enforces rate limits to prevent brute-force attacks.

    Thread-safe implementation with automatic cleanup to prevent memory leaks.
    """

    def __init__(self, config: RateLimitConfig | None = None) -> None:
        """Initialize rate limiter.

        Args:
            config: Rate limit configuration (uses defaults if not provided).
        """
        self.config = config or RateLimitConfig()
        self._records: dict[str, AttemptRecord] = {}
        self._lock = threading.RLock()
        self._cleanup_counter = 0

    def _clean_old_attempts(self, record: AttemptRecord, now: float) -> None:
        """Remove attempts outside the current time window.

        Args:
            record: Attempt record to clean.
            now: Current timestamp.
        """
        cutoff = now - self.config.window_seconds
        # Use heap for efficient removal of old timestamps
        while record.timestamps and record.timestamps[0] < cutoff:
            heapq.heappop(record.timestamps)

    def _maybe_cleanup(self) -> None:
        """Trigger cleanup if record count exceeds threshold.

        This method is called after each record modification to prevent
        unbounded memory growth.
        """
        self._cleanup_counter += 1
        # Only cleanup every 100th attempt when over threshold
        if (
            len(self._records) >= self.config.cleanup_threshold
            and self._cleanup_counter % 100 == 0
        ):
            self.cleanup_old_records()
            self._cleanup_counter = 0

    def is_blocked(self, identifier: str) -> bool:
        """Check if identifier is currently blocked.

        Args:
            identifier: Unique identifier (email or IP).

        Returns:
            True if blocked, False otherwise.
        """
        with self._lock:
            record = self._records.get(identifier)
            if record is None:
                return False

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
        with self._lock:
            if identifier not in self._records:
                self._records[identifier] = AttemptRecord()

            record = self._records[identifier]
            now = time.time()

            # Clean old attempts
            self._clean_old_attempts(record, now)

            # Record new attempt (use heap for efficient ordering)
            heapq.heappush(record.timestamps, now)

            # Check if limit exceeded
            if len(record.timestamps) > self.config.max_attempts:
                record.blocked_until = now + self.config.block_duration_seconds

            # Check if cleanup is needed
            self._maybe_cleanup()

    def get_remaining_attempts(self, identifier: str) -> int:
        """Get remaining attempts for identifier.

        Args:
            identifier: Unique identifier (email or IP).

        Returns:
            Number of remaining attempts, 0 if blocked.
        """
        with self._lock:
            if self.is_blocked(identifier):
                return 0

            record = self._records.get(identifier)
            if record is None:
                return self.config.max_attempts

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
        with self._lock:
            record = self._records.get(identifier)
            if record is None:
                return None

            now = time.time()

            if record.blocked_until > now:
                return int(record.blocked_until - now)

            return None

    def reset(self, identifier: str) -> None:
        """Reset rate limit for identifier (e.g., after successful login).

        Args:
            identifier: Unique identifier (email or IP).
        """
        with self._lock:
            if identifier in self._records:
                record = self._records[identifier]
                record.timestamps.clear()
                record.blocked_until = 0.0

    def cleanup_old_records(self) -> int:
        """Remove stale records from memory.

        Removes records that have no recent attempts and are not blocked.
        This prevents memory leaks from accumulating unused identifiers.

        Returns:
            Number of records removed.
        """
        with self._lock:
            now = time.time()
            now - self.config.window_seconds
            removed = 0

            keys_to_remove = []
            for identifier, record in self._records.items():
                # Keep if blocked or has recent attempts
                if record.blocked_until > now:
                    continue
                # Clean old timestamps first
                self._clean_old_attempts(record, now)
                if record.timestamps:
                    continue
                # Safe to remove
                keys_to_remove.append(identifier)

            for key in keys_to_remove:
                del self._records[key]
                removed += 1

            return removed

    def get_stats(self) -> dict:
        """Get rate limiter statistics.

        Returns:
            Dictionary with statistics about the rate limiter state.
        """
        with self._lock:
            now = time.time()
            blocked_count = 0
            active_count = 0

            for record in self._records.values():
                if record.blocked_until > now:
                    blocked_count += 1
                elif record.timestamps:
                    active_count += 1

            return {
                "total_records": len(self._records),
                "blocked": blocked_count,
                "active": active_count,
                "max_records": self.config.max_records,
            }


# Global rate limiter instance for authentication
_auth_rate_limiter: RateLimiter | None = None
_lock = threading.Lock()


def get_auth_rate_limiter() -> RateLimiter:
    """Get global authentication rate limiter.

    Returns:
        RateLimiter instance.
    """
    global _auth_rate_limiter
    if _auth_rate_limiter is None:
        with _lock:
            if _auth_rate_limiter is None:
                _auth_rate_limiter = RateLimiter()
    return _auth_rate_limiter


def reset_auth_rate_limiter() -> None:
    """Reset global rate limiter (useful for testing)."""
    global _auth_rate_limiter
    _auth_rate_limiter = None
