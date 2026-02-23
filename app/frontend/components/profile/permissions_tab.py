import dash_mantine_components as dmc

from app.backend.domain import PermissionGroupDto, UserDto
from app.frontend.components.locale import _l


def _render_roles(groups: tuple[PermissionGroupDto, ...]):
    if not groups:
        return dmc.Text(_l("profilepage_permissions_no_roles"), c="dimmed")

    badges = []
    for group in groups:
        label = group.name
        if group.system_key:
            label = f"{group.name} ({group.system_key})"
        badges.append(
            dmc.Badge(
                label,
                size="sm",
                radius="sm",
                c="blue",
                variant="light",
            )
        )
    return dmc.Group(badges, gap="xs", wrap=True)


def _render_permissions(permissions: frozenset[tuple[str, str]]):
    sorted_perms = sorted(permissions, key=lambda item: (item[0], item[1]))
    if not sorted_perms:
        return dmc.Text(
            _l("profilepage_permissions_no_permissions"),
            c="dimmed",
        )

    rows = []
    for category, key in sorted_perms:
        rows.append(
            dmc.ListItem(
                dmc.Group(
                    [
                        dmc.Text(category, fw=500, size="sm"),
                        dmc.Text(key, size="sm", c="dimmed"),
                    ],
                    justify="space-between",
                )
            )
        )

    return dmc.List(children=rows)


def _section(title, content):
    return dmc.Card(
        [
            dmc.Text(title, fw=600, size="sm"),
            dmc.Space(h="xs"),
            content,
        ],
        shadow="sm",
        radius="md",
        withBorder=True,
        p="md",
    )


def PermissionsTab(user: UserDto):
    return dmc.Stack(
        [
            _section(
                _l("profilepage_permissions_roles_title"),
                _render_roles(user.permission_groups),
            ),
            _section(
                _l("profilepage_permissions_permissions_title"),
                _render_permissions(user.permissions),
            ),
        ]
    )
