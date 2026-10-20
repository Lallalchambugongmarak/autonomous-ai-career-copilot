"""Input validation and verification status for research drafts."""

from typing import Any


def review_research_draft(task_id: str, draft: str) -> dict[str, Any]:
    """Validate a research draft and report its verification status.

    This function does not independently verify factual claims or sources.
    """
    if not isinstance(task_id, str) or not task_id.strip():
        raise ValueError("task_id must be a non-empty string.")

    if not isinstance(draft, str) or not draft.strip():
        raise ValueError("Research draft must be a non-empty string.")

    return {
        "task_id": task_id.strip(),
        "status": "pending_source_verification",
        "draft_length": len(draft.strip()),
        "independently_verified": False,
        "verification_method": "input_validation_only",
        "message": (
            "Draft input is valid. Factual claims and sources "
            "have not yet been independently checked."
        ),
    }
