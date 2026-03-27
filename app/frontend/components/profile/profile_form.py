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

from app.backend.domain import UserDto
from app.frontend.components.locale import _l, _l_dt, _l_dt_relative
from app.frontend.components.primitives import Box
from app.frontend.components.shared.inputs import (
    PwdInput,
    UserEmailInput,
    UserFirstNameInput,
    UserLastNameInput,
    UserSexInput,
)
from app.frontend.utils import FrontendProfileService, ProfileUpdateData

from .buttons import ProfileLogoutButton, ProfileSaveButton

NAMESPACE = "profile"
ProfileRespBox = Box(namespace=NAMESPACE, suffix="ProfileResp")


def ProfileForm(user: UserDto) -> dmc.Box:
    """User profile form.

    Args:
        user: User object with data to display.

    Returns:
        Profile form component.
    """
    return dmc.Box(
        [
            UserEmailInput(namespace=NAMESPACE)(value=user.email, disabled=True),
            dmc.Divider(my="sm"),
            UserLastNameInput(namespace=NAMESPACE)(
                value=user.last_name,
            ),
            UserFirstNameInput(namespace=NAMESPACE)(
                value=user.first_name,
                pb="md",
            ),
            UserSexInput(namespace=NAMESPACE)(
                value=user.sex,
            ),
            dmc.Divider(my="sm"),
            PwdInput(
                namespace=NAMESPACE,
            )(),
            ProfileSaveButton(namespace=NAMESPACE)(),
            ProfileRespBox(),
            dmc.Text(
                [
                    _l("profileform_account_created"),
                    _l_dt(user.created_at, "L LT"),
                    " || ",
                    _l_dt_relative(user.created_at),
                ],
                pt="md",
                ta="center",
            ),
            dmc.Text([_l("profileform_user_id"), str(user.id)], ta="center"),
            ProfileLogoutButton(namespace=NAMESPACE)(),
        ]
    )


@callback(
    Output(ProfileRespBox.cid(namespace=NAMESPACE), "children"),
    Input(ProfileSaveButton.cid(namespace=NAMESPACE), "n_clicks"),
    State(UserFirstNameInput.cid(namespace=NAMESPACE), "value"),
    State(UserLastNameInput.cid(namespace=NAMESPACE), "value"),
    State(UserSexInput.cid(namespace=NAMESPACE), "value"),
    State(PwdInput.cid(namespace=NAMESPACE), "value"),
    running=(
        Output(ProfileSaveButton.cid(namespace=NAMESPACE), "loading"),
        True,
        False,
    ),
    prevent_initial_call=True,
)
def update_profile(
    n: int | None,
    firstname: str | None,
    lastname: str | None,
    sex: str | None,
    pwd: str | None,
) -> str | None:
    """Update user profile data.

    Args:
        n: Number of clicks on save button.
        firstname: New user first name.
        lastname: New user last name.
        sex: User sex.
        pwd: New password (empty string = no change).

    Returns:
        Empty string on success, None if no changes.
    """
    if not (n and firstname and lastname):
        return None

    try:
        update_data = ProfileUpdateData(
            user_id=current_user.id,
            first_name=firstname,
            last_name=lastname,
            sex=sex,
            password=pwd if pwd else None,
        )

        user = FrontendProfileService.update_profile(update_data)

        set_props(
            UserFirstNameInput.cid(namespace=NAMESPACE), {"value": user.first_name}
        )
        set_props(UserLastNameInput.cid(namespace=NAMESPACE), {"value": user.last_name})
        set_props(PwdInput.cid(namespace=NAMESPACE), {"value": ""})

        patched_notify = Patch()
        patched_notify.append(
            {
                "action": "show",
                "id": str(uuid7()),
                "message": _l("notify_data_update"),
                "withCloseButton": True,
                "color": "green",
                "autoClose": 3500,
            }
        )
        set_props(
            "notification-container",
            {"sendNotifications": patched_notify},
        )
        set_props(
            "user-section-navbar",
            {"label": f"{user.first_name} {user.last_name}"},
        )
        return ""

    except Exception:
        patched_notify = Patch()
        patched_notify.append(
            {
                "action": "show",
                "id": str(uuid7()),
                "message": _l("notify_error"),
                "withCloseButton": True,
                "color": "red",
                "autoClose": 5000,
            }
        )
        set_props("notification-container", {"sendNotifications": patched_notify})
        return ""


clientside_callback(
    ClientsideFunction("profile", "check_pwd"),
    Output(ProfileSaveButton.cid(namespace=NAMESPACE), "disabled"),
    Input(PwdInput.cid(namespace=NAMESPACE), "error"),
    prevent_initial_call=True,
)
