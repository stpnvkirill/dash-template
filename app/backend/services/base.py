"""Base service class for business logic.

This module contains the base class for all services. Services should use
repositories for data access, not SqlService directly.
"""

from app.backend.database import SessionManager


class BaseService:
    """Base class for all business logic services.

    Provides a session_scope context manager for database operations
    that need to span multiple repository calls.
    """

    def session_scope(self) -> SessionManager:
        """Get database session context manager.

        Returns:
            SessionManager context manager for database transactions.
        """
        return SessionManager().session()
