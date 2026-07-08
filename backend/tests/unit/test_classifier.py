from app.core.classifier.classifier import classify
from app.models.diagnostic import (
    Diagnostic,
    DiagnosticType,
    LinkerError,
    LinkerErrorKind,
    Location,
    Severity
)

def test_classify_linker_overflow():
    linker_error = LinkerError(
        kind=LinkerErrorKind.OVERFLOW
    )

    assert classify(linker_error) == DiagnosticType.OVERFLOW


def test_classify_linker_undefined_ref():
    linker_error = LinkerError(
        kind=LinkerErrorKind.UNDEFINED_REF
    )

    assert classify(linker_error) == DiagnosticType.UNDEFINED_REF


def test_classify_implicit_declaration():
    diagnostic = Diagnostic(
        location=Location(
            file_path="main.c",
            line_num=1,
        ),
        severity=Severity.ERROR,
        msg_txt="implicit declaration of function 'printf'",
    )

    assert classify(diagnostic) == DiagnosticType.IMPLICIT_DEC


def test_classify_unused_variable():
    diagnostic = Diagnostic(
        location=Location(
            file_path="main.c",
            line_num=2,
        ),
        severity=Severity.WARNING,
        msg_txt="unused variable 'x'",
    )

    assert classify(diagnostic) == DiagnosticType.UNUSED_VAR


def test_classify_overflow_diagnostic():
    diagnostic = Diagnostic(
        location=Location(
            file_path="main.c",
            line_num=3,
        ),
        severity=Severity.ERROR,
        msg_txt="integer overflow in expression",
    )

    assert classify(diagnostic) == DiagnosticType.OVERFLOW


def test_classify_unknown_diagnostic():
    diagnostic = Diagnostic(
        location=Location(
            file_path="main.c",
            line_num=4,
        ),
        severity=Severity.ERROR,
        msg_txt="expected ';' before '}' token",
    )

    assert classify(diagnostic) == DiagnosticType.UNKNOWN