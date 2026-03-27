from typing import Any

import dash_mantine_components as dmc

from app.frontend.components.base import BaseComponent


class Box(BaseComponent):
    """Base Box container with automatic ID generation.

    Usage example:
        >>> box = Box(namespace="profile", suffix="Container")
        >>> box()  # dmc.Box with id={"component": "Box", "namespace": "profile", ...}
    """

    def __call__(self, **kwargs: Any) -> dmc.Box:
        """Create Box component.

        Args:
            **kwargs: Parameters for dmc.Box.

        Returns:
            Configured dmc.Box component with auto-generated ID.
        """
        return dmc.Box(id=self.component_id, **kwargs)
