from typing import Any

from dash_iconify import DashIconify
import dash_mantine_components as dmc

from app.frontend.components.base import BaseComponent
from app.frontend.components.locale import _l


class UserEmailInput(BaseComponent):
    """User email input field.

    Usage example:
        >>> email = UserEmailInput(namespace="profile")
        >>> email(value="user@example.com")
    """

    def __call__(self, **kwargs: Any) -> dmc.TextInput:
        """Create TextInput component for email.

        Args:
            **kwargs: Parameters for dmc.TextInput.

        Returns:
            Configured dmc.TextInput component with auto-generated ID.
        """
        return dmc.TextInput(
            label=_l("email_input_label"),
            placeholder="ivan@developer.ru",
            leftSection=DashIconify(icon="ic:round-alternate-email"),
            id=self.component_id,
            **kwargs,
        )


class UserFirstNameInput(BaseComponent):
    """User first name input field.

    Usage example:
        >>> first_name = UserFirstNameInput(namespace="profile")
        >>> first_name(value="John")
    """

    def __call__(self, **kwargs: Any) -> dmc.TextInput:
        """Create TextInput component for first name.

        Args:
            **kwargs: Parameters for dmc.TextInput.

        Returns:
            Configured dmc.TextInput component with auto-generated ID.
        """
        return dmc.TextInput(
            label=_l("firstname_input_label"),
            placeholder="John",
            leftSection=DashIconify(icon="radix-icons:person"),
            id=self.component_id,
            **kwargs,
        )


class UserLastNameInput(BaseComponent):
    """User last name input field.

    Usage example:
        >>> last_name = UserLastNameInput(namespace="profile")
        >>> last_name(value="Smith")
    """

    def __call__(self, **kwargs: Any) -> dmc.TextInput:
        """Create TextInput component for last name.

        Args:
            **kwargs: Parameters for dmc.TextInput.

        Returns:
            Configured dmc.TextInput component with auto-generated ID.
        """
        return dmc.TextInput(
            label=_l("lastname_input_label"),
            placeholder="Smith",
            leftSection=DashIconify(icon="radix-icons:person"),
            id=self.component_id,
            **kwargs,
        )


class UserSexInput(BaseComponent):
    """User sex selection field (ChipGroup).

    Usage example:
        >>> sex = UserSexInput(namespace="profile")
        >>> sex(value="MALE")
    """

    def __call__(self, **kwargs: Any) -> dmc.ChipGroup:
        """Create ChipGroup component for sex selection.

        Args:
            **kwargs: Parameters for dmc.ChipGroup.

        Returns:
            Configured dmc.ChipGroup component with auto-generated ID.
        """
        return dmc.ChipGroup(
            dmc.Group(
                [
                    dmc.Chip(_l("usersex_input_label_man"), value="MALE"),
                    dmc.Chip(_l("usersex_input_label_woman"), value="FEMALE"),
                ]
            ),
            multiple=False,
            deselectable=True,
            id=self.component_id,
            **kwargs,
        )


class RememberMe(BaseComponent):
    """Remember me checkbox for login form.

    Usage example:
        >>> remember = RememberMe(namespace="login")
        >>> remember(checked=True)
    """

    def __call__(self, **kwargs: Any) -> dmc.Checkbox:
        """Create Checkbox component for remember me.

        Args:
            **kwargs: Parameters for dmc.Checkbox.

        Returns:
            Configured dmc.Checkbox component with auto-generated ID.
        """
        return dmc.Checkbox(
            label=_l("rememberme_checkbox_label"),
            checked=True,
            id=self.component_id,
            **kwargs,
        )
