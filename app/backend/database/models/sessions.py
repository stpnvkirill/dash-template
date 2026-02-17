import datetime as dt
from typing import ClassVar
import uuid as uuid_lib

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import INET, UUID
import sqlalchemy.orm as so

from .shared import Base


class OS(Base):
    __tablename__: ClassVar = "operating_systems"
    __table_args__ = (
        sa.CheckConstraint(
            "name = LOWER(name)",
            name="os_name_lowercase_check",
        ),
    )

    id: so.Mapped[int] = so.mapped_column(
        sa.SmallInteger,
        primary_key=True,
    )
    name: so.Mapped[str] = so.mapped_column(unique=True)


class Browser(Base):
    __tablename__: ClassVar = "browsers"
    __table_args__ = (
        sa.CheckConstraint(
            "name = LOWER(name)",
            name="browser_name_lowercase_check",
        ),
    )

    id: so.Mapped[int] = so.mapped_column(
        sa.SmallInteger,
        primary_key=True,
    )
    name: so.Mapped[str] = so.mapped_column(unique=True)


class UserSession(Base):
    __tablename__: ClassVar = "user_sessions"

    id: so.Mapped[uuid_lib.UUID] = so.mapped_column(
        UUID,
        server_default=sa.func.uuidv7(),
        primary_key=True,
    )

    user_id: so.Mapped[uuid_lib.UUID] = so.mapped_column(
        UUID,
        sa.ForeignKey("users.id", ondelete="CASCADE"),
    )

    last_activity: so.Mapped[dt.datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
    )
    is_active: so.Mapped[bool] = so.mapped_column(server_default="true")

    os_id: so.Mapped[int] = so.mapped_column(sa.SmallInteger, sa.ForeignKey(OS.id))
    browser_id: so.Mapped[int] = so.mapped_column(
        sa.SmallInteger, sa.ForeignKey(Browser.id)
    )
    ip_address: so.Mapped[str | None] = so.mapped_column(INET)
    request_count: so.Mapped[sa.Integer] = so.mapped_column(
        sa.Integer,
        server_default="0",
        default=0,
    )

    os: so.Mapped[OS] = so.relationship(lazy="joined")
    browser: so.Mapped[Browser] = so.relationship(lazy="joined")
