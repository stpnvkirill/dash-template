"""Infrastructure module for external dependencies.

This module contains implementations for database access, external services,
and other infrastructure concerns.
"""

from .database import SqlService

__all__ = ["SqlService"]
