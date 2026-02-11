from dash_iconify import DashIconify
import dash_mantine_components as dmc

from app.frontend.components.base import BaseComponent


class UserEmailInput(BaseComponent):
    def __call__(self, **kwargs):
        return dmc.TextInput(
            label="Email",
            placeholder="ivan@developer.ru",
            leftSection=DashIconify(icon="ic:round-alternate-email"),
            id=self.component_id,
            **kwargs,
        )


class UserFirstNameInput(BaseComponent):
    def __call__(self, **kwargs):
        return dmc.TextInput(
            label="First Name",
            placeholder="John",
            leftSection=DashIconify(icon="radix-icons:person"),
            id=self.component_id,
            **kwargs,
        )


class UserLastNameInput(BaseComponent):
    def __call__(self, **kwargs):
        return dmc.TextInput(
            label="Last Name",
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
                    dmc.Chip("Man", value="MALE"),
                    dmc.Chip("Women", value="FEMALE"),
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
            label="Remember me", checked=True, id=self.component_id, **kwargs
        )
