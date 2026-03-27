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
from flask_login import current_user

from app.frontend.components.locale import LocaleStore

from .header import Header
from .navbar import NavBar
from .theme import NAVBAR_BREAKPOINT, NAVBAR_WIDTH, THEME

# =============================================================================
# Clientside callbacks for theme and navbar management
# =============================================================================
# Note: clientside_callback is used instead of @callback for
# performance - these functions execute entirely on the client side
# without server calls, providing instant UI response.
# =============================================================================

# Dark/Light theme toggle (clientside for instant switching)
clientside_callback(
    ClientsideFunction(
        namespace="app_shell",
        function_name="change_data_in_theme_store",
    ),
    Output("theme-store", "data"),
    Input("color-scheme-toggle", "n_clicks"),
    State("theme-store", "data"),
)

clientside_callback(
    ClientsideFunction(
        namespace="app_shell", function_name="change_mantine_theme_provider"
    ),
    Output("m2d-mantine-provider", "forceColorScheme"),
    Input("theme-store", "data"),
)

# Mobile navbar toggle (clientside for instant response)
clientside_callback(
    ClientsideFunction(namespace="app_shell", function_name="open_navbar"),
    Output("app-shell", "navbar"),
    Input("burger", "opened"),
    State("app-shell", "navbar"),
)


def AppShell() -> dmc.MantineProvider:
    """Main application shell (AppShell).

    Creates the main application layout with:
    - MantineProvider (theming)
    - Header (top bar)
    - Navbar (sidebar)
    - NotificationContainer (notifications)

    Returns:
        MantineProvider with full application structure.
    """
    return dmc.MantineProvider(
        id="m2d-mantine-provider",
        forceColorScheme="light",
        theme=THEME,
        children=[
            dcc.Store(id="theme-store", storage_type="local"),
            LocaleStore(),
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
                    "width": 0 if current_user.is_anonymous else NAVBAR_WIDTH,
                    "breakpoint": NAVBAR_BREAKPOINT,
                    "collapsed": {"mobile": True},
                },
            ),
        ],
    )
