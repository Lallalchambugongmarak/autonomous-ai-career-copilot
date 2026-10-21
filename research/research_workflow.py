"""Connect research draft generation to verification status."""

from research.research_agent import run_research_task
from verification.research_verifier import review_research_draft


def run_research_workflow(task, client) -> dict:
    """Generate a research draft and attach its verification status.

    This workflow validates the draft input only. It does not independently
    verify factual claims, citations, or external sources.
    """
    research_result = run_research_task(task=task, client=client)

    verification = review_research_draft(
        task_id=research_result["task_id"],
        draft=research_result["content"],
    )

    return {
        **research_result,
        "status": verification["status"],
        "independently_verified": False,
        "verification": verification,
    }
