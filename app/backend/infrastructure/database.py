"""Database service for low-level SQL operations.

This module provides a thin wrapper around SQLAlchemy for basic CRUD operations.
It should only be used by repositories, not by services directly.
"""

from typing import Any

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import DeclarativeBase

from app.backend.database import SessionManager


class SqlService:
    """Service for executing raw SQL operations.

    This is a low-level database service that should only be used by repositories.
    Services should use repositories instead of calling this service directly.

    Attributes:
        model: SQLAlchemy model class for operations.
        primary_key: Name of the primary key column.
    """

    _session_manager: SessionManager = SessionManager()

    def __init__(self, model: type[DeclarativeBase], primary_key: str = "id") -> None:
        """Initialize SqlService with a model.

        Args:
            model: SQLAlchemy model class for operations.
            primary_key: Name of the primary key column (default: 'id').
        """
        self.model: type[DeclarativeBase] = model
        self.primary_key: str = primary_key

    @property
    def session(self) -> SessionManager:
        """Get session manager context."""
        return self._session_manager

    def get(self, id: Any) -> DeclarativeBase | None:
        """Get object by primary key.

        Args:
            id: Primary key value.

        Returns:
            Model instance or None if not found.
        """
        with self.session.session() as s:
            stmt = sa.select(self.model).where(
                getattr(self.model, self.primary_key) == id
            )
            return s.scalar(stmt)

    def get_by(self, **kwargs: Any) -> DeclarativeBase | None:
        """Get object by filter conditions.

        Args:
            **kwargs: Filter conditions as keyword arguments.

        Returns:
            Model instance or None if not found.
        """
        with self.session.session() as s:
            stmt = (
                sa.select(self.model)
                .where(*[getattr(self.model, k) == v for k, v in kwargs.items()])
                .limit(1)
            )
            return s.scalar(stmt)

    def select(self, *conditions: Any, **kwargs: Any) -> list[DeclarativeBase]:
        """Select multiple objects with optional conditions.

        Args:
            *conditions: SQLAlchemy WHERE conditions.
            **kwargs: Additional filter conditions.

        Returns:
            List of model instances.
        """
        with self.session.session() as s:
            stmt = (
                sa.select(self.model)
                .where(*conditions)
                .where(*[getattr(self.model, k) == v for k, v in kwargs.items()])
            )
            return list(s.scalars(stmt))

    def upsert(self, id: Any, **data: Any) -> DeclarativeBase:
        """Insert or update object by primary key.

        Args:
            id: Primary key value.
            **data: Field values to insert/update.

        Returns:
            Model instance after insert/update.
        """
        with self.session.session() as s:
            data[self.primary_key] = id
            stmt = (
                pg_insert(self.model)
                .values(data)
                .on_conflict_do_update(index_elements=[self.primary_key], set_=data)
                .returning(self.model)
            )
            return s.scalar(stmt)

    def insert_or_update(
        self,
        index_elements: list[str],
        only_stmt: bool = False,
        **data: Any,
    ) -> DeclarativeBase | sa.Insert | sa.Update:
        """Insert or update object with custom conflict resolution.

        Args:
            index_elements: Columns to check for conflicts.
            only_stmt: If True, return statement without executing.
            **data: Field values to insert/update.

        Returns:
            Model instance after insert/update, or SQL statement if only_stmt=True.
        """
        stmt = (
            pg_insert(self.model)
            .values(data)
            .on_conflict_do_update(index_elements=index_elements, set_=data)
            .returning(self.model)
        )
        if only_stmt:
            return stmt
        with self.session.session() as s:
            return s.scalar(stmt)

    def insert(self, **data: Any) -> DeclarativeBase:
        """Insert new object.

        Args:
            **data: Field values to insert.

        Returns:
            Created model instance.
        """
        with self.session.session() as s:
            stmt = pg_insert(self.model).values(data).returning(self.model)
            return s.scalar(stmt)

    def update(self, id: Any, **data: Any) -> DeclarativeBase | None:
        """Update object by primary key.

        Args:
            id: Primary key value.
            **data: Field values to update.

        Returns:
            Updated model instance or None if not found.
        """
        with self.session.session() as s:
            stmt = (
                sa.update(self.model)
                .where(getattr(self.model, self.primary_key) == id)
                .values(**data)
                .returning(self.model)
            )
            return s.scalar(stmt)

    def delete(self, id: Any) -> bool:
        """Delete object by primary key.

        Args:
            id: Primary key value.

        Returns:
            True if object was deleted, False if not found.
        """
        with self.session.session() as s:
            stmt = sa.delete(self.model).where(
                getattr(self.model, self.primary_key) == id
            )
            result = s.execute(stmt)
            return result.rowcount > 0
