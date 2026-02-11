from .services import UserService


class Backend:
    user: UserService

    def __init__(self):
        self.user = UserService()


back = Backend()
