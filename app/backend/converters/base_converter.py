"""Base protocol for converters."""

from typing import Any, Protocol, TypeVar

M = TypeVar("M")  # Model type
D = TypeVar("D")  # DTO type


class BaseConverter(Protocol[M, D]):
    """Base protocol for model-DTO converters.

    Type parameters:
        M: Model type.
        D: DTO type.
    """

    @staticmethod
    def to_dto(model: M, **kwargs: Any) -> D | None:
        """Convert model to DTO.

        Args:
            model: Model instance to convert.
            **kwargs: Additional conversion options.

        Returns:
            DTO instance or None if model is None.
        """
        ...

    @staticmethod
    def from_dto(dto: D) -> M | None:
        """Convert DTO to model.

        Args:
            dto: DTO instance to convert.

        Returns:
            Model instance or None if dto is None.
        """
        ...
