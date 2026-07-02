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