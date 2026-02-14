from dash import (
    ClientsideFunction,
    Input,
    Output,
    State,
    callback,
    clientside_callback,
    dcc,
    no_update,
)
import dash_mantine_components as dmc
from flask_login import login_user

from app.backend import back
from app.frontend.components.box import Box
from app.frontend.components.forms.inputs.password import PwdInput
from app.frontend.components.forms.inputs.user_attr import (
    RememberMe,
    UserEmailInput,
    UserFirstNameInput,
    UserLastNameInput,
    UserSexInput,
)
from app.frontend.components.locale import _l
from app.frontend.components.store import Store

from .btn import RegButton

namespace = "reg"

RegRespBox = Box(namespace=namespace, suffix="RegResp")
store = Store(namespace=namespace, suffix="RegStore")


def RegForm(next_page="/"):
    return dmc.Stack(
        pos="relative",
        p="lg",
        children=[
            UserEmailInput(namespace=namespace)(),
            UserFirstNameInput(namespace=namespace)(),
            UserLastNameInput(namespace=namespace)(),
            UserSexInput(namespace=namespace)(value="MALE"),
            dmc.Divider(),
            PwdInput(namespace=namespace)(),
            dmc.Group(
                [
                    RememberMe(namespace=namespace)(),
                    dmc.Anchor(
                        dmc.Text(_l("regform_back_to_login"), size="xs"), href="/login"
                    ),
                ],
                justify="space-between",
            ),
            RegRespBox(),
            RegButton(namespace=namespace)(disabled=True),
            store(data=next_page),
        ],
    )


clientside_callback(
    ClientsideFunction("registration", "check_reg_inputs"),
    Output(RegButton.cid(namespace=namespace), "disabled"),
    Input(PwdInput.cid(namespace=namespace), "error"),
    Input(UserEmailInput.cid(namespace=namespace), "error"),
    Input(PwdInput.cid(namespace=namespace), "value"),
    Input(UserEmailInput.cid(namespace=namespace), "value"),
    Input(UserFirstNameInput.cid(namespace=namespace), "value"),
    Input(UserLastNameInput.cid(namespace=namespace), "value"),
    prevent_initial_call=True,
    hidden=True,
)


@callback(
    Output(UserEmailInput.cid(namespace=namespace), "error"),
    Input(UserEmailInput.cid(namespace=namespace), "value"),
    prevent_initial_call=True,
    hidden=True,
)
def check_email(email):
    if email and not back.user.check_email_is_available(email=email):
        return "Email не подходит"
    return ""


@callback(
    Output(RegRespBox.cid(namespace=namespace), "children"),
    Input(RegButton.cid(namespace=namespace), "n_clicks"),
    State(UserEmailInput.cid(namespace=namespace), "value"),
    State(UserFirstNameInput.cid(namespace=namespace), "value"),
    State(UserLastNameInput.cid(namespace=namespace), "value"),
    State(UserSexInput.cid(namespace=namespace), "value"),
    State(PwdInput.cid(namespace=namespace), "value"),
    State(store.cid(namespace=namespace), "data"),
    prevent_initial_call=True,
    running=(Output(RegButton.cid(namespace=namespace), "loading"), True, False),
    hidden=True,
)
def reg_user_callback(n_clicks, email, first_name, last_name, sex, password, next_page):  # noqa: PLR0913
    if n_clicks:
        user = back.user.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            sex=sex,
        )
        if not user:
            return "An error occurred when creating a user"
        user = back.user.create_session(user=user)
        login_user(user)
        return dcc.Location(href=next_page, id="login-redirect")
    return no_update
