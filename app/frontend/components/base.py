from typing import ClassVar

from dash import MATCH


class BaseComponent:
    suffix = None
    extra_config: ClassVar = {}

    def __init__(
        self, namespace="root", suffix: str | None = None, extra: dict | None = None
    ):
        self.namespace = namespace
        self.suffix = suffix
        self.extra = extra if extra else {}

    @classmethod
    def get_component_name(cls):
        if cls.suffix is not None:
            return cls.__name__ + cls.suffix
        return cls.__name__

    @property
    def component_id(self):
        return {
            "component": self.__class__.get_component_name(),
            "namespace": self.namespace,
            **self.extra,
        }

    def suffix_component_id(self, suffix):
        return {
            "component": self.__class__.get_component_name() + suffix,
            "namespace": self.namespace,
            **self.extra,
        }

    @classmethod
    def match_component_id(cls, suffix: str = ""):
        return {
            "component": cls.get_component_name() + suffix,
            "namespace": MATCH,
            **cls.extra_config,
        }

    @classmethod
    def cid(cls, namespace):
        return {
            "component": cls.get_component_name(),
            "namespace": namespace,
            **cls.extra_config,
        }
