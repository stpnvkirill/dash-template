from dash import register_page, set_props
from flask_login import current_user

from app.error import UserNotAuthenticated

register_page(
    __name__,
    "/",
)


def layout():
    if current_user.is_anonymous:
        raise UserNotAuthenticated
    set_props(component_id="app-shell", props={"disabled": False})
    return ["Hello world"]
