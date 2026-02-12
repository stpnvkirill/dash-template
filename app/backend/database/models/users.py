from enum import Enum
import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy.orm as so

from .shared import Base, UpdatedMixin


class GenderEnum(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NOT_SPECIFIED = "NOT_SPECIFIED"


gender_enum = sa.Enum(
    GenderEnum,
    name="gender_enum",
    validate_strings=True,
)


class User(Base, UpdatedMixin):
    __tablename__ = "users"

    __table_args__ = (
        sa.CheckConstraint(
            "email = LOWER(email)",
            name="email_lowercase_check",
        ),
    )

    id: so.Mapped[uuid.UUID] = so.mapped_column(
        UUID(as_uuid=True),
        server_default=sa.func.uuidv7(),
        primary_key=True,
    )

    email: so.Mapped[str] = so.mapped_column(
        sa.VARCHAR(100),
        unique=True,
        index=True,
    )

    password: so.Mapped[str | None] = so.mapped_column(
        sa.VARCHAR(128),
    )

    first_name: so.Mapped[str | None] = so.mapped_column(
        sa.VARCHAR(100),
    )

    last_name: so.Mapped[str | None] = so.mapped_column(
        sa.VARCHAR(100),
    )

    sex: so.Mapped[GenderEnum] = so.mapped_column(
        gender_enum,
        server_default=GenderEnum.NOT_SPECIFIED.value,
        default=GenderEnum.NOT_SPECIFIED,
    )
