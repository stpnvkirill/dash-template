from dash_iconify import DashIconify
import dash_mantine_components as dmc
from flask_login import current_user

from .theme import NAVBAR_WIDTH


def UserSection() -> dmc.NavLink:
    """User profile navigation link in navbar.

    Returns:
        NavLink with user name, email and icon.
    """
    return dmc.NavLink(
        id="user-section-navbar",
        label=f"{current_user.first_name} {current_user.last_name}",
        description=current_user.email,
        bdrs=0,
        m=0,
        leftSection=dmc.ActionIcon(
            DashIconify(icon="mdi:user"),
            variant="light",
            size="lg",
            radius="xl",
        ),
        rightSection=DashIconify(icon="tabler-chevron-right"),
        disableRightSectionRotation=True,
        href="/me",
    )


def get_icon(icon: str, variant: str = "light") -> dmc.ActionIcon:
    """Create navigation icon.

    Args:
        icon: Icon name (e.g., "tabler:home").
        variant: Icon style (light, filled, outline).

    Returns:
        ActionIcon with specified icon.
    """
    return dmc.ActionIcon(DashIconify(icon=icon, height=16), variant=variant)


def NavBar() -> dmc.AppShellNavbar | dmc.Box:
    """Application sidebar navigation.

    Returns:
        AppShellNavbar with navigation links or empty Box
        for unauthenticated users.
    """
    if current_user.is_anonymous:
        return dmc.Box()

    return dmc.AppShellNavbar(
        p=0,
        bg="var(--ui-paper-color)",
        w=NAVBAR_WIDTH,
        children=[
            dmc.AppShellSection(
                [dmc.Skeleton(height=35, mt="sm", animate=False) for _ in range(8)],
                grow=True,
                p="xs",
            ),
            dmc.AppShellSection(children=[dmc.Divider(), UserSection()]),
        ],
    )
