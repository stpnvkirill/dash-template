from typing import Literal
from uuid import UUID

import sqlalchemy as sa
from werkzeug.security import check_password_hash, generate_password_hash

from app.backend.database.models import User, UserSession
from app.backend.domain import SessionDto, UserDto

from .base import BaseService, SqlService


class UserService(BaseService):
    def __init__(self):
        self.UserSQL = SqlService(model=User)
        self.SessionSQL = SqlService(model=UserSession)
        super().__init__()

    def check_email_is_available(self, email):
        return not self.UserSQL.get_by(email=email)

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
                session=SessionDto(
                    id=session.id,
                    is_active=session.is_active,
                    os=session.os,
                    ip=session.ip_address,
                )
                if session is not None
                else None,
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

    def auth(self, email, password):
        user_model: User = self.UserSQL.get_by(email=email.lower())
        if user_model and check_password_hash(user_model.password, password):
            return self.create_session(user=user_model)

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
        ip: str | None = None,
        os: Literal["WINDOWS", "LINUX", "MACOS", "IOS", "ANDROID"] | None = None,
    ):
        session: UserSession = self.SessionSQL.insert(
            user_id=user.id, ip_address=ip, os=os
        )
        if session:
            return self.to_dto(user_model=user, session=session)

    def deactivate_session(
        self,
        session_id: UUID,
    ):
        self.SessionSQL.update(id=session_id, is_active=False)
