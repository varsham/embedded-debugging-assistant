import re
from app.models.diagnostic import LinkerError, Diagnostic, DiagnosticType

def classify(diagnostic: Diagnostic | LinkerError) -> DiagnosticType:
    if (diagnostic isinstance LinkerError):
        # use kind directly, no regex needed
    else:
        # match msg_txt against patterns