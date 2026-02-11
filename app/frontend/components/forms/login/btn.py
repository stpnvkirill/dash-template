from app.frontend.components.button import Button


class LoginButton(Button):
    def __call__(self, **kwargs):
        kwrg = {
            "children": "Войти",
            "fullWidth": True,
        }
        kwrg.update(kwargs)
        return super().__call__(**kwrg)
