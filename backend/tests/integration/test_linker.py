from pathlib import Path
from app.core.parser.linker import parse_linker_output    

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
FIXTURES = _PROJECT_ROOT / "examples" / "build_logs"

def test_parse_mixed_log():
    log = (FIXTURES / "linker_mixed.txt").read_text()
    result = parse_linker_output(log)

    assert len(result) == 4
    assert result[0].kind == "undefined_ref"
    assert result[0].symbol == "gpio_init"
    assert result[0].file_path == "src/main.c"
    assert result[0].line_num == 42
    
    assert result[1].kind == "undefined_ref"
    assert result[1].symbol == "uart_send"
    assert result[1].file_path == "src/main.c"
    assert result[1].line_num == 51

    assert result[2].kind == "undefined_ref"
    assert result[2].symbol == "clock_enable"
    assert result[2].file_path == "src/uart.c"
    assert result[2].line_num == 17

    assert result[3].kind == "overflow"
    assert result[3].region == "FLASH"
    assert result[3].bytes_overflowed == 4208