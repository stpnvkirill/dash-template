from typing import Any

from dash import ClientsideFunction, Input, Output, clientside_callback
from dash_iconify import DashIconify
import dash_mantine_components as dmc

from app.frontend.components.base import BaseComponent
from app.frontend.components.locale import _l


class PwdInput(BaseComponent):
    """Password input field with complexity indicator.

    Usage example:
        >>> pwd = PwdInput(namespace="login")
        >>> pwd(with_check=True)  # PasswordInput with complexity check
    """

    def __call__(self, with_check: bool = True, **kwargs: Any) -> dmc.PasswordInput:
        """Create PasswordInput component.

        Args:
            with_check: Show password complexity indicator.
            **kwargs: Parameters for dmc.PasswordInput.

        Returns:
            Configured dmc.PasswordInput component with auto-generated ID.
        """
        description = None
        if with_check:
            description = dmc.Group(
                [
                    dmc.Text(_l("password_complexity_label"), size="sm"),
                    dmc.Rating(
                        id=self.suffix_component_id(suffix="Rating"),
                        fractions=2,
                        value=0,
                        readOnly=True,
                        size="sm",
                    ),
                ],
            )
        return dmc.PasswordInput(
            id=self.component_id,
            placeholder="**********",
            label=_l("password_input_label"),
            description=description,
            leftSection=DashIconify(icon="bi:shield-lock"),
            **kwargs,
        )


# Clientside callback for password complexity check
# Note: hidden=True is not required for clientside callbacks
clientside_callback(
    ClientsideFunction("auth", "check_pwd"),
    Output(PwdInput.match_component_id(suffix="Rating"), "value"),
    Output(PwdInput.match_component_id(), "error"),
    Input(PwdInput.match_component_id(), "value"),
    prevent_initial_call=True,
)
