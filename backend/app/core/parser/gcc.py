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