"""Integration tests for optional research evidence assessment."""

from unittest.mock import patch

import pytest

from research.research_workflow import run_research_workflow
from shared_state.tasks import AgentTask
from verification.evidence_models import SourceEvidence


def make_task():
    return AgentTask(
        task_id="evidence-integration-001",
        description="Research an example topic.",
        agent="research",
        priority="medium",
    )


def make_evidence(relationship="supports"):
    return SourceEvidence(
        source_url="https://example.com/research",
        title="Example source",
        excerpt="Example excerpt supplied for testing.",
        relationship=relationship,
    )


def mock_research_result(task):
    return {
        "task_id": task.task_id,
        "agent": "research",
        "status": "draft_generated",
        "content": "Example research draft.",
        "independently_verified": False,
    }


def test_existing_workflow_without_evidence_is_preserved():
    task = make_task()

    with patch(
        "research.research_workflow.run_research_task",
        side_effect=lambda task, client: mock_research_result(task),
    ):
        result = run_research_workflow(task=task, client=None)

    assert result["status"] == "pending_source_verification"
    assert result["independently_verified"] is False
    assert result["evidence_assessment"] is None


def test_workflow_returns_preliminary_evidence_assessment():
    task = make_task()

    with patch(
        "research.research_workflow.run_research_task",
        side_effect=lambda task, client: mock_research_result(task),
    ):
        result = run_research_workflow(
            task=task,
            client=None,
            claim="Example claim.",
            evidence=(make_evidence("supports"),),
        )

    assessment = result["evidence_assessment"]
    assert assessment["claim"] == "Example claim."
    assert assessment["status"] == "supported_by_provided_evidence"
    assert assessment["independently_verified"] is False
    assert result["independently_verified"] is False
    assert result["status"] == "pending_source_verification"


def test_claim_without_evidence_is_inconclusive():
    task = make_task()

    with patch(
        "research.research_workflow.run_research_task",
        side_effect=lambda task, client: mock_research_result(task),
    ):
        result = run_research_workflow(
            task=task,
            client=None,
            claim="Example claim.",
        )

    assert result["evidence_assessment"]["status"] == "inconclusive"
    assert result["evidence_assessment"]["evidence"] == ()


def test_evidence_without_claim_is_rejected_before_research():
    task = make_task()

    with patch(
        "research.research_workflow.run_research_task"
    ) as mock_research:
        with pytest.raises(ValueError, match="claim is required"):
            run_research_workflow(
                task=task,
                client=None,
                evidence=(make_evidence(),),
            )

    mock_research.assert_not_called()


def test_conflicting_evidence_remains_inconclusive():
    task = make_task()

    with patch(
        "research.research_workflow.run_research_task",
        side_effect=lambda task, client: mock_research_result(task),
    ):
        result = run_research_workflow(
            task=task,
            client=None,
            claim="Example claim.",
            evidence=(
                make_evidence("supports"),
                make_evidence("contradicts"),
            ),
        )

    assert result["evidence_assessment"]["status"] == "inconclusive"
    assert result["evidence_assessment"]["independently_verified"] is False
