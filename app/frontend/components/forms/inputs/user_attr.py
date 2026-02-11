from dash_iconify import DashIconify
import dash_mantine_components as dmc

from app.frontend.components.base import BaseComponent


class UserEmailInput(BaseComponent):
    def __call__(self, **kwargs):
        return dmc.TextInput(
            label="Почта",
            placeholder="ivan@developer.ru",
            leftSection=DashIconify(icon="ic:round-alternate-email"),
            id=self.component_id,
            **kwargs,
        )


class UserFirstNameInput(BaseComponent):
    def __call__(self, **kwargs):
        return dmc.TextInput(
            label="Имя",
            placeholder="Иван",
            leftSection=DashIconify(icon="radix-icons:person"),
            id=self.component_id,
            **kwargs,
        )


class UserLastNameInput(BaseComponent):
    def __call__(self, **kwargs):
        return dmc.TextInput(
            label="Фамилия",
            placeholder="Иванов",
            leftSection=DashIconify(icon="radix-icons:person"),
            id=self.component_id,
            **kwargs,
        )


class UserSexInput(BaseComponent):
    def __call__(self, **kwargs):
        return dmc.ChipGroup(
            dmc.Group(
                [
                    dmc.Chip("Мужчина", value="MALE"),
                    dmc.Chip("Женщина", value="FEMALE"),
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
            label="Запомнить меня", checked=True, id=self.component_id, **kwargs
        )
