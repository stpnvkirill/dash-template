from dash_iconify import DashIconify
import dash_mantine_components as dmc


def ChangeColorIcon():
    return dmc.ActionIcon(
        [
            DashIconify(
                icon="akar-icons:sun",
                width=25,
                id="light-theme-icon",
                color="yellow",
            ),
            DashIconify(
                icon="akar-icons:moon",
                width=25,
                id="dark-theme-icon",
                color="gray",
            ),
        ],
        variant="transparent",
        id="color-scheme-toggle",
        size="lg",
    )


def CallNavbarIcon():
    return dmc.Burger(id="burger", size="sm", hiddenFrom="sm", opened=False)


def Header():
    return dmc.AppShellHeader(
        dmc.Group(
            justify="space-between",
            children=[
                dmc.Group(
                    [
                        dmc.Anchor(
                            dmc.Group(
                                [
                                    dmc.Image(
                                        src="/assets/logo-dark.svg",
                                        h=36,
                                        fit="contain",
                                        lightHidden=True,
                                    ),
                                    dmc.Image(
                                        src="/assets/logo.svg",
                                        h=36,
                                        fit="contain",
                                        darkHidden=True,
                                    ),
                                ]
                            ),
                            href="/",
                        )
                    ],
                    align="center",
                    pl="sm",
                ),
                dmc.Group(
                    justify="flex-end",
                    children=[ChangeColorIcon(), CallNavbarIcon()],
                ),
            ],
        ),
        bg="var(--ui-paper-color)",
    )
