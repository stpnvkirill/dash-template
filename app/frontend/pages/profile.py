from dash import Input, Output, callback, register_page
from dash_iconify import DashIconify
import dash_mantine_components as dmc
from flask_login import current_user

from app.error import UserNotAuthenticated
from app.frontend.components.locale import _l
from app.frontend.components.profile import PermissionsTab, ProfileForm, SessionTab

register_page(
    __name__,
    "/me",
)


def layout(**kwargs):
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
                            ),
                        ]
                    ),
                ],
                value="profile",
                id="profilepage-tabs",
            ),
            dmc.Box(id="profilepage-tabbox", pt="md"),
        ],
    )


@callback(Output("profilepage-tabbox", "children"), Input("profilepage-tabs", "value"))
def render_tab_content(active):
    if active == "profile":
        return ProfileForm(current_user)
    elif active == "sessions":
        return SessionTab(current_user)
    elif active == "permission":
        return PermissionsTab(current_user)

    return dmc.Box()
