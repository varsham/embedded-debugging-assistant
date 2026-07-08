from app.core.explainer.explainer import lookup, KNOWLEDGE_BASE
from app.models.diagnostic import DiagnosticType


def test_lookup_undefined_ref():
    explanation = lookup(DiagnosticType.UNDEFINED_REF)

    assert explanation.error_summary == (
        "Could not find a definition for a referenced symbol."
    )

    assert len(explanation.common_causes) > 0
    assert explanation.what_happened
    assert explanation.how_to_fix


def test_lookup_overflow():
    explanation = lookup(DiagnosticType.OVERFLOW)

    assert explanation.error_summary == (
        "A value exceeded the space available to store it."
    )

    assert explanation.common_causes
    assert explanation.what_happened
    assert explanation.how_to_fix


def test_lookup_implicit_declaration():
    explanation = lookup(DiagnosticType.IMPLICIT_DEC)

    assert explanation.error_summary == (
        "A function was used before it was declared."
    )

    assert explanation.common_causes
    assert explanation.what_happened
    assert explanation.how_to_fix


def test_lookup_unused_variable():
    explanation = lookup(DiagnosticType.UNUSED_VAR)

    assert explanation.error_summary == (
        "A variable was created but never used."
    )

    assert explanation.common_causes
    assert explanation.what_happened
    assert explanation.how_to_fix


def test_lookup_unknown():
    explanation = lookup(DiagnosticType.UNKNOWN)

    assert explanation.error_summary
    assert explanation.common_causes
    assert explanation.what_happened
    assert explanation.how_to_fix


def test_all_diagnostic_types_have_explanations():
    for diagnostic_type in DiagnosticType:
        explanation = lookup(diagnostic_type)

        assert explanation is not None
        assert explanation.error_summary
        assert explanation.what_happened
        assert len(explanation.common_causes) > 0
        assert explanation.how_to_fix


def test_knowledge_base_contains_all_types():
    assert set(KNOWLEDGE_BASE.keys()) == set(DiagnosticType)