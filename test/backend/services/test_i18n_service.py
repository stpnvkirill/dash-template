"""Unit tests for I18nService."""

from app.backend.services.i18n import (
    ALLOWED_LOCALES,
    I18N_DIR,
    I18nService,
    _get_locale_path,
    get_i18n_service,
    reset_i18n_service,
)


class TestGetLocalePath:
    """Tests for _get_locale_path security function."""

    def test_valid_locale_en(self) -> None:
        """Test valid English locale."""
        path = _get_locale_path("en")
        assert path.name == "en.json"
        assert path.exists()

    def test_valid_locale_ru(self) -> None:
        """Test valid Russian locale."""
        path = _get_locale_path("ru")
        assert path.name == "ru.json"
        assert path.exists()

    def test_invalid_locale_fallback(self) -> None:
        """Test invalid locale falls back to English."""
        path = _get_locale_path("invalid")
        assert path.name == "en.json"

    def test_path_traversal_attempt(self) -> None:
        """Test path traversal attack is prevented."""
        path = _get_locale_path("../../../etc/passwd")
        assert path.name == "en.json"
        assert "/etc/passwd" not in str(path)

    def test_path_traversal_with_valid_prefix(self) -> None:
        """Test path traversal with valid locale prefix."""
        path = _get_locale_path("en../../../etc/passwd")
        # Should sanitize to just "en"
        assert path.name == "en.json"

    def test_special_characters_sanitized(self) -> None:
        """Test special characters are removed from locale."""
        path = _get_locale_path("en_US")
        # Underscore is allowed
        assert "en_US" in str(path) or path.name == "en.json"

    def test_null_byte_injection(self) -> None:
        """Test null byte injection is prevented."""
        path = _get_locale_path("en\x00.json")
        # Null byte should be filtered or fallback to en
        assert path.exists()

    def test_empty_locale(self) -> None:
        """Test empty locale falls back to English."""
        path = _get_locale_path("")
        assert path.name == "en.json"

    def test_case_sensitivity(self) -> None:
        """Test locale case handling."""
        path = _get_locale_path("EN")
        # Should fallback since "EN" != "en" in ALLOWED_LOCALES
        assert path.name == "en.json"


class TestI18nService:
    """Tests for I18nService."""

    def teardown_method(self) -> None:
        """Reset global i18n service after each test."""
        reset_i18n_service()

    def test_init_default(self) -> None:
        """Test default initialization."""
        service = I18nService()
        assert service._cache_maxsize > 0
        assert service._cache == {}

    def test_init_custom_cache_size(self) -> None:
        """Test initialization with custom cache size."""
        service = I18nService(cache_maxsize=50)
        assert service._cache_maxsize == 50  # noqa: PLR2004

    def test_get_translation_english(self) -> None:
        """Test loading English translations."""
        service = I18nService()
        translations = service.get_translation("en")

        assert isinstance(translations, dict)
        assert len(translations) > 0

    def test_get_translation_russian(self) -> None:
        """Test loading Russian translations."""
        service = I18nService()
        translations = service.get_translation("ru")

        assert isinstance(translations, dict)
        assert len(translations) > 0

    def test_get_translation_caching(self) -> None:
        """Test that translations are cached."""
        service = I18nService()

        # First call - should load from file
        translations1 = service.get_translation("en")
        assert "en" in service._cache

        # Second call - should return from cache
        translations2 = service.get_translation("en")
        assert translations1 is translations2  # Same object

    def test_get_translation_invalid_locale(self) -> None:
        """Test loading invalid locale falls back to English."""
        service = I18nService()
        translations = service.get_translation("invalid")

        # Should return English translations
        assert isinstance(translations, dict)
        en_translations = service.get_translation("en")
        assert translations == en_translations

    def test_get_text_existing_key(self) -> None:
        """Test getting existing translation key."""
        service = I18nService()
        text = service.get_text("btn_login", "en")

        assert isinstance(text, str)
        assert len(text) > 0

    def test_get_text_nonexistent_key(self) -> None:
        """Test getting non-existent key returns key."""
        service = I18nService()
        text = service.get_text("nonexistent_key_12345", "en")

        assert text == "nonexistent_key_12345"

    def test_get_text_default_locale(self) -> None:
        """Test get_text with default locale."""
        service = I18nService()
        text = service.get_text("btn_login")

        assert isinstance(text, str)

    def test_cache_lru_eviction(self) -> None:
        """Test LRU cache eviction."""
        service = I18nService(cache_maxsize=2)

        # Load 2 translations
        service.get_translation("en")
        service.get_translation("ru")

        assert len(service._cache) == 2  # noqa: PLR2004

        # Load 3rd translation (if it existed) would evict oldest
        # For now, verify cache doesn't exceed maxsize
        service.get_translation("en")  # Access "en" to make it recently used

        assert len(service._cache) <= 2  # noqa: PLR2004

    def test_get_translation_error_handling(self) -> None:
        """Test error handling for missing files."""
        service = I18nService()

        # Should not raise, should fallback to English
        translations = service.get_translation("nonexistent")
        assert isinstance(translations, dict)


class TestGlobalI18nService:
    """Tests for global i18n service functions."""

    def teardown_method(self) -> None:
        """Reset global i18n service after each test."""
        reset_i18n_service()

    def test_get_i18n_service_singleton(self) -> None:
        """Test that get_i18n_service returns singleton."""
        service1 = get_i18n_service()
        service2 = get_i18n_service()

        assert service1 is service2

    def test_reset_i18n_service(self) -> None:
        """Test resetting global i18n service."""
        service1 = get_i18n_service()
        reset_i18n_service()
        service2 = get_i18n_service()

        assert service1 is not service2


class TestAllowedLocales:
    """Tests for ALLOWED_LOCALES configuration."""

    def test_allowed_locales_contains_en(self) -> None:
        """Test that English is in allowed locales."""
        assert "en" in ALLOWED_LOCALES

    def test_allowed_locales_contains_ru(self) -> None:
        """Test that Russian is in allowed locales."""
        assert "ru" in ALLOWED_LOCALES

    def test_allowed_locales_is_frozenset(self) -> None:
        """Test that ALLOWED_LOCALES is immutable."""
        assert isinstance(ALLOWED_LOCALES, frozenset)

    def test_i18n_dir_exists(self) -> None:
        """Test that i18n directory exists."""
        assert I18N_DIR.exists()
        assert I18N_DIR.is_dir()
