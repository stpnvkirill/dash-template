"""Internationalization (i18n) service for loading translations."""

import logging
from pathlib import Path

import orjson

from config import config

logger = logging.getLogger(__name__)

# Allowed locales for security (prevent path traversal)
ALLOWED_LOCALES = frozenset({"en", "ru"})
I18N_DIR = Path(__file__).parent.parent.parent.parent / "i18n"


def _get_locale_path(locale: str) -> Path:
    """Get safe path to locale file, preventing path traversal.

    Args:
        locale: Locale code (e.g., 'en', 'ru')

    Returns:
        Resolved path to locale JSON file.
    """
    # Sanitize locale: allow only alphanumeric and underscore
    safe_locale = "".join(c for c in locale if c.isalnum() or c == "_")

    # Check if locale is in allowed list
    if safe_locale not in ALLOWED_LOCALES:
        safe_locale = "en"

    # Build and resolve path
    locale_path = (I18N_DIR / f"{safe_locale}.json").resolve()

    # Ensure path is within i18n directory (defense in depth)
    if not str(locale_path).startswith(str(I18N_DIR.resolve())):
        locale_path = (I18N_DIR / "en.json").resolve()

    return locale_path


def _load_translation_file(locale: str) -> dict:
    """Load translation file for locale.

    Args:
        locale: Locale code.

    Returns:
        Dictionary with translations.
    """
    try:
        locale_path = _get_locale_path(locale)
        with locale_path.open() as fp:
            return orjson.loads(fp.read())
    except FileNotFoundError, orjson.JSONDecodeError:
        logger.exception("Failed to load translation for %s", locale)
        # Fallback to English
        with (I18N_DIR / "en.json").open() as fp:
            return orjson.loads(fp.read())


class I18nService:
    """Service for loading and managing translations.

    Provides cached access to translation files with security checks
    to prevent path traversal attacks.
    """

    def __init__(self, cache_maxsize: int | None = None) -> None:
        """Initialize i18n service.

        Args:
            cache_maxsize: Maximum cache size (uses config if not provided).
        """
        self._cache_maxsize = (
            cache_maxsize
            if cache_maxsize is not None
            else config.server.LRU_CACHE_MAXSIZE
        )
        # Preload all available translations at startup
        self._cache: dict[str, dict] = {}
        self._preload_translations()

    def _preload_translations(self) -> None:
        """Preload all available translations at startup."""
        for locale in ALLOWED_LOCALES:
            try:
                self._cache[locale] = _load_translation_file(locale)
            except Exception:
                logger.warning("Failed to preload translation for %s", locale)

    def get_translation(self, locale: str) -> dict:
        """Load translation file for the given locale.

        Args:
            locale: Locale code (e.g., 'en', 'ru')

        Returns:
            Dictionary with translations.
        """
        # Check cache first (includes preloaded translations)
        if locale in self._cache:
            return self._cache[locale]

        # Load and cache
        result = _load_translation_file(locale)
        self._cache[locale] = result
        return result

    def get_text(self, key: str, locale: str = "en") -> str:
        """Get translated text by key.

        Args:
            key: Translation key.
            locale: Locale code (default: 'en').

        Returns:
            Translated text or key if not found.
        """
        translation = self.get_translation(locale)
        return translation.get(key, key)


# Global i18n service instance
_i18n_service: I18nService | None = None


def get_i18n_service() -> I18nService:
    """Get global i18n service instance.

    Returns:
        I18nService instance.
    """
    global _i18n_service
    if _i18n_service is None:
        _i18n_service = I18nService()
    return _i18n_service


def reset_i18n_service() -> None:
    """Reset global i18n service (useful for testing)."""
    global _i18n_service
    _i18n_service = None
