from dash import MATCH


class BaseComponent:
    suffix = None

    def __init__(self, namespace="root", suffix: str | None = None):
        self.namespace = namespace
        self.suffix = suffix

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
        }

    def suffix_component_id(self, suffix):
        return {
            "component": self.__class__.get_component_name() + suffix,
            "namespace": self.namespace,
        }

    @classmethod
    def match_component_id(cls, suffix: str = ""):
        return {"component": cls.get_component_name() + suffix, "namespace": MATCH}

    @classmethod
    def cid(cls, namespace):
        return {"component": cls.get_component_name(), "namespace": namespace}
