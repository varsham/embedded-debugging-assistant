import re
from app.models.diagnostic import (
    BuildOutput, Diagnostic, DiagnosticNote, Location, Severity
)

def classify_line(line: str) -> str:
    if re.search(r"^[^:]+:\d+:(\d+:)? fatal error:", line):
        return "fatal error"
    elif re.search(r"^[^:]+:\d+:(\d+:)? error:", line):
        return "error"
    elif re.search(r"^[^:]+:\d+:(\d+:)? warning:", line):
        return "warning"
    elif re.search(r"^[^:]+:\d+:(\d+:)? note:", line):
        return "note"
    elif re.search(r"^[^:]+:\s+(In function|At top level|In file included from)", line):
        return "context"
    elif re.search(r"\d+\s*\|", line):
        return "source"
        # example: 42 |     ...
    elif re.search(r"\|.*?\^+~*", line):
        return "caret"
    else:
        return "other"

def parse_diagnostic_line(line: str) -> dict | None:
    pattern = (
        r"^(?P<file>[^:]+):"                    # 1. File path
        r"(?P<line>\d+):"                       # 2. Line number
        r"(?:(?P<column>\d+):)?"                # 3. Optional Column number
        r"\s*(?P<severity>fatal error|error|warning|note):\s*" # 4. Severity
        r"(?P<message>.*?)"                     # 5. Message
        r"(?:\s*\[(?P<flag>-W[a-zA-Z0-9-]+)\])?$" # 6. Optional compiler flag
    )
    match = re.match(pattern, line)

    if match is None:
        return None
    return {
        "file_path": match.group('file'),
        "line_num": int(match.group('line')),
        "col_num": int(match.group('column')) if match.group('column') else None,
        "severity": match.group('severity'),
        "message": match.group('message'),
        "flag": match.group('flag'),
    }

def parse_gcc_output(log: str) -> BuildOutput:
    lines = log.splitlines()

    state = "IDLE"
    current_context: str | None = None
    current_diagnostic: Diagnostic | None = None
    current_note: DiagnosticNote | None = None
    diagnostics: list[Diagnostic] = []
    error_count = 0
    warning_count = 0

    for line in lines:
        line_type = classify_line(line)

        if state == "IDLE":
            if line_type in ("error", "warning", "fatal error"):
                current_diagnostic = _build_diagnostic(line, current_context)

                if line_type in ("error", "fatal error"):
                    error_count += 1
                elif line_type == "warning":
                    warning_count += 1
                
                state = "IN_DIAGNOSTIC"
            elif line_type == "context":
                # does not create a diagnostic
                m = re.match(r"^[^:]+:\s+(.+?):\s*$", line)
                if m:
                    current_context = m.group(1)

        elif state == "IN_DIAGNOSTIC":
            if line_type in ("error", "warning", "fatal error"):
                diagnostics.append(current_diagnostic)
                current_diagnostic = _build_diagnostic(line, current_context)

                if line_type in ("error", "fatal error"):
                    error_count += 1
                elif line_type == "warning":
                    warning_count += 1
            elif line_type == "note":
                current_note = _build_note(line)
                state = "IN_NOTE"
            elif line_type == "source":
                current_diagnostic.source_excerpt = line
            elif line_type == "caret":
                current_diagnostic.caret_line = line
            elif line_type == "context":
                # does not create a diagnostic
                m = re.match(r"^[^:]+:\s+(.+?):\s*$", line)
                if m:
                    current_context = m.group(1)
        
        elif state == "IN_NOTE":
            if line_type in ("error", "warning", "fatal error"):
                current_diagnostic.notes.append(current_note)
                current_note = None
                diagnostics.append(current_diagnostic)          
                current_diagnostic = _build_diagnostic(line, current_context)
                if line_type in ("error", "fatal error"):
                    error_count += 1
                elif line_type == "warning":
                    warning_count += 1

                state = "IN_DIAGNOSTIC"
            elif line_type == "note":
                current_diagnostic.notes.append(current_note)
                current_note = _build_note(line)
                # state stays the same
            elif line_type == "source":
                current_note.source_line = line
            elif line_type == "caret":
                current_note.caret_line = line
    
    if state == "IN_NOTE" and current_note is not None:
        current_diagnostic.notes.append(current_note)
    if current_diagnostic is not None:
        diagnostics.append(current_diagnostic)

    return BuildOutput(
        log_txt=log,
        diagnostics=diagnostics,
        error_count=error_count,
        warning_count=warning_count
    )

def _build_diagnostic(line: str, context: str | None) -> Diagnostic:
    parsed = parse_diagnostic_line(line)
    loc = Location(
        file_path=parsed["file_path"],
        line_num=parsed["line_num"],
        col_num=parsed["col_num"],
    )
    return Diagnostic(
        location=loc,
        severity=Severity(parsed["severity"]),
        msg_txt=parsed["message"],
        gcc_flag=parsed["flag"],
        function_context=context,
    )

def _build_note(line: str) -> DiagnosticNote:
    parsed = parse_diagnostic_line(line)
    loc = Location(
        file_path=parsed["file_path"],
        line_num=parsed["line_num"],
        col_num=parsed["col_num"],
    )
    return DiagnosticNote(
        location=loc,
        msg_txt=parsed["message"],
    )