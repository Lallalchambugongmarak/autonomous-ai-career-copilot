"""Permanent tests for preliminary evidence assessment."""

import pytest

from verification.evidence_models import (
    SourceEvidence,
    assess_provided_evidence,
)


def make_evidence(relationship):
    return SourceEvidence(
        source_url="https://example.com/research",
        title="Example test source",
        excerpt="Example excerpt used only for testing.",
        relationship=relationship,
    )


def test_no_evidence_is_inconclusive():
    result = assess_provided_evidence("Example claim", ())

    assert result.status == "inconclusive"
    assert result.independently_verified is False


def test_support_label_is_preliminary_only():
    result = assess_provided_evidence(
        "Example claim",
        (make_evidence("supports"),),
    )

    assert result.status == "supported_by_provided_evidence"
    assert result.independently_verified is False
    assert "not been independently checked" in result.rationale


def test_contradiction_label_is_preliminary_only():
    result = assess_provided_evidence(
        "Example claim",
        (make_evidence("contradicts"),),
    )

    assert result.status == "contradicted_by_provided_evidence"
    assert result.independently_verified is False
    assert "not been independently checked" in result.rationale


def test_conflicting_labels_are_inconclusive():
    result = assess_provided_evidence(
        "Example claim",
        (
            make_evidence("supports"),
            make_evidence("contradicts"),
        ),
    )

    assert result.status == "inconclusive"


@pytest.mark.parametrize("relationship", ["contextual", "irrelevant"])
def test_non_decisive_labels_are_inconclusive(relationship):
    result = assess_provided_evidence(
        "Example claim",
        (make_evidence(relationship),),
    )

    assert result.status == "inconclusive"


def test_empty_claim_is_rejected():
    with pytest.raises(ValueError):
        assess_provided_evidence(" ", ())


def test_evidence_must_be_a_tuple():
    with pytest.raises(ValueError):
        assess_provided_evidence("Example claim", [])


def test_invalid_evidence_record_is_rejected():
    with pytest.raises(ValueError):
        assess_provided_evidence("Example claim", ("not evidence",))
