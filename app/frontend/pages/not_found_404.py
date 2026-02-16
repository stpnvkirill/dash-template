import dash
import dash_mantine_components as dmc

from app.frontend.components.locale import _l

dash.register_page(__name__)

layout = dmc.Container(
    dmc.SimpleGrid(
        [
            dmc.Stack(
                [
                    dmc.Title(_l("404page_title"), fw=500, size=34),
                    dmc.Text(
                        _l("404page_text"),
                        c="dimmed",
                    ),
                    dmc.Anchor(
                        dmc.Button(
                            _l("404page_btn"),
                            variant="outline",
                            # size="md",
                            mt="xl",
                            fullWidth=False,
                        ),
                        href="/",
                    ),
                ],
                p="md",
                justify="center",
            ),
            dmc.Image(src="/assets/img/404.svg"),
        ],
        cols={"base": 1, "md": 2},
    ),
    size="xl",
    mt="xl",
)
