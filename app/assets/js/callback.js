window.dash_clientside = Object.assign({}, window.dash_clientside, {
    app_shell: {
        // Dark/Light theme
        change_data_in_theme_store: function (
            n_clicks,
            theme_store_data
        ) {
            if (theme_store_data) {
                if (n_clicks) {
                    const scheme = theme_store_data == "dark" ? "light" : "dark";
                    return scheme;
                }
                return dash_clientside.no_update;
            } else {
                return "light";
            }
        },
        change_mantine_theme_provider: function (data) { return data; },
        open_navbar: function (opened, navbar) {
            navbar = navbar || {};
            navbar.collapsed = { mobile: !opened };
            return navbar;
        }
    }
});
