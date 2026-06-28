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

class BuildOutput(BaseModel):
    log_txt: str
    diagnostics: list[Diagnostic] = []
    error_count: int
    warning_count: int

