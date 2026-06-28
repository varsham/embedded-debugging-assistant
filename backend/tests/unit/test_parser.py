# writing pytest test cases for classify_line

from app.core.parser.gcc import classify_line

# fatal error
def test_fatal_error():
    line = "src/drivers/gpio.c:4:10: fatal error: 'stm32f4xx_hal.h' file not found"
    assert classify_line(line) == "fatal error"

def test_fatal_error_confirm():
    line = "src/drivers/gpio.c:4:10: fatal error: 'GPIOA_MODER' undeclared (first use in this function)"
    assert classify_line(line) == "fatal error"

# error
def test_error():
    line = "src/main.c:14:5: error: 'GPIOA_MODER' undeclared (first use in this function)"
    assert classify_line(line) == "error"

def test_error_other():
    line = "arm-none-eabi-gcc: error: argument to '-mcpu=' is not valid: 'cortex-m45'"
    assert classify_line(line) == "other"

# warning
def test_warning():
    line = "src/startup.c:88:21: warning: initialization makes pointer from integer without a cast [-Wint-conversion]"
    assert classify_line(line) == "warning"

def test_warning_no_cols_nums():
    line = "src/drivers/spi.c:142: warning: array subscript 4 is outside array bounds of 'uint8_t[4]' [-Warray-bounds]"
    assert classify_line(line) == "warning"

# note
def test_note():
    line = "src/interrupts.c:102:5: note: interrupt vector table must be aligned to a 128-byte boundary"
    assert classify_line(line) == "note"

def test_note_log():
    line = "src/drivers/gpio.h:12:25: note: expanded from macro 'SET_PIN'"
    assert classify_line(line) == "note"

def test_stdlib_note():
    line = "/usr/include/newlib/stdlib.h:18: note: expected 'size_t' but argument is of type 'int *'"
    assert classify_line(line) == "note"

# context
def test_context():
    line = "src/drivers/uart.c: In function 'uart_init':"
    assert classify_line(line) == "context"

def test_context_with_digit():
    line = "src/drivers/uart2.c: In function 'uart_init':"
    assert classify_line(line) == "context"

# source
def test_source():
    line = "15 |     GPIOA_MODER &= ~(3 << (5 * 2));"
    assert classify_line(line) == "source"

def test_source_with_caret():
    line = "15 |     GPIOA_MODER ^= ~(3 << (5 * 2));"
    assert classify_line(line) == "source"

def test_source_colon():
    line = "104 |         case UART_STATUS_RX_NE: print_char();"
    assert classify_line(line) == "source"

# caret
def test_caret():
    line = "   |     ~~~~~~~~~~~^"
    assert classify_line(line) == "caret"

def test_multiline_caret():
    line = """
      |            ^~~~
      |            MODER
"""
    assert classify_line(line) == "caret"

def test_caret_tilde():
    line = "   |         ~~~~~~~~~~~~^~~~~~"
    assert classify_line(line) == "caret"

# other
def test_other():
    line = "arm-none-eabi-gcc (GNU Arm Embedded Toolchain 10.3-2021.10) 10.3.1 20210824 (release)"
    assert classify_line(line) == "other"

def test_fatal_error_other():
    line = "arm-none-eabi-gcc: fatal error: cannot read spec file 'nosys.specs': No such file or director"
    assert classify_line(line) == "other"

def test_note_no_location_other():
    line = "arm-none-eabi-gcc: other: valid arguments to '-march=' are: armv6-m armv7-m armv7e-m"
    assert classify_line(line) == "other"

def test_note_other():
    line = "arm-none-eabi-gcc: note: valid arguments to '-march=' are: armv6-m armv7-m armv7e-m"
    assert classify_line(line) == "other"

def test_linker_error():
    line = "/usr/lib/gcc/arm-none-eabi/bin/ld: region `FLASH' overflowed by 4208 bytes"
    assert classify_line(line) == "other"

def test_empty_context_line():
    line = "   |"
    assert classify_line(line) == "other"