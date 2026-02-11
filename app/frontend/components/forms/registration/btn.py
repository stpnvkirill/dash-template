from app.frontend.components.button import Button


class RegButton(Button):
    def __call__(self, **kwargs):
        kwrg = {
            "children": "Create account",
            "fullWidth": True,
        }
        kwrg.update(kwargs)
        return super().__call__(**kwrg)
