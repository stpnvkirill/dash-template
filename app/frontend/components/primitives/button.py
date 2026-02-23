import dash_mantine_components as dmc

from app.frontend.components.base import BaseComponent


class Button(BaseComponent):
    def __call__(self, **kwargs):
        return dmc.Button(id=self.component_id, **kwargs)
