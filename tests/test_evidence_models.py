"""Permanent tests for structured research evidence models."""

import pytest

from verification.evidence_models import (
    ClaimAssessment,
    SourceEvidence,
)


def make_evidence(**overrides):
    values = {
        "source_url": "https://example.com/research",
        "title": "Example research source",
        "excerpt": "Example excerpt supplied as test data.",
        "relationship": "supports",
    }
    values.update(overrides)
    return SourceEvidence(**values)


def test_valid_source_evidence_is_accepted():
    evidence = make_evidence()

    assert evidence.source_url == "https://example.com/research"
    assert evidence.relationship == "supports"
    assert evidence.excerpt


def test_valid_assessment_is_not_certified_as_independently_verified():
    evidence = make_evidence()

    assessment = ClaimAssessment(
        claim="Example claim for testing.",
        status="supported_by_provided_evidence",
        evidence=(evidence,),
        rationale="Example test rationale.",
    )

    assert assessment.evidence == (evidence,)
    assert assessment.independently_verified is False


@pytest.mark.parametrize(
    "url",
    [
        "",
        "not-a-url",
        "file:///private/data",
        "ftp://example.com/research",
    ],
)
def test_invalid_source_urls_are_rejected(url):
    with pytest.raises(ValueError):
        make_evidence(source_url=url)


def test_empty_source_title_is_rejected():
    with pytest.raises(ValueError):
        make_evidence(title="   ")


def test_empty_excerpt_is_rejected():
    with pytest.raises(ValueError):
        make_evidence(excerpt="")


def test_invalid_evidence_relationship_is_rejected():
    with pytest.raises(ValueError):
        make_evidence(relationship="unknown")


def test_empty_claim_is_rejected():
    with pytest.raises(ValueError):
        ClaimAssessment(
            claim=" ",
            status="inconclusive",
            evidence=(),
            rationale="No claim was supplied.",
        )


def test_empty_rationale_is_rejected():
    with pytest.raises(ValueError):
        ClaimAssessment(
            claim="Example claim",
            status="inconclusive",
            evidence=(),
            rationale=" ",
        )


def test_invalid_assessment_status_is_rejected():
    with pytest.raises(ValueError):
        ClaimAssessment(
            claim="Example claim",
            status="verified",
            evidence=(),
            rationale="Invalid status test.",
        )


def test_evidence_must_be_a_tuple_of_source_evidence():
    with pytest.raises(ValueError):
        ClaimAssessment(
            claim="Example claim",
            status="inconclusive",
            evidence=["not a SourceEvidence object"],
            rationale="Invalid evidence container.",
        )


def test_independent_verification_cannot_be_self_certified():
    with pytest.raises(ValueError):
        ClaimAssessment(
            claim="Example claim",
            status="supported_by_provided_evidence",
            evidence=(make_evidence(),),
            rationale="Test self-certification protection.",
            independently_verified=True,
        )
