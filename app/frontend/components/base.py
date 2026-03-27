from typing import ClassVar

from dash import MATCH


class BaseComponent:
    """Base class for generating Dash component identifiers.

    Simplifies creation of pattern-matching IDs for Dash components,
    ensuring naming consistency and reducing error probability.

    Attributes:
        suffix: Suffix added to class name for component name formation.
        extra_config: Additional parameters added to all IDs (class-level).

    Example:
        >>> class UserInput(BaseComponent):
        ...     pass
        >>> input = UserInput(namespace="profile")
        >>> input.component_id
        {"component": "UserInput", "namespace": "profile"}
    """

    suffix: str | None = None
    extra_config: ClassVar[dict] = {}

    def __init__(
        self,
        namespace: str = "root",
        suffix: str | None = None,
        extra: dict | None = None,
    ) -> None:
        """Initialize component.

        Args:
            namespace: Namespace for grouping components (e.g., "login", "profile").
            suffix: Suffix for specific instance (overrides class-level).
            extra: Additional keys for pattern-matching ID.
        """
        self.namespace = namespace
        self.suffix = suffix
        self.extra = extra if extra else {}

    @classmethod
    def get_component_name(cls) -> str:
        """Get component name based on class and suffix.

        Returns:
            Component name (class name + suffix if specified).
        """
        if cls.suffix is not None:
            return cls.__name__ + cls.suffix
        return cls.__name__

    @property
    def component_id(self) -> dict:
        """Generate full ID for component instance.

        Returns:
            Dict with keys "component", "namespace" and additional parameters.
        """
        return {
            "component": self.__class__.get_component_name(),
            "namespace": self.namespace,
            **self.extra,
        }

    def suffix_component_id(self, suffix: str) -> dict:
        """Generate ID with suffix added to component name.

        Args:
            suffix: Suffix to append to component name.

        Returns:
            Dict with keys "component" (with suffix), "namespace" and additional params.
        """
        return {
            "component": self.__class__.get_component_name() + suffix,
            "namespace": self.namespace,
            **self.extra,
        }

    @classmethod
    def match_component_id(cls, suffix: str = "") -> dict:
        """Generate pattern-matching ID for use in callbacks.

        Designed for Input/Output/State in callbacks where you need to catch
        events from multiple components of the same type.

        Args:
            suffix: Optional suffix for component name.

        Returns:
            Dict with MATCH for namespace, allowing to catch events from all instances.

        Example:
            @callback(Output(PwdInput.match_component_id(), "value"), ...)
        """
        return {
            "component": cls.get_component_name() + suffix,
            "namespace": MATCH,
            **cls.extra_config,
        }

    @classmethod
    def cid(cls, namespace: str) -> dict:
        """Shorthand method for generating ID with specified namespace.

        Args:
            namespace: Namespace for component.

        Returns:
            Dict with keys "component" and "namespace".

        Example:
            Output(LoginButton.cid("login"), "n_clicks")
        """
        return {
            "component": cls.get_component_name(),
            "namespace": namespace,
            **cls.extra_config,
        }
