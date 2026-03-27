from dash_iconify import DashIconify
import dash_mantine_components as dmc
from flask_login import current_user

from app.frontend.components.shared import LanguagePicker

from .theme import HEADER_HEIGHT


def ChangeColorIcon() -> dmc.ActionIcon:
    """Theme toggle icon (light/dark).

    Returns:
        ActionIcon with sun and moon icons.
    """
    return dmc.ActionIcon(
        [
            DashIconify(
                icon="akar-icons:sun",
                width=25,
                id="light-theme-icon",
                color="yellow",
            ),
            DashIconify(
                icon="akar-icons:moon",
                width=25,
                id="dark-theme-icon",
                color="gray",
            ),
        ],
        variant="transparent",
        id="color-scheme-toggle",
        size="lg",
    )


def CallNavbarIcon() -> dmc.Burger | dmc.Box:
    """Burger icon for opening navbar on mobile.

    Returns:
        Burger component or hidden Box for unauthenticated users.
    """
    if current_user.is_anonymous:
        return dmc.Box(display="none")
    return dmc.Burger(id="burger", size="sm", hiddenFrom="sm", opened=False)


def Header() -> dmc.AppShellHeader:
    """Application header.

    Returns:
        AppShellHeader with logo, language and theme toggles.
    """
    return dmc.AppShellHeader(
        dmc.Group(
            justify="space-between",
            children=[
                dmc.Group(
                    [
                        dmc.Anchor(
                            dmc.Group(
                                [
                                    dmc.Image(
                                        src="/assets/logo-dark.svg",
                                        h=36,
                                        fit="contain",
                                        lightHidden=True,
                                    ),
                                    dmc.Image(
                                        src="/assets/logo.svg",
                                        h=36,
                                        fit="contain",
                                        darkHidden=True,
                                    ),
                                ]
                            ),
                            href="/",
                        )
                    ],
                    align="center",
                    pl="sm",
                ),
                dmc.Group(
                    justify="flex-end",
                    children=[LanguagePicker(), ChangeColorIcon(), CallNavbarIcon()],
                ),
            ],
        ),
        bg="var(--ui-paper-color)",
        h=HEADER_HEIGHT,
    )
