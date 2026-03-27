from typing import Any
from uuid import UUID

from dash import MATCH, Input, Output, callback, ctx, no_update
from dash_iconify import DashIconify
import dash_mantine_components as dmc
from flask_login import current_user

from app.backend.domain import SessionDto, UserDto
from app.frontend.components.locale import _l, _l_dt_relative
from app.frontend.utils import FrontendProfileService

from .buttons import TerminateAllOtherSessionBtn, TerminateSessionBtn

NAMESPACE = "session_tab"


def SessionTab(user: UserDto) -> dmc.Stack:
    """User sessions management tab.

    Args:
        user: User object for fetching sessions.

    Returns:
        Sessions tab component.
    """
    sessions = FrontendProfileService.get_active_sessions(
        user.id, exclude_id=user.session.id
    )
    return dmc.Stack([CurrentSessionBlock(user.session), SessionBlock(sessions)])


def SessionCard(session: SessionDto, with_terminate: bool = False) -> dmc.NavLink:
    """Session card for display.

    Args:
        session: Session object.
        with_terminate: Show session terminate button.

    Returns:
        Session card component.
    """
    # XSS protection: sanitize OS and browser data
    os_name = str(session.os).capitalize()
    browser_name = str(session.browser).capitalize()
    label = f"{os_name} | {browser_name}"

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
        rightSection=TerminateSessionBtn(session_id=session.id, namespace=NAMESPACE)()
        if with_terminate
        else "",
        disableRightSectionRotation=True,
    )


def SessionBlock(sessions: list[SessionDto]) -> dmc.Fieldset:
    """Sessions list block.

    Args:
        sessions: List of sessions to display.

    Returns:
        Fieldset component with sessions list.
    """
    return dmc.Fieldset(
        [SessionCard(s, with_terminate=True) for s in sessions],
        legend=_l("profilepage_sessions_block_legend"),
        variant="filled",
        radius="sm",
        disabled=False,
        p="xs",
        id={"component": "SessionBlock", "namespace": NAMESPACE},
    )


def CurrentSessionBlock(session: SessionDto) -> dmc.Fieldset:
    """Current session block.

    Args:
        session: Current session object.

    Returns:
        Fieldset component with current session info.
    """
    return dmc.Fieldset(
        [
            SessionCard(session),
            TerminateAllOtherSessionBtn(namespace=NAMESPACE)(),
        ],
        legend=_l("profilepage_sessions_block_current_legend"),
        radius="sm",
        disabled=False,
        p="xs",
    )


@callback(
    Output({"type": "session-card", "session_id": MATCH}, "display"),
    Input(TerminateSessionBtn.cid(namespace=NAMESPACE), "n_clicks"),
    prevent_initial_call=True,
)
def terminate_session(n: int | None) -> str | None:
    """Terminate session by ID.

    Args:
        n: Number of clicks on terminate button.

    Returns:
        "none" to hide card or None on error.
    """
    if not n:
        return None

    try:
        session_id = ctx.triggered_id.get("session_id")
        if session_id:
            FrontendProfileService.deactivate_session(UUID(session_id))
            return "none"
    except ValueError, TypeError:
        pass

    return None


@callback(
    Output({"component": "SessionBlock", "namespace": NAMESPACE}, "children"),
    Input(TerminateAllOtherSessionBtn.cid(namespace=NAMESPACE), "n_clicks"),
    prevent_initial_call=True,
)
def terminate_all_other_session(n: int | None) -> list | Any:
    """Terminate all sessions except current.

    Args:
        n: Number of clicks on terminate all button.

    Returns:
        Empty list after termination or no_update.
    """
    if not n:
        return no_update

    try:
        FrontendProfileService.deactivate_all_other_sessions(
            user_id=current_user.id,
            current_session_id=current_user.session.id,
        )
        return []
    except Exception:
        return no_update
