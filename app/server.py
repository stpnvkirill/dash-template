from flask import Flask
from flask_login import LoginManager

from config import config

from .backend import back
from .frontend import create_dash
from .middleware import init_middlewares


def get_application():
    server = Flask(__name__)
    login_manager = LoginManager(server)
    server.config.from_object(config.server)
    init_middlewares(server)

    @login_manager.user_loader
    def load_user(session_id):
        user = back.user.get_user_by_session(session_id=session_id)
        return user

    return create_dash(server=server)
