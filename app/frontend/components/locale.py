from datetime import datetime
from functools import lru_cache
from pathlib import Path
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
import orjson

from config import config

# Allowed locales for security (prevent path traversal)
ALLOWED_LOCALES = frozenset({"en", "ru"})
I18N_DIR = Path(__file__).parent.parent.parent.parent / "i18n"


def _get_locale_path(locale: str) -> Path:
    """Get safe path to locale file, preventing path traversal.

    Args:
        locale: Locale code (e.g., 'en', 'ru')

    Returns:
        Resolved path to locale JSON file.
    """
    # Sanitize locale: allow only alphanumeric and underscore
    safe_locale = "".join(c for c in locale if c.isalnum() or c == "_")

    # Check if locale is in allowed list
    if safe_locale not in ALLOWED_LOCALES:
        safe_locale = "en"

    # Build and resolve path
    locale_path = (I18N_DIR / f"{safe_locale}.json").resolve()

    # Ensure path is within i18n directory (defense in depth)
    if not str(locale_path).startswith(str(I18N_DIR.resolve())):
        locale_path = (I18N_DIR / "en.json").resolve()

    return locale_path


def _l(text_id):
    return html.Div(
        id={"type": "i18n", "id": text_id, "uuid": str(uuid4())},
        style={
            "display": "inline",
        },
    )


def _l_dt(dt: datetime, dt_format="L LT"):
    """
    dt_format: https://day.js.org/docs/en/display/format
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
    return dcc.Store(
        id="locale-store",
    )


@callback(
    Output("locale-store", "data"), Input("locale-selector", "value"), hidden=True
)
@lru_cache(maxsize=config.server.LRU_CACHE_MAXSIZE)
def load_translate(locale: str) -> dict:
    """Load translation file for the given locale.

    Args:
        locale: Locale code (e.g., 'en', 'ru')

    Returns:
        Dictionary with translations
    """
    try:
        locale_path = _get_locale_path(locale)
        with locale_path.open() as fp:
            return orjson.loads(fp.read())
    except FileNotFoundError, orjson.JSONDecodeError:
        # Fallback to English
        with (I18N_DIR / "en.json").open() as fp:
            return orjson.loads(fp.read())


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
