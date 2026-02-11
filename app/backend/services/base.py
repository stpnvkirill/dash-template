import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import DeclarativeBase

from app.backend.database import SessionManager


class SqlService:
    model: DeclarativeBase
    primary_key: str
    _sm: SessionManager

    def __init__(self, model, primary_key="id"):
        self.model = model
        self.primary_key = primary_key
        self._sm = SessionManager()

    @property
    def session(self):
        return self._sm.session()

    def get(self, id):
        with self.session as s:
            stmt = sa.select(self.model).where(
                getattr(self.model, self.primary_key) == id
            )
            return s.scalar(stmt)

    def get_by(self, **kwargs):
        with self.session as s:
            stmt = (
                sa.select(self.model)
                .where(*[getattr(self.model, k) == v for k, v in kwargs.items()])
                .limit(1)
            )
            return s.scalar(stmt)

    def select(self, *conditions):
        with self.session as s:
            stmt = sa.select(self.model).where(*conditions)
            return list(s.scalars(stmt))

    def upsert(self, id, **data):
        with self.session as s:
            data[self.primary_key] = id
            stmt = (
                pg_insert(self.model)
                .values(data)
                .on_conflict_do_update(index_elements=[self.primary_key], set_=data)
                .returning(self.model)
            )
            return s.scalar(stmt)

    def insert(self, **data):
        with self.session as s:
            stmt = pg_insert(self.model).values(data).returning(self.model)
            return s.scalar(stmt)

    def update(self, id, **data):
        with self.session as s:
            stmt = (
                sa.update(self.model)
                .where(getattr(self.model, self.primary_key) == id)
                .values(**data)
                .returning(self.model)
            )
            return s.scalar(stmt)


class BaseService:
    pass
