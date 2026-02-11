import dash_mantine_components as dmc

from .base import BaseComponent


class Box(BaseComponent):
    def __call__(self, **kwargs):
        return dmc.Box(id=self.component_id, **kwargs)
