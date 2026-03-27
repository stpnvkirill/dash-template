"""Mantine UI theme configuration.

Module contains constants for application visual style settings,
including colors, fonts, and component parameters.
"""

# Color scheme
PRIMARY_COLOR = "indigo"
DEFAULT_GRADIENT_FROM = "teal"
DEFAULT_GRADIENT_TO = "blue"
DEFAULT_GRADIENT_ANGLE = 60

# Fonts
FONT_FAMILY = "'Inter', sans-serif"

# Component sizes
HEADER_HEIGHT = 60
NAVBAR_WIDTH = 300
NAVBAR_BREAKPOINT = "sm"

# Spacing and radii
COMPONENT_PADDING = "sm"
NAVLink_MARGIN_Y = 3
NAVLink_PADDING_X = "sm"
CONTAINER_SIZE = "xxl"
CONTAINER_PADDING = "xs"

THEME = {
    "primaryColor": PRIMARY_COLOR,
    "fontFamily": FONT_FAMILY,
    "defaultGradient": {
        "from": DEFAULT_GRADIENT_FROM,
        "to": DEFAULT_GRADIENT_TO,
        "deg": DEFAULT_GRADIENT_ANGLE,
    },
    "components": {
        "AppShellHeader": {
            "defaultProps": {"p": COMPONENT_PADDING, "withBorder": True},
        },
        "AppShellNavbar": {
            "defaultProps": {"p": COMPONENT_PADDING, "withBorder": True},
        },
        "NavLink": {
            "defaultProps": {
                "bdrs": "md",
                "my": NAVLink_MARGIN_Y,
                "px": NAVLink_PADDING_X,
            },
        },
        "Container": {"defaultProps": {"size": CONTAINER_SIZE, "p": CONTAINER_PADDING}},
    },
    "colors": {},
}
