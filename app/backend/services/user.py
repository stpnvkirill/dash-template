from typing import Literal
from uuid import UUID

import sqlalchemy as sa
from werkzeug.security import check_password_hash, generate_password_hash

from app.backend.database.models import OS, Browser, User, UserSession
from app.backend.domain import SessionDto, UserDto

from .base import BaseService, SqlService, pg_insert


class UserService(BaseService):
    def __init__(self):
        self.UserSQL = SqlService(model=User)
        self.SessionSQL = SqlService(model=UserSession)
        super().__init__()

    def check_email_is_available(self, email):
        return not self.UserSQL.get_by(email=email)

    def to_session_dto(self, session: UserSession):
        return SessionDto(
            id=session.id,
            is_active=session.is_active,
            os=session.os.name,
            browser=session.browser.name,
            ip=session.ip_address,
            last_active=session.last_activity,
        )

    def to_dto(self, user_model: User | UserDto, session: UserSession = None):
        if user_model:
            return UserDto(
                id=user_model.id,
                email=user_model.email,
                first_name=user_model.first_name,
                last_name=user_model.last_name,
                sex=user_model.sex
                if isinstance(user_model.sex, str)
                else user_model.sex.value,
                session=self.to_session_dto(session) if session is not None else None,
            )

    def create_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        sex: Literal["MALE", "FEMALE", "NOT_SPECIFIED"] = "NOT_SPECIFIED",
    ):
        if not self.check_email_is_available(email=email.lower()):
            return None
        hashed_password = generate_password_hash(password, method="pbkdf2")
        user_model: User = self.UserSQL.insert(
            email=email.lower(),
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            password=hashed_password,
        )
        return self.to_dto(user_model)

    def get_user(self, id):
        user_model: User = self.UserSQL.get(id=id)
        return self.to_dto(user_model)

    def auth(
        self,
        email: str,
        password: str,
        ip: str | None,
        os: str | None = None,
        browser: str | None = None,
    ):
        user_model: User = self.UserSQL.get_by(email=email.lower())
        if user_model and check_password_hash(user_model.password, password):
            return self.create_session(user=user_model, ip=ip, os=os, browser=browser)

    def get_user_by_session(self, session_id: UUID):
        with self.UserSQL.session as s:
            update_subq = (
                sa.update(UserSession)
                .where(
                    UserSession.id == session_id,
                    UserSession.is_active,
                )
                .values(
                    last_activity=sa.func.now(),
                    request_count=UserSession.request_count + 1,
                )
                .returning(UserSession.user_id)
                .cte("updated_session_ids")
            )

            stmt = sa.select(User).join(update_subq, User.id == update_subq.c.user_id)
            user = s.scalar(stmt)
            session = s.scalar(
                sa.select(UserSession).where(UserSession.id == session_id)
            )
            return self.to_dto(user, session)

    def create_session(
        self,
        user: UserDto | User,
        ip: str | None,
        os: str | None = None,
        browser: str | None = None,
    ):
        with self.UserSQL.session as s:
            os_name = sa.func.lower(os or "unknown")
            os_cte = (
                pg_insert(OS)
                .values(name=os_name)
                .on_conflict_do_update(index_elements=["name"], set_={"name": os_name})
                .returning(OS.id)
                .cte("os_cte")
            )
            browser_name = sa.func.lower(browser or "unknown")

            browser_cte = (
                pg_insert(Browser)
                .values(name=browser_name)
                .on_conflict_do_update(
                    index_elements=["name"], set_={"name": browser_name}
                )
                .returning(Browser.id)
                .cte("browser_cte")
            )
            session_id = s.scalar(
                pg_insert(UserSession)
                .values(
                    user_id=user.id,
                    ip_address=ip,
                    os_id=sa.select(os_cte.c.id).scalar_subquery(),
                    browser_id=sa.select(browser_cte.c.id).scalar_subquery(),
                )
                .returning(UserSession.id)
            )
            session: UserSession = s.scalar(
                sa.select(UserSession).where(UserSession.id == session_id)
            )
            if session:
                s.expunge(session)
                return self.to_dto(user_model=user, session=session)

    def deactivate_session(
        self,
        session_id: UUID,
    ):
        self.SessionSQL.update(id=session_id, is_active=False)

    def update_user(
        self,
        user_id: UUID,
        first_name: str,
        last_name: str,
        sex: str,
        password: str | None = None,
    ):
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "sex": sex or "NOT_SPECIFIED",
        }
        if password:
            hashed_password = generate_password_hash(password, method="pbkdf2")
            data["password"] = hashed_password
        user_model = self.UserSQL.update(id=user_id, **data)
        return self.to_dto(user_model)

    def get_active_session(self, user_id: UUID, exclude_id: UUID | None = None):
        conditions = [UserSession.id != exclude_id] if exclude_id else []
        sessions = self.SessionSQL.select(*conditions, is_active=True, user_id=user_id)
        return [self.to_session_dto(s) for s in sessions]
