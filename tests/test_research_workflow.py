"""Tests for the research workflow integration."""

from unittest.mock import patch

from shared_state.tasks import AgentTask
from research.research_workflow import run_research_workflow


def test_research_draft_is_sent_for_verification():
    task = AgentTask(
        task_id="research-test-001",
        description="Compare LangGraph and CrewAI.",
        agent="research",
        priority="medium",
    )
    draft = (
        "Draft comparison. This content has not been independently "
        "fact-checked."
    )

    with patch(
        "research.research_workflow.run_research_task",
        return_value={
            "task_id": task.task_id,
            "agent": "research",
            "status": "draft_generated",
            "content": draft,
            "independently_verified": False,
        },
    ) as mock_research:
        result = run_research_workflow(task=task, client=None)

    mock_research.assert_called_once_with(task=task, client=None)
    assert result["task_id"] == task.task_id
    assert result["content"] == draft
    assert result["status"] == "pending_source_verification"
    assert result["independently_verified"] is False
    assert (
        result["verification"]["verification_method"]
        == "input_validation_only"
    )
