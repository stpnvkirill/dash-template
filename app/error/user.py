from dash import set_props

from .base import AppError


class UserNotAuthenticated(AppError):
    def __init__(self, next_page="/login", *args):
        self.next_page = next_page
        super().__init__(*args)

    def on_error(self):
        set_props("_pages_location", {"pathname": self.next_page, "search": ""})


class UserIsAuthenticated(AppError):
    def __init__(self, next_page="/", *args):
        self.next_page = next_page
        super().__init__(*args)

    def on_error(self):
        set_props("_pages_location", {"pathname": self.next_page, "search": ""})
