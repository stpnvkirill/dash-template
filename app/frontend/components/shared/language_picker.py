import dash_mantine_components as dmc


def LanguagePicker() -> dmc.Select:
    """Application language picker component.

    Returns:
        Select component with flags for locale selection (en/ru).
    """
    return dmc.Select(
        id="locale-selector",
        value="en",
        data=[
            {"label": "🇬🇧", "value": "en"},
            {"label": "🇷🇺", "value": "ru"},
        ],
        w=45,
        persistence_type="local",
        persistence=True,
        rightSection=None,
        withCheckIcon=False,
        variant="filled",
        clearable=False,
        allowDeselect=False,
    )
