from app.frontend.components.button import Button
from app.frontend.components.locale import _l


class LoginButton(Button):
    def __call__(self, **kwargs):
        kwrg = {
            "children": _l("btn_login"),
            "fullWidth": True,
        }
        kwrg.update(kwargs)
        return super().__call__(**kwrg)
