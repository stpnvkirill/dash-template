from dash import register_page, set_props
from dash_iconify import DashIconify
import dash_mantine_components as dmc
from flask_login import current_user

from app.error import UserNotAuthenticated
from app.frontend.components.forms import ProfileForm

register_page(
    __name__,
    "/me",
)


def layout(**kwargs):  # noqa: ARG001
    if not current_user.is_authenticated:
        raise UserNotAuthenticated()
    set_props(component_id="app-shell", props={"disabled": False})
    return dmc.Container(
        size=800,
        children=[
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.TabsTab(
                                "Profile",
                                value="profile",
                                leftSection=DashIconify(icon="tabler:photo"),
                            ),
                            dmc.TabsTab(
                                "Permission",
                                value="permission",
                                leftSection=DashIconify(icon="tabler:settings"),
                                disabled=True,
                            ),
                            dmc.TabsTab(
                                "Sessions",
                                value="sessions",
                                leftSection=DashIconify(icon="tabler:lock"),
                                disabled=True,
                            ),
                        ]
                    ),
                    dmc.TabsPanel(
                        ProfileForm(current_user),
                        value="profile",
                        pt="md",
                    ),
                ],
                value="profile",
            )
        ],
    )
