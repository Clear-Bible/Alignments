"""Test Language.py."""

import pytest

from pydantic import ValidationError

from bible_alignments.languages import Language


class TestScript:
    """Test SCRIPT enumeration."""

    def test_value(self) -> None:
        """Test value."""
        assert Language.SCRIPT["Latn"].value == "Latin"


class TestLanguage:
    """Test Language class."""

    def test_init(self) -> None:
        """Test initialization."""
        lang = Language.Language(
            BCP47="tu",
            Language="Turkmen",
            ISO="tuk",
            Resource_Level=1,
            RL_Rationale="",
            Inclusive_code="",
            script="",
        )
        assert lang.Language == "Turkmen"

    def test_init_BCP47(self) -> None:
        """Test initialization of BCP47 attribute."""
        with pytest.raises(ValidationError):
            Language.Language(
                # only 2-3 chars allowed
                BCP47="tusk",
                Language="Turkmen",
                ISO="tuk",
                Resource_Level=1,
                RL_Rationale="",
                Inclusive_code="",
                script="",
            )

    def test_init_ISO_short(self) -> None:
        """Test initialization of ISO attribute."""
        with pytest.raises(ValidationError):
            Language.Language(
                BCP47="tu",
                Language="Turkmen",
                # too short
                ISO="tu",
                Resource_Level=1,
                RL_Rationale="",
                Inclusive_code="",
                script="",
            )

    def test_init_ISO_long(self) -> None:
        """Test initialization of ISO attribute."""
        with pytest.raises(ValidationError):
            Language.Language(
                BCP47="tu",
                Language="Turkmen",
                # too long
                ISO="tuktu",
                Resource_Level=1,
                RL_Rationale="",
                Inclusive_code="",
                script="",
            )

    def test_init_RL(self) -> None:
        """Test initialization of Resource_Level attribute."""
        with pytest.raises(ValidationError):
            Language.Language(
                BCP47="tu",
                Language="Turkmen",
                ISO="tuk",
                # only goes to 4
                Resource_Level=5,
                RL_Rationale="",
                Inclusive_code="",
                script="",
            )


class TestLanguageManager:
    """Test LanguageManager."""

    lm = Language.LanguageManager()

    def test_reading(self) -> None:
        """Test reading."""
        # fragile approximation
        assert len(self.lm) > 200
        assert "tuk" in self.lm
        assert self.lm["tuk"].BCP47 == "tk"
        assert self.lm["ory"].script == "Oriya"

    def test_languages_for_script(self) -> None:
        """Test languages_for_script."""
        langs = {lang.Language for lang in self.lm.languages_for_script("Bengali")}
        assert langs == {"Assamese", "Bengali"}
