from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

convention = {
    "all_column_names": lambda constraint, table: "_".join(  # noqa: ARG005
        [column.name for column in constraint.columns.values()],
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}


class Base(DeclarativeBase):
    __abstract__ = True
    metadata = sa.MetaData(naming_convention=convention)


class CreatedMixin:
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
    )


class UpdatedMixin:
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        server_onupdate=sa.func.now(),
    )


class BaseWithDt(Base, CreatedMixin, UpdatedMixin):
    __abstract__ = True


table = Base.metadata
