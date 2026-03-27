"""Locale and internationalization components."""

from datetime import datetime
from uuid import uuid4

from dash import (
    MATCH,
    ClientsideFunction,
    Input,
    Output,
    State,
    callback,
    clientside_callback,
    dcc,
    html,
)

from app.backend.services.i18n import get_i18n_service


def _l(text_id: str):
    """Create a translatable text placeholder.

    Args:
        text_id: Translation key.

    Returns:
        HTML div with i18n attributes.
    """
    return html.Div(
        id={"type": "i18n", "id": text_id, "uuid": str(uuid4())},
        style={
            "display": "inline",
        },
    )


def _l_dt(dt: datetime, dt_format: str = "L LT"):
    """Create a translatable datetime placeholder.

    Args:
        dt: Datetime to format.
        dt_format: Day.js format string (default: "L LT").

    Returns:
        HTML div with datetime attributes.
    """
    return html.Div(
        id={
            "type": "dayjs",
            "timestamp": dt.timestamp() * 1000,
            "uuid": str(uuid4()),
            "format": dt_format,
        },
        style={
            "display": "inline",
        },
    )


def _l_dt_relative(dt: datetime):
    """Create a relative datetime placeholder.

    Args:
        dt: Datetime to format.

    Returns:
        HTML div with relative datetime attributes.
    """
    return html.Div(
        id={
            "type": "dayjs-relative",
            "timestamp": dt.timestamp() * 1000,
            "uuid": str(uuid4()),
        },
        style={
            "display": "inline",
        },
    )


def LocaleStore():
    """Create locale store component.

    Returns:
        Dash dcc.Store component for locale data.
    """
    return dcc.Store(
        id="locale-store",
    )


@callback(
    Output("locale-store", "data"), Input("locale-selector", "value"), hidden=True
)
def load_translate(locale: str) -> dict:
    """Load translation file for the given locale.

    Args:
        locale: Locale code (e.g., 'en', 'ru')

    Returns:
        Dictionary with translations
    """
    i18n_service = get_i18n_service()
    return i18n_service.get_translation(locale)


clientside_callback(
    ClientsideFunction("i18n", "internalize"),
    Output({"type": "i18n", "id": MATCH, "uuid": MATCH}, "children"),
    Input("locale-store", "data"),
    State({"type": "i18n", "id": MATCH, "uuid": MATCH}, "id"),
    hidden=True,
)

clientside_callback(
    ClientsideFunction("i18n", "internalize_dt"),
    Output(
        {"type": "dayjs", "timestamp": MATCH, "uuid": MATCH, "format": MATCH},
        "children",
    ),
    Input("locale-selector", "value"),
    State({"type": "dayjs", "timestamp": MATCH, "uuid": MATCH, "format": MATCH}, "id"),
    hidden=True,
)


clientside_callback(
    ClientsideFunction("i18n", "internalize_dt_relative"),
    Output(
        {"type": "dayjs-relative", "timestamp": MATCH, "uuid": MATCH},
        "children",
    ),
    Input("locale-selector", "value"),
    State({"type": "dayjs-relative", "timestamp": MATCH, "uuid": MATCH}, "id"),
    hidden=True,
)
