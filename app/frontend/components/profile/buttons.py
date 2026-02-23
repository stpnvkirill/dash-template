from typing import ClassVar
from uuid import UUID

from dash import MATCH
from dash_iconify import DashIconify
import dash_mantine_components as dmc

from app.frontend.components.locale import _l
from app.frontend.components.primitives import Button


class ProfileSaveButton(Button):
    def __call__(self, **kwargs):
        kwrg = {
            "children": _l("profileform_save_btn"),
            "fullWidth": True,
            "mt": "md",
        }
        kwrg.update(kwargs)
        return super().__call__(**kwrg)


class ProfileLogoutButton(Button):
    def __call__(self, **kwargs):
        kwrg = {
            "children": _l("profileform_logout_btn"),
            "variant": "transparent",
            "fullWidth": True,
            "color": "red",
        }
        kwrg.update(kwargs)
        return dmc.Anchor(
            super().__call__(**kwrg),
            href="/logout",
            underline="never",
        )


class TerminateSessionBtn(Button):
    extra_config: ClassVar = {"session_id": MATCH}

    def __init__(
        self,
        session_id: UUID,
        namespace="root",
        suffix: str | None = None,
    ):
        super().__init__(
            namespace=namespace, suffix=suffix, extra={"session_id": str(session_id)}
        )

    def __call__(self, **kwargs):
        kwrg = {
            "children": _l("terminate_session_btn_children"),
            "variant": "outline",
            "fullWidth": True,
            "color": "red",
            "bdrs": "xl",
            "size": "xs",
        }
        kwrg.update(kwargs)
        return super().__call__(**kwrg)


class TerminateAllOtherSessionBtn(Button):
    def __call__(self, **kwargs):
        kwrg = {
            "children": _l("terminate_all_session_btn_children"),
            "variant": "transparent",
            "fullWidth": True,
            "color": "red",
            "leftSection": DashIconify(icon="tabler:hand-stop"),
        }
        kwrg.update(kwargs)
        return super().__call__(**kwrg)
