from typing import Any

import dash_mantine_components as dmc

from app.frontend.components.base import BaseComponent


class Button(BaseComponent):
    """Base Button component with automatic ID generation.

    Usage example:
        >>> btn = Button(namespace="login", suffix="Submit")
        >>> btn()  # dmc.Button with auto-generated ID
    """

    def __call__(self, **kwargs: Any) -> dmc.Button:
        """Create Button component.

        Args:
            **kwargs: Parameters for dmc.Button.

        Returns:
            Configured dmc.Button component with auto-generated ID.
        """
        return dmc.Button(id=self.component_id, **kwargs)
