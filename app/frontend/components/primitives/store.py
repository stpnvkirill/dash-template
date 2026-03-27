from typing import Any

from dash import dcc

from app.frontend.components.base import BaseComponent


class Store(BaseComponent):
    """Store component for client-side data storage.

    Usage example:
        >>> store = Store(namespace="login", suffix="DataStore")
        >>> store(data={"key": "value"})  # dcc.Store with data
    """

    def __call__(self, data: Any = None, **kwargs: Any) -> dcc.Store:
        """Create Store component.

        Args:
            data: Data to store (any serializable type).
            **kwargs: Parameters for dcc.Store.

        Returns:
            Configured dcc.Store component with auto-generated ID.
        """
        return dcc.Store(id=self.component_id, data=data, **kwargs)
