from typing import TYPE_CHECKING
import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy.orm as so

from .shared import Base, UpdatedMixin

if TYPE_CHECKING:
    pass

user_permissions = sa.Table(
    "user_permissions",
    Base.metadata,
    sa.Column(
        "user_id",
        UUID(as_uuid=True),
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    sa.Column(
        "permission_id",
        UUID(as_uuid=True),
        sa.ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

user_permission_groups = sa.Table(
    "user_permission_groups",
    Base.metadata,
    sa.Column(
        "user_id",
        UUID(as_uuid=True),
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    sa.Column(
        "group_id",
        UUID(as_uuid=True),
        sa.ForeignKey("permission_groups.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

permission_group_permissions = sa.Table(
    "permission_group_permissions",
    Base.metadata,
    sa.Column(
        "group_id",
        UUID(as_uuid=True),
        sa.ForeignKey("permission_groups.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    sa.Column(
        "permission_id",
        UUID(as_uuid=True),
        sa.ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Permission(Base, UpdatedMixin):
    """Permission identified by unique (category, key)."""

    __tablename__ = "permissions"

    __table_args__ = (sa.UniqueConstraint("category", "key"),)

    id: so.Mapped[uuid.UUID] = so.mapped_column(
        UUID(as_uuid=True),
        server_default=sa.func.uuidv7(),
        primary_key=True,
    )

    category: so.Mapped[str] = so.mapped_column(sa.VARCHAR(100), nullable=False)
    key: so.Mapped[str] = so.mapped_column(sa.VARCHAR(100), nullable=False)


class PermissionGroup(Base, UpdatedMixin):
    """Permission group; system groups have unique key."""

    __tablename__ = "permission_groups"

    id: so.Mapped[uuid.UUID] = so.mapped_column(
        UUID(as_uuid=True),
        server_default=sa.func.uuidv7(),
        primary_key=True,
    )
    name: so.Mapped[str] = so.mapped_column(sa.VARCHAR(200))

    system_key: so.Mapped[str | None] = so.mapped_column(sa.VARCHAR(50), unique=True)
