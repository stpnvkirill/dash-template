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


def _l(text_id):
    return html.Div(
        id={"type": "i18n", "id": text_id},
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
def load_translate(locale):
    try:
        with Path(f"./i18n/{locale}.json").open() as fp:
            return orjson.loads(fp.read())
    except:  # noqa: E722
        with Path("./i18n/en.json").open() as fp:
            return orjson.loads(fp.read())


clientside_callback(
    ClientsideFunction("i18n", "internalize"),
    Output({"type": "i18n", "id": MATCH}, "children"),
    Input("locale-store", "data"),
    State({"type": "i18n", "id": MATCH}, "id"),
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
