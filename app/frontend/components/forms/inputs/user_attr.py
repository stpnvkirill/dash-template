from dash_iconify import DashIconify
import dash_mantine_components as dmc

from app.frontend.components.base import BaseComponent
from app.frontend.components.locale import _l


class UserEmailInput(BaseComponent):
    def __call__(self, **kwargs):
        return dmc.TextInput(
            label=_l("email_input_label"),
            placeholder="ivan@developer.ru",
            leftSection=DashIconify(icon="ic:round-alternate-email"),
            id=self.component_id,
            **kwargs,
        )


class UserFirstNameInput(BaseComponent):
    def __call__(self, **kwargs):
        return dmc.TextInput(
            label=_l("firstname_input_label"),
            placeholder="John",
            leftSection=DashIconify(icon="radix-icons:person"),
            id=self.component_id,
            **kwargs,
        )


class UserLastNameInput(BaseComponent):
    def __call__(self, **kwargs):
        return dmc.TextInput(
            label=_l("lastname_input_label"),
            placeholder="Smith",
            leftSection=DashIconify(icon="radix-icons:person"),
            id=self.component_id,
            **kwargs,
        )


class UserSexInput(BaseComponent):
    def __call__(self, **kwargs):
        return dmc.ChipGroup(
            dmc.Group(
                [
                    dmc.Chip(_l("usersex_input_label_man"), value="MALE"),
                    dmc.Chip(_l("usersex_input_label_woman"), value="FEMALE"),
                ]
            ),
            multiple=False,
            deselectable=True,
            id=self.component_id,
            **kwargs,
        )


class RememberMe(BaseComponent):
    def __call__(self, **kwargs):
        return dmc.Checkbox(
            label=_l("rememberme_checkbox_label"),
            checked=True,
            id=self.component_id,
            **kwargs,
        )
