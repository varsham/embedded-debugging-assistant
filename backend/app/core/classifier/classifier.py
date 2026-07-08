import re
from app.models.diagnostic import LinkerError, LinkerErrorKind, Diagnostic, DiagnosticType

def classify(diagnostic: Diagnostic | LinkerError) -> DiagnosticType:
    if isinstance(diagnostic, LinkerError):
        if diagnostic.kind == LinkerErrorKind.OVERFLOW:
            return DiagnosticType.OVERFLOW
        elif diagnostic.kind == LinkerErrorKind.UNDEFINED_REF:
            return DiagnosticType.UNDEFINED_REF
        else:
            return DiagnosticType.UNKNOWN
    else:
        msg = diagnostic.msg_txt.lower()

        if re.search(r"\bimplicit declaration(?: of function)?\b", msg):
            return DiagnosticType.IMPLICIT_DEC

        elif re.search(r"\bunused (?:variable|parameter|function)\b", msg):
            return DiagnosticType.UNUSED_VAR

        elif re.search(r"\boverflow\b", msg):
            return DiagnosticType.OVERFLOW

        else:
            return DiagnosticType.UNKNOWN