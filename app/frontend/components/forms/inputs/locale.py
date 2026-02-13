import dash_mantine_components as dmc


def LanguagePicker():
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
        variant="unstaled",
        clearable=False,
        allowDeselect=False,
    )
