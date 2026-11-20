"""Unit tests for cinema_nexus.schemas schemas and enums."""

import pytest
from pydantic import ValidationError

from schemas.actions import WatchlistAction
from schemas.payloads import GuardrailResult, WatchlistResult


class TestWatchlistActionEnum:
    def test_enum_members_and_values(self):
        assert WatchlistAction.ADD.value == "add"
        assert WatchlistAction.REMOVE.value == "remove"
        assert WatchlistAction.LIST.value == "list"

    def test_enum_instantiation_from_valid_strings(self):
        assert WatchlistAction("add") is WatchlistAction.ADD
        assert WatchlistAction("remove") is WatchlistAction.REMOVE
        assert WatchlistAction("list") is WatchlistAction.LIST

    def test_enum_invalid_value_raises_value_error(self):
        with pytest.raises(ValueError):
            WatchlistAction("delete")


class TestWatchlistResultModel:
    def test_default_values(self):
        result = WatchlistResult(status="added")
        assert result.status == "added"
        assert result.title is None
        assert result.watchlist == []
        assert result.count == 0
        assert result.message is None

    def test_populated_model_serialization(self):
        result = WatchlistResult(
            status="added",
            title="Dune: Part Two",
            watchlist=["Inception", "Dune: Part Two"],
            count=2,
            message="'Dune: Part Two' added to your watchlist.",
        )
        data = result.model_dump()
        assert data["status"] == "added"
        assert data["title"] == "Dune: Part Two"
        assert data["count"] == 2
        assert "Inception" in data["watchlist"]

    def test_missing_required_status_raises_validation_error(self):
        with pytest.raises(ValidationError):
            WatchlistResult()


class TestGuardrailResultModel:
    def test_passed_guardrail(self):
        result = GuardrailResult(passed=True)
        assert result.passed is True
        assert result.reason is None
        assert result.patterns_matched == []

    def test_failed_guardrail_serialization(self):
        result = GuardrailResult(
            passed=False,
            reason="prompt_injection",
            patterns_matched=["developer\\s+mode"],
        )
        assert result.passed is False
        assert result.reason == "prompt_injection"
        assert len(result.patterns_matched) == 1

        json_str = result.model_dump_json()
        assert '"passed":false' in json_str
        assert '"prompt_injection"' in json_str

    def test_missing_passed_flag_raises_validation_error(self):
        with pytest.raises(ValidationError):
            GuardrailResult()
