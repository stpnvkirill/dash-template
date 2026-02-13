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
    },
    auth: {
        check_pwd: function (password) {
            if (!password) return [0, null];

            // Правильные регулярные выражения для клиентского кода
            // Используем 4 слеша для экранирования
            const hasMinLength = password.length >= 8;
            const hasNumber = /[0-9]/.test(password);  // Простой вариант

            // Для кириллицы используем Unicode диапазоны
            const hasLower = /[a-zа-яё]/.test(password);
            const hasUpper = /[A-ZА-ЯЁ]/.test(password);

            // Специальные символы (безопасный список)
            const hasSpecial = /[$&+,:;=?@#|'<>.^*()%!-]/.test(password);

            // Считаем баллы
            const checks = [hasMinLength, hasNumber, hasLower, hasUpper, hasSpecial];
            const score = checks.filter(v => v).length;

            // Определяем ошибку
            let error = null;
            if (!hasMinLength) {
                error = 'Minimum of 8 characters';
            } else if (score < 3) {
                error = 'The password is too weak';
            }

            return [score, error];
        }
    },
    registration: {
        'check_reg_inputs': function (pwd_error, email_error, pwd_value, email_value, first_name_value, last_name_value) {
            const allFieldsFilled = pwd_value && email_value && first_name_value && last_name_value;
            return !allFieldsFilled || pwd_error || email_error;
        }
    },
    profile: {
        check_pwd: function (error) {
            if (error) {
                return true;
            }
            return false
        }
    },
    i18n: {
        internalize: function (locale, text_id) { return locale?.[text_id.id] || '?' }
    }
});
