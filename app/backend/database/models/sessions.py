import datetime as dt
from enum import Enum
from typing import ClassVar
import uuid as uuid_lib

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import INET, UUID
import sqlalchemy.orm as so

from .shared import Base


class OsEnum(Enum):
    WINDOWS = "WINDOWS"
    LINUX = "LINUX"
    MACOS = "MACOS"
    IOS = "IOS"
    ANDROID = "ANDROID"


os_enum = sa.Enum(
    OsEnum,
    name="os_enum",
    validate_strings=True,
)


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
        server_default=sa.func.now(),
    )
    is_active: so.Mapped[bool] = so.mapped_column(server_default="true")

    os: so.Mapped[OsEnum | None] = so.mapped_column(os_enum)
    ip_address: so.Mapped[str | None] = so.mapped_column(INET)
    request_count: so.Mapped[sa.Integer] = so.mapped_column(
        sa.Integer,
        server_default="0",
        default=0,
    )
