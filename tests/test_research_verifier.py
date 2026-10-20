"""Tests for the research verifier."""

import pytest

from verification.research_verifier import review_research_draft


def test_valid_draft_is_pending_source_verification():
    result = review_research_draft(
        task_id="research-001",
        draft="Compare LangGraph and CrewAI.",
    )

    assert result["task_id"] == "research-001"
    assert result["status"] == "pending_source_verification"
    assert result["independently_verified"] is False
    assert result["verification_method"] == "input_validation_only"


@pytest.mark.parametrize(
    "task_id,draft",
    [
        ("", "A valid draft"),
        ("   ", "A valid draft"),
        ("research-002", ""),
        ("research-003", "   "),
    ],
)
def test_invalid_inputs_are_rejected(task_id, draft):
    with pytest.raises(ValueError):
        review_research_draft(task_id=task_id, draft=draft)
