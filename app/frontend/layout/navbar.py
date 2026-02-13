from dash_iconify import DashIconify
import dash_mantine_components as dmc
from flask_login import current_user


def UserSection():
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


def get_icon(icon, variant="light"):
    return dmc.ActionIcon(DashIconify(icon=icon, height=16), variant=variant)


def NavBar():
    if current_user.is_anonymous:
        return dmc.Box()
    return dmc.AppShellNavbar(
        p=0,
        bg="var(--ui-paper-color)",
        children=[
            dmc.AppShellSection(
                [dmc.Skeleton(height=35, mt="sm", animate=False) for _ in range(8)],
                grow=True,
                p="xs",
            ),
            dmc.AppShellSection(children=[dmc.Divider(), UserSection()]),
        ],
    )
