from typing import Protocol


class BaseConverter(Protocol):
    """Base protocol for converters"""

    @staticmethod
    def to_dto(model, **kwargs):
        """Convert model to DTO"""
        ...

    @staticmethod
    def from_dto(dto):
        """Convert DTO to model"""
        ...
