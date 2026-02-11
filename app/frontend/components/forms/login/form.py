from dash import Input, Output, State, callback, dcc, no_update
import dash_mantine_components as dmc
from flask_login import login_user

from app.backend import back
from app.frontend.components.box import Box
from app.frontend.components.forms.inputs.password import PwdInput
from app.frontend.components.forms.inputs.user_attr import RememberMe, UserEmailInput
from app.frontend.components.store import Store

from .btn import LoginButton

namespace = "login"

LoginRespBox = Box(namespace=namespace, suffix="LoginResp")
store = Store(namespace=namespace, suffix="LoginStore")


def LoginForm(next_page="/"):
    return dmc.Stack(
        pos="relative",
        p="lg",
        children=[
            UserEmailInput(namespace=namespace)(required=False),
            PwdInput(namespace=namespace)(with_check=False, required=False),
            dmc.Group(
                [
                    RememberMe(namespace=namespace)(),
                    dmc.Anchor("Forgot password", href="/forgot_pwd"),
                ],
                justify="space-between",
            ),
            LoginRespBox(),
            LoginButton(namespace=namespace)(),
            store(data=next_page),
        ],
    )


@callback(
    Output(LoginRespBox.cid(namespace=namespace), "children"),
    Input(LoginButton.cid(namespace=namespace), "n_clicks"),
    State(UserEmailInput.cid(namespace=namespace), "value"),
    State(PwdInput.cid(namespace=namespace), "value"),
    State(RememberMe.cid(namespace=namespace), "value"),
    State(store.cid(namespace=namespace), "data"),
    hidden=True,
)
def login(n_clicks, email, password, remember=True, next_page="/"):
    if n_clicks and email and password:
        user = back.user.auth(email=email, password=password)
        if not user:
            return dmc.Alert("Unsuccessful login!", color="yellow")
        login_user(user, remember=remember)
        return dcc.Location(href=next_page, id="login-redirect")
    return no_update
