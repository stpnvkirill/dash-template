import dash
from flask_login import current_user, logout_user

from app.backend import back

dash.register_page(__name__, path="/logout")


def layout(**kwargs):  # noqa: ARG001
    if current_user.is_authenticated:
        back.user.deactivate_session(session_id=current_user.get_id())
        logout_user()

    return dash.dcc.Location(pathname="/login", id="redirect-to-login")
