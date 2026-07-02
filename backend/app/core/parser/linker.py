import re

def classify_linker_line(line: str) -> str:
    if re.search(r"ld:.*in function", line):
        return "ld_context"
    elif re.search("undefined reference to", line):
        return "undefined_ref"
    elif re.search(r"ld:.*overflowed by", line):
        return "overflow"
    else:
        return "other"

def parse_undefined_ref_line(line: str) -> dict | None:
    pattern = (
        r"^(?P<file_path>[^:]+):"  # 1. File path
        r"(?P<line_num>\d+):" # 2. Line number
        r"\s*undefined reference to '(?P<symbol>[^']+)'" # 3. Symbol
    )

    match = re.match(pattern, line)

    if match is None:
        return None
    return {
        "file_path": match.group('file_path'),
        "line_num": int(match.group('line_num')),
        "symbol": match.group('symbol')
    }

def parse_overflow_line(line: str) -> dict | None:
    pattern = (
        r"^.*?region `(?P<region>[^']+)'\s*" # 1. Region
        r"overflowed by (?P<overflowed_bytes>\d+)\s*bytes" # 2. number of overflowed bytes
    )

    match = re.match(pattern, line)

    if match is None:
        return None
    return {
        "region": match.group('region'),
        "overflowed_bytes": int(match.group('overflowed_bytes'))
    }