from dash_iconify import DashIconify
import dash_mantine_components as dmc


def UserSection():
    return dmc.NavLink(
        label="User Name",
        description="username@email.com",
        bdrs=0,
        m=0,
        leftSection=dmc.ActionIcon(
            DashIconify(icon="mdi:user"),
            variant="light",
            size="lg",
            radius="xl",
        ),
        rightSection=DashIconify(icon="tabler-chevron-right"),
        disableRightSectionRotation=True,
        href="/me",
    )


def get_icon(icon, variant="light"):
    return dmc.ActionIcon(DashIconify(icon=icon, height=16), variant=variant)


def NavBar():
    return dmc.AppShellNavbar(
        p=0,
        bg="var(--ui-paper-color)",
        children=[
            dmc.AppShellSection(
                [dmc.Skeleton(height=35, mt="sm", animate=False) for _ in range(8)],
                grow=True,
                p="xs",
            ),
            dmc.AppShellSection(children=[dmc.Divider(), UserSection()]),
        ],
    )
