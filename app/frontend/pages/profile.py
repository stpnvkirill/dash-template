from dash import register_page
from dash_iconify import DashIconify
import dash_mantine_components as dmc
from flask_login import current_user

from app.error import UserNotAuthenticated
from app.frontend.components.forms import ProfileForm
from app.frontend.components.locale import _l
from app.frontend.components.session import SessionTab

register_page(
    __name__,
    "/me",
)


def layout(**kwargs):  # noqa: ARG001
    if not current_user.is_authenticated:
        raise UserNotAuthenticated()
    return dmc.Container(
        size=800,
        children=[
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.TabsTab(
                                _l("profilepage_tab_profile_name"),
                                value="profile",
                                leftSection=DashIconify(icon="tabler:photo"),
                            ),
                            dmc.TabsTab(
                                _l("profilepage_tab_sessions_name"),
                                value="sessions",
                                leftSection=DashIconify(icon="tabler:lock"),
                            ),
                            dmc.TabsTab(
                                _l("profilepage_tab_permission_name"),
                                value="permission",
                                leftSection=DashIconify(icon="tabler:settings"),
                                disabled=True,
                            ),
                        ]
                    ),
                    dmc.TabsPanel(
                        ProfileForm(current_user),
                        value="profile",
                        pt="md",
                    ),
                    dmc.TabsPanel(
                        SessionTab(current_user),
                        value="sessions",
                        pt="md",
                    ),
                ],
                value="profile",
            )
        ],
    )
