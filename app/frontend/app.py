from dash import Dash
from flask import Flask

from .layout import AppShell


def create_dash(server: Flask) -> Dash:
    app = Dash(
        server=server,
        pages_folder="frontend/pages",
        suppress_callback_exceptions=True,
        compress=True,
    )
    app.layout = AppShell
    return app
