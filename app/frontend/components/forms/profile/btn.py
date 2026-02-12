import dash_mantine_components as dmc

from app.frontend.components.button import Button


class ProfileLogoutButton(Button):
    def __call__(self, **kwargs):
        kwrg = {
            "children": "Выйти из аккаунта",
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


class ProfileSaveButton(Button):
    def __call__(self, **kwargs):
        kwrg = {
            "children": "Сохранить",
            "fullWidth": True,
            "mt": "md",
        }
        kwrg.update(kwargs)
        return super().__call__(**kwrg)
