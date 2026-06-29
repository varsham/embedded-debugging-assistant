import re

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