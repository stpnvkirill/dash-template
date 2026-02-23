from uuid import UUID

from dash import MATCH, Input, Output, callback, ctx, no_update
from dash_iconify import DashIconify
import dash_mantine_components as dmc
from flask_login import current_user

from app.backend import back
from app.backend.domain import SessionDto, UserDto
from app.frontend.components.locale import _l, _l_dt_relative

from .buttons import TerminateAllOtherSessionBtn, TerminateSessionBtn

namespace = "session-tab"


def SessionTab(user: UserDto):
    sessions = back.user.get_active_session(user.id, exclude_id=user.session.id)
    return dmc.Stack([CurrentSessionBlock(user.session), SessionBlock(sessions)])


def SessionCard(session: SessionDto, with_terminate: bool = False):
    label = f"{session.os.capitalize()} | {session.browser.capitalize()}"
    return dmc.NavLink(
        id={"type": "session-card", "session_id": str(session.id)},
        label=label,
        description=[
            _l("profilepage_sessions_last_active"),
            _l_dt_relative(session.last_active),
        ],
        bdrs="md",
        m=0,
        leftSection=dmc.ActionIcon(
            DashIconify(icon="lets-icons:user-scan"),
            variant="light",
            size="lg",
            radius="xl",
        ),
        rightSection=TerminateSessionBtn(session_id=session.id, namespace=namespace)()
        if with_terminate
        else "",
        disableRightSectionRotation=True,
    )


def SessionBlock(session: list[SessionDto]):
    return dmc.Fieldset(
        [SessionCard(s, with_terminate=True) for s in session],
        legend=_l("profilepage_sessions_block_legend"),
        variant="filled",
        radius="sm",
        disabled=False,
        p="xs",
        id={"component": "SessionBlock", "namespace": namespace},
    )


def CurrentSessionBlock(session: SessionDto):
    return dmc.Fieldset(
        [
            SessionCard(session),
            TerminateAllOtherSessionBtn(namespace=namespace)(),
        ],
        legend=_l("profilepage_sessions_block_current_legend"),
        radius="sm",
        disabled=False,
        p="xs",
    )


@callback(
    Output({"type": "session-card", "session_id": MATCH}, "display"),
    Input(TerminateSessionBtn.cid(namespace=namespace), "n_clicks"),
    hidden=True,
)
def terminate_session(n):
    if n:
        session_id = ctx.triggered_id.get("session_id")
        back.user.deactivate_session(session_id=UUID(session_id))
        return "none"


@callback(
    Output({"component": "SessionBlock", "namespace": namespace}, "children"),
    Input(TerminateAllOtherSessionBtn.cid(namespace=namespace), "n_clicks"),
    hidden=True,
)
def terminate_all_other_session(n):
    if n:
        sessions = back.user.get_active_session(
            current_user.id, exclude_id=current_user.session.id
        )
        for s in sessions:
            back.user.deactivate_session(session_id=s.id)
        return []
    return no_update
