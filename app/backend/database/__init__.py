from contextlib import contextmanager

import sqlalchemy as sa
import sqlalchemy.orm as so

from config import config


class SessionManager:
    def __init__(self):
        self.engine = self.get_engine()
        self.session_factory = self.get_session_maker()

    def get_engine(self) -> sa.Engine:
        return sa.create_engine(
            url=config.database.database_url, echo=config.database.DB_ECHO
        )

    def get_session_maker(self):
        return so.sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
        )

    @contextmanager
    def session(self):
        with self.session_factory() as session:
            try:
                yield session
                session.commit()
            except Exception:
                session.rollback()
                raise

    def inject(self, func):
        def wrapper(*args, **kwargs):
            if "session" not in kwargs:
                with self.session_factory() as session:
                    kwargs["session"] = session
                    try:
                        res = func(*args, **kwargs)
                        session.commit()
                    except Exception:
                        session.rollback()
                        raise
                    else:
                        return res

            return func(*args, **kwargs)

        return wrapper
