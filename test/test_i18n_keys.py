import json
from pathlib import Path
import re

import pytest


@pytest.fixture
def i18n_files():
    translations = {}
    json_files = Path().glob(pattern="i18n/*.json")

    for json_file in json_files:
        lang = Path(json_file).stem
        with Path(json_file).open(encoding="utf-8") as f:
            translations[lang] = json.load(f)

    return translations


@pytest.fixture
def used_keys():
    keys = set()
    pattern = r'_l\(\s*[\'"]([^\'"]+)[\'"]\s*\)'

    python_files = Path().glob(pattern="app/**/*.py", recurse_symlinks=True)

    for py_file in python_files:
        with Path(py_file).open(encoding="utf-8") as f:
            content = f.read()
            matches = re.findall(pattern, content)
            keys.update(matches)

    return keys


def test_all_languages_have_same_keys(i18n_files):
    languages = list(i18n_files.keys())

    if len(languages) < 2:  # noqa: PLR2004
        return

    base_lang = "en" if "en" in languages else languages[0]
    base_keys = set(i18n_files[base_lang].keys())

    for lang in languages:
        lang_keys = set(i18n_files[lang].keys())

        missing = base_keys - lang_keys
        extra = lang_keys - base_keys

        assert not missing, f"{lang} keys are missing: {missing}"
        assert not extra, f"{lang} There are extra keys: {extra}"


def test_all_used_keys_exist(i18n_files, used_keys):
    languages = list(i18n_files.keys())

    for key in used_keys:
        for lang in languages:
            assert key in i18n_files[lang], f"The key '{key}' is missing in {lang}.json"


def test_no_unused_keys(i18n_files, used_keys):
    for lang, translations in i18n_files.items():
        unused = set(translations.keys()) - used_keys
        assert not unused, f"{lang}.json contains unused keys: {unused}"


def test_translations_format(i18n_files):
    for lang, translations in i18n_files.items():
        for key, value in translations.items():
            assert value and value.strip(), (
                f"{lang}.json: the key '{key}' has an empty value"
            )
            assert "  " not in value, (
                f"{lang}.json: the key '{key}' contains double spaces"
            )
