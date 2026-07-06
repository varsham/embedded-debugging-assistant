from pydantic import BaseModel
from typing import Optional
from enum import Enum

class Location(BaseModel):
    file_path: str
    line_num: int
    col_num: Optional[int] = None # not always present in all diagnostic types

class DiagnosticNote(BaseModel):
    location: Location
    msg_txt: str
    source_line: Optional[str] = None
    caret_line: Optional[str] = None

class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    NOTE = "note"
    FATAL_ERROR = "fatal error"

class Diagnostic(BaseModel):
    location: Location
    severity: Severity
    msg_txt: str
    gcc_flag: Optional[str] = None
    function_context: Optional[str] = None
    source_excerpt: Optional[str] = None
    caret_line: Optional[str] = None
    notes: list[DiagnosticNote] = []

class LinkerErrorKind(str, Enum):
    OVERFLOW = "overflow"
    UNDEFINED_REF = "undefined_ref"

class LinkerError(BaseModel):
    kind: LinkerErrorKind
    # for undefined_ref
    file_path: Optional[str] = None
    line_num: Optional[int] = None
    symbol: Optional[str] = None
    object_file: Optional[str] = None
    function_context: Optional[str] = None
    # for overflow
    region: Optional[str] = None
    bytes_overflowed: Optional[int] = None

class BuildOutput(BaseModel):
    log_txt: str
    diagnostics: list[Diagnostic] = []
    linker_errors: list[LinkerError] = []
    error_count: int
    warning_count: int

class DiagnosticType(str, Enum):
    UNDEFINED_REF = "undefined_reference"
    OVERFLOW = "overflow"
    IMPLICIT_DEC = "implicit_declaration"
    UNUSED_VAR = "unused_variable"
    UNKNOWN = "unknown"

    