import re
from app.models.diagnostic import LinkerError, LinkerErrorKind

def classify_linker_line(line: str) -> str:
    if re.search(r"ld:.*in function", line):
        return "ld_context"
    elif re.search(r"undefined reference to", line):
        return "undefined_ref"
    elif re.search(r"ld:.*overflowed by", line):
        return "overflow"
    else:
        return "other"

def parse_undefined_ref_line(line: str) -> dict | None:
    pattern = (
        r"^(?P<file_path>[^:]+):"
        r"(?P<line_num>\d+):"
        r"\s*undefined reference to '(?P<symbol>[^']+)'"
    )
    match = re.match(pattern, line)
    if match is None:
        return None
    return {
        "file_path": match.group("file_path"),
        "line_num": int(match.group("line_num")),
        "symbol": match.group("symbol"),
    }

def parse_overflow_line(line: str) -> dict | None:
    pattern = (
        r"^.*?region `(?P<region>[^']+)'\s*"
        r"overflowed by (?P<overflowed_bytes>\d+)\s*bytes"
    )
    match = re.match(pattern, line)
    if match is None:
        return None
    return {
        "region": match.group("region"),
        "overflowed_bytes": int(match.group("overflowed_bytes")),
    }

def parse_linker_output(log: str) -> list[LinkerError]:
    lines = log.splitlines()

    state = "IDLE"
    current_object_file: str | None = None
    current_function_context: str | None = None
    linker_errors: list[LinkerError] = []

    for line in lines:
        line_type = classify_linker_line(line)

        if state == "IDLE":
            if line_type == "overflow":
                linker_errors.append(_build_overflow(line, current_object_file, current_function_context))
            elif line_type == "ld_context":
                result = _parse_context_line(line)
                if result:
                    current_function_context, current_object_file = result
                state = "IN_CONTEXT"

        elif state == "IN_CONTEXT":
            if line_type == "undefined_ref":
                linker_errors.append(_build_undefined_ref(line, current_object_file, current_function_context))
            elif line_type == "ld_context":
                result = _parse_context_line(line)
                if result:
                    current_function_context, current_object_file = result
            else:
                state = "IDLE"

    return linker_errors

def _build_undefined_ref(line: str, object_file: str | None, function_context: str | None) -> LinkerError:
    parsed = parse_undefined_ref_line(line)
    return LinkerError(
        kind=LinkerErrorKind.UNDEFINED_REF,
        file_path=parsed["file_path"],
        line_num=parsed["line_num"],
        symbol=parsed["symbol"],
        function_context=function_context,
        object_file=object_file,
    )

def _build_overflow(line: str, object_file: str | None, function_context: str | None) -> LinkerError:
    parsed = parse_overflow_line(line)
    return LinkerError(
        kind=LinkerErrorKind.OVERFLOW,
        region=parsed["region"],
        bytes_overflowed=parsed["overflowed_bytes"],
        function_context=function_context,
        object_file=object_file,
    )

def _parse_context_line(line: str) -> tuple[str, str] | None:
    match = re.search(
        r"ld:\s+(?P<object_file>[^:]+):\s+in function '(?P<function_context>[^']+)'",
        line,
    )
    if match:
        return (match.group("function_context"), match.group("object_file"))
    return None