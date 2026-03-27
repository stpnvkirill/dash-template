"""Tests for PermissionService."""

import uuid

import pytest

from app.backend.database.models import (
    Permission,
    PermissionGroup,
    User,
    permission_group_permissions,
    user_permission_groups,
    user_permissions,
)
from app.backend.infrastructure.database import SqlService
from app.backend.services.permission.permission_service import PermissionService


class TestPermissionService:
    """Tests for PermissionService."""

    @pytest.fixture
    def permission_service(self) -> PermissionService:
        """Fixture for PermissionService."""
        return PermissionService()

    def test_load_permissions_empty(
        self, permission_service: PermissionService
    ) -> None:
        """Test loading permissions for user without permissions."""
        # Create user without permissions
        email = f"test_empty_{uuid.uuid4()}@example.com"
        user_repo = SqlService(model=User)
        user = user_repo.insert(
            email=email, password="password", first_name="Test", last_name="User"
        )

        permissions = permission_service.load_permissions(user.id)
        assert permissions == frozenset()

    def test_load_permissions_direct(
        self, permission_service: PermissionService
    ) -> None:
        """Test loading user's direct permissions."""
        # Create user
        email = f"test_direct_{uuid.uuid4()}@example.com"
        user_repo = SqlService(model=User)
        user = user_repo.insert(
            email=email, password="password", first_name="Test", last_name="User"
        )

        # Create permission
        perm_repo = SqlService(model=Permission)
        permission = perm_repo.insert(category=f"test_{uuid.uuid4()}", key="read")

        # Assign permission to user directly
        with permission_service.session_scope() as session:
            session.execute(
                user_permissions.insert().values(
                    user_id=user.id, permission_id=permission.id
                )
            )
            session.commit()

        # Load permissions
        permissions = permission_service.load_permissions(user.id)
        assert len(permissions) == 1
        # Check that permission is in the list
        perm_tuple = next(iter(permissions))
        assert perm_tuple[1] == "read"

    def test_load_permissions_via_group(
        self, permission_service: PermissionService
    ) -> None:
        """Test loading permissions through groups."""
        # Create user
        email = f"test_group_{uuid.uuid4()}@example.com"
        user_repo = SqlService(model=User)
        user = user_repo.insert(
            email=email, password="password", first_name="Test", last_name="User"
        )

        # Create permission group
        system_key = f"test_group_{uuid.uuid4()}"
        group_repo = SqlService(model=PermissionGroup)
        group = group_repo.insert(name="Test Group", system_key=system_key)

        perm_repo = SqlService(model=Permission)
        permission = perm_repo.insert(category=f"test_{uuid.uuid4()}", key="write")

        # Add permission to group
        with permission_service.session_scope() as session:
            session.execute(
                permission_group_permissions.insert().values(
                    group_id=group.id, permission_id=permission.id
                )
            )

            # Add user to group
            session.execute(
                user_permission_groups.insert().values(
                    user_id=user.id, group_id=group.id
                )
            )
            session.commit()

        # Load permissions
        permissions = permission_service.load_permissions(user.id)
        assert len(permissions) == 1
        # Check that permission is in the list
        perm_tuple = next(iter(permissions))
        assert perm_tuple[1] == "write"

    def test_load_permission_groups_empty(
        self, permission_service: PermissionService
    ) -> None:
        """Test loading permission groups for user without groups."""
        email = f"test_groups_empty_{uuid.uuid4()}@example.com"
        user_repo = SqlService(model=User)
        user = user_repo.insert(
            email=email, password="password", first_name="Test", last_name="User"
        )

        groups = permission_service.load_permission_groups(user.id)
        assert groups == ()

    def test_load_permission_groups(
        self, permission_service: PermissionService
    ) -> None:
        """Test loading user's permission groups."""
        email = f"test_groups_{uuid.uuid4()}@example.com"
        user_repo = SqlService(model=User)
        user = user_repo.insert(
            email=email, password="password", first_name="Test", last_name="User"
        )

        # Create permission group
        system_key = f"test_group_{uuid.uuid4()}"
        group_repo = SqlService(model=PermissionGroup)
        group = group_repo.insert(name="Test Group", system_key=system_key)

        with permission_service.session_scope() as session:
            session.execute(
                user_permission_groups.insert().values(
                    user_id=user.id, group_id=group.id
                )
            )
            session.commit()

        groups = permission_service.load_permission_groups(user.id)
        assert len(groups) == 1
        assert groups[0].name == "Test Group"
        assert groups[0].name == "Test Group"
