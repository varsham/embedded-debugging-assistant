from pathlib import Path
from app.core.parser.gcc import parse_gcc_output      

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
FIXTURES = _PROJECT_ROOT / "examples" / "build_logs"

def test_parse_mixed_log():
    log = (FIXTURES / "gcc_mixed.txt").read_text()
    result = parse_gcc_output(log)

    assert result.error_count == 1
    assert result.warning_count == 1
    assert len(result.diagnostics) == 2

    error = result.diagnostics[0]
    assert error.msg_txt == "implicit declaration of function 'gpio_init'"
    assert error.severity == "error"
    assert error.location.line_num == 42
    assert error.function_context == "In function 'main'"
    assert error.gcc_flag == "-Wimplicit-function-declaration"
    assert len(error.notes) == 2
    assert error.notes[0].msg_txt == "did you mean 'gpio_deinit'?"
    assert error.notes[0].location.file_path == "src/main.c"

    warning = result.diagnostics[1]
    assert warning.msg_txt == "unused variable 'status'"
    assert warning.severity == "warning"
    assert warning.location.line_num == 67
    assert warning.function_context == "In function 'main'"
    assert warning.gcc_flag == "-Wunused-variable"
    assert len(warning.notes) == 0

