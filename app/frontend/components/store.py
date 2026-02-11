from dash import dcc

from app.frontend.components.base import BaseComponent


class Store(BaseComponent):
    def __call__(self, data=None, **kwargs):
        return dcc.Store(id=self.component_id, data=data, **kwargs)
