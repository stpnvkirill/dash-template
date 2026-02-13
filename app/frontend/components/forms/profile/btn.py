import dash_mantine_components as dmc

from app.frontend.components.button import Button
from app.frontend.components.locale import _l


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


class ProfileSaveButton(Button):
    def __call__(self, **kwargs):
        kwrg = {
            "children": _l("profileform_save_btn"),
            "fullWidth": True,
            "mt": "md",
        }
        kwrg.update(kwargs)
        return super().__call__(**kwrg)
