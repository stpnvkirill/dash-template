from dash import ClientsideFunction, Input, Output, clientside_callback
from dash_iconify import DashIconify
import dash_mantine_components as dmc

from app.frontend.components.base import BaseComponent


class PwdInput(BaseComponent):
    def __call__(self, with_check=True, **kwargs):
        description = None
        if with_check:
            description = dmc.Group(
                [
                    dmc.Text("Сложность:", size="sm"),
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
            label="Пароль",
            description=description,
            leftSection=DashIconify(icon="bi:shield-lock"),
            **kwargs,
        )


# Клиентский callback для расчета сложности пароля
clientside_callback(
    ClientsideFunction("auth", "check_pwd"),
    Output(PwdInput.match_component_id(suffix="Rating"), "value"),
    Output(PwdInput.match_component_id(), "error"),
    Input(PwdInput.match_component_id(), "value"),
    hidden=True,
    prevent_initial_call=True,
)
