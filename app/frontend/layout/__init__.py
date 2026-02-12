from dash import (
    ClientsideFunction,
    Input,
    Output,
    State,
    clientside_callback,
    dcc,
    page_container,
)
import dash_mantine_components as dmc

from .header import Header
from .navbar import NavBar
from .theme import THEME

# Dark/Light theme
clientside_callback(
    ClientsideFunction(
        namespace="app_shell",
        function_name="change_data_in_theme_store",
    ),
    Output("theme-store", "data"),
    Input("color-scheme-toggle", "n_clicks"),
    State("theme-store", "data"),
    hidden=True,
)

clientside_callback(
    ClientsideFunction(
        namespace="app_shell", function_name="change_mantine_theme_provider"
    ),
    Output("m2d-mantine-provider", "forceColorScheme"),
    Input("theme-store", "data"),
    hidden=True,
)

# Mobile navbar toggle
clientside_callback(
    ClientsideFunction(namespace="app_shell", function_name="open_navbar"),
    Output("app-shell", "navbar"),
    Input("burger", "opened"),
    State("app-shell", "navbar"),
    hidden=True,
)


def AppShell():
    return dmc.MantineProvider(
        id="m2d-mantine-provider",
        forceColorScheme="light",
        theme=THEME,
        children=[
            dcc.Store(id="theme-store", storage_type="local"),
            dmc.AppShell(
                [
                    Header(),
                    NavBar(),
                    dmc.AppShellMain(
                        [
                            dmc.Container(page_container),
                            dmc.NotificationContainer(
                                id="notification-container",
                                sendNotifications=[],
                            ),
                        ],
                    ),
                ],
                id="app-shell",
                header={"height": 60},
                navbar={
                    "width": 300,
                    "breakpoint": "sm",
                    "collapsed": {"mobile": True},
                },
                disabled=True,
            ),
        ],
    )
