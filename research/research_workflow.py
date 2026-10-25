"""Connect research draft generation to verification status."""

from research.research_agent import run_research_task
from verification.research_verifier import review_research_draft
from dataclasses import asdict
from verification.evidence_models import (
    SourceEvidence,
    assess_provided_evidence,
)


def run_research_workflow(
    task,
    client,
    *,
    claim: str | None = None,
    evidence: tuple[SourceEvidence, ...] = (),
) -> dict:
    """Generate a draft and optionally assess caller-supplied evidence.

    Evidence assessment uses caller-provided relationship labels. It does
    not retrieve sources or independently verify factual claims.
    """
    if claim is None and evidence:
        raise ValueError(
            "A claim is required when evidence is supplied."
        )

    research_result = run_research_task(task=task, client=client)

    verification = review_research_draft(
        task_id=research_result["task_id"],
        draft=research_result["content"],
    )

    evidence_assessment = None
    if claim is not None:
        assessment = assess_provided_evidence(
            claim=claim,
            evidence=evidence,
        )
        evidence_assessment = asdict(assessment)

    return {
        **research_result,
        "status": verification["status"],
        "independently_verified": False,
        "verification": verification,
        "evidence_assessment": evidence_assessment,
    }
