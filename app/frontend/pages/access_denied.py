import dash
import dash_mantine_components as dmc

from app.frontend.components.locale import _l

dash.register_page(
    __name__,
    "/access-denied",
)

layout = dmc.Container(
    dmc.SimpleGrid(
        [
            dmc.Stack(
                [
                    dmc.Title(_l("accessdenied_title"), fw=600, size=32),
                    dmc.Text(
                        _l("accessdenied_text"),
                        c="dimmed",
                        size="md",
                    ),
                    dmc.List(
                        [
                            dmc.ListItem(_l("accessdenied_hint_admin")),
                            dmc.ListItem(_l("accessdenied_hint_support")),
                        ],
                        size="sm",
                        icon="⚠",
                    ),
                    dmc.Anchor(
                        dmc.Button(
                            _l("accessdenied_home_btn"),
                            variant="outline",
                            mt="xl",
                            fullWidth=False,
                        ),
                        href="/",
                    ),
                ],
                p="md",
                justify="center",
            ),
            dmc.Center(
                dmc.Image(
                    src="/assets/img/404.svg",
                    style={"maxHeight": 360},
                    alt="Access denied illustration",
                )
            ),
        ],
        cols={"base": 1, "md": 2},
        spacing="xl",
    ),
    size="xl",
    mt="xl",
)
