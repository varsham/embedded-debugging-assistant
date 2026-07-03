from app.core.parser.linker import classify_linker_line, parse_undefined_ref_line, parse_overflow_line

def test_ld_context():
    line = "ld: main.o: in function 'main':"
    assert classify_linker_line(line) == "ld_context"

def test_ld_context_different_object():
    line = "ld: utils.o: in function 'helper':"
    assert classify_linker_line(line) == "ld_context"

def test_ld_context_with_path():
    line = "ld: build/main.o: in function 'main':"
    assert classify_linker_line(line) == "ld_context"

def test_undefined_ref():
    line = "main.c:(.text+0x14): undefined reference to `printf'" 
    assert classify_linker_line(line) == "undefined_ref"

def test_undefined_ref_cpp_symbol():
    line = "foo.o:(.text+0x20): undefined reference to `std::cout'"
    assert classify_linker_line(line) == "undefined_ref"

def test_undefined_ref_global_symbol():
    line = "main.o:(.text+0x8): undefined reference to `global_var'"
    assert classify_linker_line(line) == "undefined_ref"

def test_overflow():
    line = "ld: region `FLASH' overflowed by 128 bytes"  
    assert classify_linker_line(line) == "overflow"

def test_overflow_ram():
    line = "ld: region `RAM' overflowed by 64 bytes"
    assert classify_linker_line(line) == "overflow"

def test_overflow_large_value():
    line = "ld: region `FLASH' overflowed by 4096 bytes"
    assert classify_linker_line(line) == "overflow"

def test_other():
    line = "gcc -c main.c -o main.o"
    assert classify_linker_line(line) == "other"

def test_other_empty():
    line = ""
    assert classify_linker_line(line) == "other"

def test_other_blank():
    line = "   "
    assert classify_linker_line(line) == "other"

def test_other_compiler_warning():
    line = "warning: unused variable 'x'"
    assert classify_linker_line(line) == "other"

def test_other_link_success():
    line = "Linking C executable app"
    assert classify_linker_line(line) == "other"


def test_parse_undefined_ref_line():
    line = "main.c:42: undefined reference to 'printf'"
    assert parse_undefined_ref_line(line) == {
        "file_path": "main.c",
        "line_num": 42,
        "symbol": "printf",
    }

def test_parse_undefined_ref_line_with_path():
    line = "src/main.c:105: undefined reference to 'malloc'"
    assert parse_undefined_ref_line(line) == {
        "file_path": "src/main.c",
        "line_num": 105,
        "symbol": "malloc",
    }

def test_parse_undefined_ref_line_invalid():
    line = "main.c:42: error: something else"
    assert parse_undefined_ref_line(line) is None

def test_parse_undefined_ref_line_missing_line_number():
    line = "main.c: undefined reference to 'printf'"
    assert parse_undefined_ref_line(line) is None

def test_parse_overflow_line():
    line = "ld: region `FLASH' overflowed by 128 bytes"
    assert parse_overflow_line(line) == {
        "region": "FLASH",
        "overflowed_bytes": 128,
    }

def test_parse_overflow_line_ram():
    line = "ld: region `RAM' overflowed by 64 bytes"
    assert parse_overflow_line(line) == {
        "region": "RAM",
        "overflowed_bytes": 64,
    }

def test_parse_overflow_line_without_prefix():
    line = "region `FLASH' overflowed by 4096 bytes"
    assert parse_overflow_line(line) == {
        "region": "FLASH",
        "overflowed_bytes": 4096,
    }

def test_parse_overflow_line_invalid():
    line = "ld: region `FLASH' is full"
    assert parse_overflow_line(line) is None

def test_parse_overflow_line_missing_bytes():
    line = "ld: region `FLASH' overflowed by bytes"
    assert parse_overflow_line(line) is None