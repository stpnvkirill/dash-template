from app.frontend.components.locale import _l
from app.frontend.components.primitives import Button


class LoginButton(Button):
    def __call__(self, **kwargs):
        kwrg = {
            "children": _l("btn_login"),
            "fullWidth": True,
        }
        kwrg.update(kwargs)
        return super().__call__(**kwrg)


class RegButton(Button):
    def __call__(self, **kwargs):
        kwrg = {
            "children": _l("btn_reg"),
            "fullWidth": True,
        }
        kwrg.update(kwargs)
        return super().__call__(**kwrg)
