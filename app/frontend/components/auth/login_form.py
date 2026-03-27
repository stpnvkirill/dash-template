from typing import Any

from dash import Input, Output, State, callback, dcc, no_update
import dash_mantine_components as dmc
from flask_login import login_user

from app.frontend.components.locale import _l
from app.frontend.components.primitives import Box, Store
from app.frontend.components.shared.inputs import PwdInput, RememberMe, UserEmailInput
from app.frontend.utils import FrontendAuthService, LoginCredentials

from .buttons import LoginButton

NAMESPACE = "login"

LoginRespBox = Box(namespace=NAMESPACE, suffix="LoginResp")
StoreComponent = Store(namespace=NAMESPACE, suffix="LoginStore")


def LoginForm(next_page: str = "/") -> dmc.Stack:
    """User login form.

    Args:
        next_page: URL for redirect after successful login.

    Returns:
        Login form component.
    """
    return dmc.Stack(
        pos="relative",
        p="lg",
        children=[
            UserEmailInput(namespace=NAMESPACE)(required=False),
            PwdInput(namespace=NAMESPACE)(with_check=False, required=False),
            dmc.Group(
                [
                    RememberMe(namespace=NAMESPACE)(),
                    dmc.Anchor(_l("loginform_forgot_password"), href="/forgot_pwd"),
                ],
                justify="space-between",
            ),
            LoginRespBox(),
            LoginButton(namespace=NAMESPACE)(),
            StoreComponent(data=next_page),
        ],
    )


@callback(
    Output(LoginRespBox.cid(namespace=NAMESPACE), "children"),
    Input(LoginButton.cid(namespace=NAMESPACE), "n_clicks"),
    State(UserEmailInput.cid(namespace=NAMESPACE), "value"),
    State(PwdInput.cid(namespace=NAMESPACE), "value"),
    State(RememberMe.cid(namespace=NAMESPACE), "value"),
    State(StoreComponent.cid(namespace=NAMESPACE), "data"),
    prevent_initial_call=True,
)
def login(
    n_clicks: int | None,
    email: str | None,
    password: str | None,
    remember: bool = True,
    next_page: str = "/",
) -> dmc.Alert | dcc.Location | Any:
    """Handle user login attempt.

    Args:
        n_clicks: Number of clicks on login button.
        email: User email.
        password: User password.
        remember: Remember me flag.
        next_page: URL for redirect after success.

    Returns:
        Alert with error or Location for redirect.
    """
    if not (n_clicks and email and password):
        return no_update

    try:
        client_info = FrontendAuthService.get_client_info()
        credentials = LoginCredentials(
            email=email,
            password=password,
            remember=remember,
            ip_address=client_info["ip_address"],
            os=client_info["os"],
            browser=client_info["browser"],
        )

        result = FrontendAuthService.authenticate(credentials)

        if not result.success:
            return dmc.Alert(
                result.error_message or _l("alert_unsuccessful_login"),
                color="yellow",
            )

        login_user(result.user, remember=remember)
        return dcc.Location(href=next_page, id="login-redirect")

    except Exception:
        return dmc.Alert(
            _l("alert_unsuccessful_login"),
            color="red",
        )
