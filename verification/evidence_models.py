"""Structured models for evidence-backed research claim assessment.

These models validate supplied records. They do not retrieve sources,
prove factual accuracy, or independently verify claims.
"""

from dataclasses import dataclass
from typing import Literal
from urllib.parse import urlparse


EvidenceRelationship = Literal[
    "supports",
    "contradicts",
    "contextual",
    "irrelevant",
]

AssessmentStatus = Literal[
    "supported_by_provided_evidence",
    "contradicted_by_provided_evidence",
    "inconclusive",
]


@dataclass(frozen=True)
class SourceEvidence:
    """A source reference and an excerpt supplied for review."""

    source_url: str
    title: str
    excerpt: str
    relationship: EvidenceRelationship

    def __post_init__(self):
        if not isinstance(self.source_url, str):
            raise ValueError("source_url must be a string.")

        parsed_url = urlparse(self.source_url.strip())

        if (
            parsed_url.scheme not in {"http", "https"}
            or not parsed_url.netloc
        ):
            raise ValueError(
                "source_url must be an absolute HTTP or HTTPS URL."
            )

        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("Source title must be non-empty.")

        if not isinstance(self.excerpt, str) or not self.excerpt.strip():
            raise ValueError("Evidence excerpt must be non-empty.")

        allowed_relationships = {
            "supports",
            "contradicts",
            "contextual",
            "irrelevant",
        }
        if self.relationship not in allowed_relationships:
            raise ValueError("Invalid evidence relationship.")

        # Store normalized text without modifying the original source URL.
        object.__setattr__(self, "source_url", self.source_url.strip())
        object.__setattr__(self, "title", self.title.strip())
        object.__setattr__(self, "excerpt", self.excerpt.strip())


@dataclass(frozen=True)
class ClaimAssessment:
    """An assessment of a claim against supplied evidence."""

    claim: str
    status: AssessmentStatus
    evidence: tuple[SourceEvidence, ...]
    rationale: str
    independently_verified: bool = False

    def __post_init__(self):
        if not isinstance(self.claim, str) or not self.claim.strip():
            raise ValueError("Claim must be a non-empty string.")

        if not isinstance(self.rationale, str) or not self.rationale.strip():
            raise ValueError("Assessment rationale must be non-empty.")

        if not isinstance(self.evidence, tuple):
            raise ValueError("Evidence must be supplied as a tuple.")

        if not all(
            isinstance(item, SourceEvidence)
            for item in self.evidence
        ):
            raise ValueError(
                "Every evidence item must be a SourceEvidence record."
            )

        allowed_statuses = {
            "supported_by_provided_evidence",
            "contradicted_by_provided_evidence",
            "inconclusive",
        }
        if self.status not in allowed_statuses:
            raise ValueError("Invalid assessment status.")

        if self.independently_verified is not False:
            raise ValueError(
                "This model cannot certify independent verification."
            )

        object.__setattr__(self, "claim", self.claim.strip())
        object.__setattr__(self, "rationale", self.rationale.strip())

def assess_provided_evidence(
    claim: str,
    evidence: tuple[SourceEvidence, ...],
) -> ClaimAssessment:
    """Create a preliminary assessment from supplied relationship labels.

    This function does not inspect whether excerpts truly support a claim.
    Relationship labels are caller-provided and must not be treated as
    independently established facts.
    """
    if not isinstance(claim, str) or not claim.strip():
        raise ValueError("Claim must be a non-empty string.")

    if not isinstance(evidence, tuple):
        raise ValueError("Evidence must be supplied as a tuple.")

    if not all(isinstance(item, SourceEvidence) for item in evidence):
        raise ValueError(
            "Every evidence item must be a SourceEvidence record."
        )

    relationships = {item.relationship for item in evidence}
    has_support = "supports" in relationships
    has_contradiction = "contradicts" in relationships

    if not evidence:
        status = "inconclusive"
        rationale = "No evidence was supplied for assessment."
    elif has_support and has_contradiction:
        status = "inconclusive"
        rationale = (
            "Supplied evidence has conflicting relationship labels. "
            "The claim requires further review."
        )
    elif has_contradiction:
        status = "contradicted_by_provided_evidence"
        rationale = (
            "All decisive supplied relationship labels indicate "
            "contradiction. The excerpts have not been independently "
            "checked against the claim."
        )
    elif has_support:
        status = "supported_by_provided_evidence"
        rationale = (
            "Supplied relationship labels indicate support, but the "
            "excerpts have not been independently checked against "
            "the claim."
        )
    else:
        status = "inconclusive"
        rationale = (
            "No supplied relationship label indicates direct support "
            "or contradiction."
        )

    return ClaimAssessment(
        claim=claim,
        status=status,
        evidence=evidence,
        rationale=rationale,
        independently_verified=False,
    )
