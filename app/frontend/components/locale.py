from functools import lru_cache
from pathlib import Path

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


def _l(text_id):
    return html.Div(id={"type": "i18n", "id": text_id})


def LocaleStore():
    return dcc.Store(
        id="locale-store",
    )


@callback(
    Output("locale-store", "data"), Input("locale-selector", "value"), hidden=True
)
@lru_cache
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
