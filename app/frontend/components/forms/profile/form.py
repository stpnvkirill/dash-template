from uuid import uuid7

from dash import (
    ClientsideFunction,
    Input,
    Output,
    Patch,
    State,
    callback,
    clientside_callback,
    set_props,
)
import dash_mantine_components as dmc
from flask_login import current_user

from app.backend import back
from app.backend.domain import UserDto
from app.frontend.components.box import Box
from app.frontend.components.forms.inputs.password import PwdInput
from app.frontend.components.forms.inputs.user_attr import (
    UserEmailInput,
    UserFirstNameInput,
    UserLastNameInput,
    UserSexInput,
)

from .btn import ProfileLogoutButton, ProfileSaveButton

namespace = "profile"
ProfileRespBox = Box(namespace=namespace, suffix="ProfileResp")


def ProfileForm(user: UserDto):
    return dmc.Box(
        [
            UserEmailInput(namespace=namespace)(value=user.email, disabled=True),
            dmc.Divider(my="sm"),
            UserLastNameInput(namespace=namespace)(
                value=user.last_name,
            ),
            UserFirstNameInput(namespace=namespace)(
                value=user.first_name,
                pb="md",
            ),
            UserSexInput(namespace=namespace)(
                value=user.sex,
            ),
            dmc.Divider(my="sm"),
            PwdInput(
                namespace=namespace,
            )(),
            ProfileSaveButton(namespace=namespace)(),
            ProfileRespBox(),
            dmc.Text(
                "Аккаунт создан: " + user.created_at.strftime("%Y-%m-%d %H:%M UTC"),
                pt="md",
                ta="center",
            ),
            dmc.Text(f"Идентификатор: {user.id}", ta="center"),
            ProfileLogoutButton(namespace=namespace)(),
        ]
    )


@callback(
    Output(ProfileRespBox.cid(namespace=namespace), "children"),
    Input(ProfileSaveButton.cid(namespace=namespace), "n_clicks"),
    State(UserFirstNameInput.cid(namespace=namespace), "value"),
    State(UserLastNameInput.cid(namespace=namespace), "value"),
    State(UserSexInput.cid(namespace=namespace), "value"),
    State(PwdInput.cid(namespace=namespace), "value"),
    running=(
        Output(ProfileSaveButton.cid(namespace=namespace), "loading"),
        True,
        False,
    ),
    hidden=True,
)
def update_profile(n, firstname, lastname, sex, pwd):
    if n and firstname and lastname:
        user = back.user.update_user(
            user_id=current_user.id,
            first_name=firstname,
            last_name=lastname,
            password=pwd,
            sex=sex,
        )
        set_props(
            UserFirstNameInput.cid(namespace=namespace), {"value": user.first_name}
        )
        set_props(UserLastNameInput.cid(namespace=namespace), {"value": user.last_name})
        set_props(PwdInput.cid(namespace=namespace), {"value": ""})
        patched_notify = Patch()
        patched_notify.append(
            {
                "action": "show",
                "id": str(uuid7()),
                "message": "Данные обновлены",
                "withCloseButton": True,
                "autoClose": 3500,
                "color": "green",
            }
        )
        set_props(
            "notification-container",
            {"sendNotifications": patched_notify},
        )
        return ""


clientside_callback(
    ClientsideFunction("profile", "check_pwd"),
    Output(ProfileSaveButton.cid(namespace=namespace), "disabled"),
    Input(PwdInput.cid(namespace=namespace), "error"),
    prevent_initial_call=True,
    hidden=True,
)
