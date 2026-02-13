import dash
import dash_mantine_components as dmc
from flask_login import current_user

from app.frontend.components.forms import RegForm

dash.register_page(__name__, path="/reg")


def login_form(next_page):
    return dmc.Grid(
        [
            dmc.GridCol(span={"xs": 0, "sm": 3}),
            dmc.GridCol(
                dmc.Stack(
                    [
                        dmc.Title(
                            "Registration in the system", order=2, w="100%", ta="center"
                        ),
                        dmc.Text(
                            [
                                "It will take a little information about you",
                            ],
                            w="100%",
                            ta="center",
                            mb="lg",
                        ),
                        dmc.Paper(
                            w="100%", maw=500, children=RegForm(next_page), mx="auto"
                        ),
                    ],
                    pt="xl",
                ),
                span={"xs": 12, "sm": 6},
            ),
            dmc.GridCol(span={"xs": 0, "sm": 3}),
        ],
    )


def layout(**kwargs):
    if current_user.is_authenticated:
        return dash.dcc.Location(
            pathname=kwargs.get("next", "/"), id="redirect-to-login"
        )
    return login_form(next_page=kwargs.get("next", "/"))
