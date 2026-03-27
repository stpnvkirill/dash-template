"""Flask application factory.

This module creates and configures the Flask/Dash application.
"""

from flask import Flask
from flask_login import LoginManager

from config import config

from .backend import back
from .frontend import create_dash
from .middleware import init_middlewares


def get_application() -> Flask:
    """Create and configure the application.

    Returns:
        Configured Flask/Dash application instance.
    """
    server = Flask(__name__)
    login_manager = LoginManager(server)
    server.config.from_object(config.server)
    init_middlewares(server)

    @login_manager.user_loader
    def load_user(session_id: str):
        """Load user from session for Flask-Login.

        Args:
            session_id: Session ID from cookie.

        Returns:
            UserDto if session is valid, None otherwise.
        """
        # Lazy loading: permissions are loaded on-demand via flask.g
        user = back.user.get_user_by_session(
            session_id=session_id,
            load_permissions=False,
        )
        return user

    return create_dash(server=server)
