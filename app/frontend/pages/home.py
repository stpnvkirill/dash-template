from dash import register_page
from flask_login import current_user

from app.error import UserNotAuthenticated

register_page(
    __name__,
    "/",
)


def layout():
    if current_user.is_anonymous:
        raise UserNotAuthenticated
    return ["Hello world"]
