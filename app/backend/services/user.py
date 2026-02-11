from werkzeug.security import check_password_hash, generate_password_hash

from app.backend.database.models import User
from app.backend.domain import UserDto

from .base import BaseService, SqlService


class UserService(BaseService):
    def __init__(self):
        self.UserSQL = SqlService(model=User)
        super().__init__()

    def check_email_is_available(self, email):
        return not self.UserSQL.get_by(email=email)

    def to_dto(self, user_model: User):
        if user_model:
            return UserDto(
                id=user_model.id,
                email=user_model.email,
                first_name=user_model.first_name,
                last_name=user_model.last_name,
                sex=user_model.sex,
            )

    def create_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        sex: str = "NOT_SPECIFIED",
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
            return self.to_dto(user_model)
