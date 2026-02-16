from dash import Dash
from flask import Flask

from app.error import error_handler

from .layout import AppShell


def create_dash(server: Flask) -> Dash:
    app = Dash(
        server=server,
        pages_folder="frontend/pages",
        suppress_callback_exceptions=True,
        compress=True,
        on_error=error_handler,
        external_scripts=[
            "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.11.18/dayjs.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.11.18/plugin/relativeTime.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.11.18/plugin/localizedFormat.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.11.18/locale/ru.min.js",
        ],
    )
    app.layout = AppShell
    return app
