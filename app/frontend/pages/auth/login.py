import dash
import dash_mantine_components as dmc
from flask_login import current_user

from app.error import UserIsAuthenticated
from app.frontend.components.forms import LoginForm

dash.register_page(__name__, path="/login")


def login_form(next_page):
    return dmc.Grid(
        [
            dmc.GridCol(span={"xs": 0, "sm": 3}),
            dmc.GridCol(
                dmc.Stack(
                    [
                        dmc.Title("Welcome back!", order=2, w="100%", ta="center"),
                        dmc.Text(
                            [
                                "Do not have an account yet? ",
                                dmc.Anchor("Create account", href="/reg"),
                            ],
                            w="100%",
                            ta="center",
                            mb="lg",
                        ),
                        dmc.Paper(
                            w="100%", maw=500, children=LoginForm(next_page), mx="auto"
                        ),
                    ]
                ),
                span={"xs": 12, "sm": 6},
                pt="xl",
            ),
            dmc.GridCol(span={"xs": 0, "sm": 3}),
        ],
        mih="70vh",
    )


def layout(**kwargs):
    if current_user.is_authenticated:
        raise UserIsAuthenticated(next_page=kwargs.get("next", "/"))
    dash.set_props(component_id="app-shell", props={"disabled": True})
    return login_form(next_page=kwargs.get("next", "/"))
