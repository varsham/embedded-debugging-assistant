from app.models.diagnostic import DiagnosticType
from app.models.explanation import Explanation


KNOWLEDGE_BASE: dict[DiagnosticType, Explanation] = {
    DiagnosticType.UNDEFINED_REF: Explanation(
        error_summary="Could not find a definition for a referenced symbol.",
        what_happened=(
            "Your code uses a function, variable, or other symbol that the "
            "program cannot find a definition for."
        ),
        common_causes=[
            "The function or variable was never created.",
            "The name was misspelled or does not match the definition.",
            "The file containing the definition was not included when building the program.",
        ],
        how_to_fix=(
            "Check that the symbol is defined, that its name matches where it is "
            "used, and that all required files are included when building your program."
        ),
    ),

    DiagnosticType.OVERFLOW: Explanation(
        error_summary="A value exceeded the space available to store it.",
        what_happened=(
            "Your program tried to store a value that is larger than the allowed "
            "range for its data type or memory region."
        ),
        common_causes=[
            "A number is larger than the variable type can hold.",
            "A memory region or storage area is too small.",
            "A calculation produced a value outside the expected range.",
        ],
        how_to_fix=(
            "Check your variable types, memory sizes, and calculations to make sure "
            "values stay within the allowed range."
        ),
    ),

    DiagnosticType.IMPLICIT_DEC: Explanation(
        error_summary="A function was used before it was declared.",
        what_happened=(
            "Your program called a function that the compiler does not know about yet."
        ),
        common_causes=[
            "The required header file was not included.",
            "The function name was misspelled.",
            "The function was declared or defined after it was used.",
        ],
        how_to_fix=(
            "Add the correct declaration or include file, check the function name, "
            "or define the function before using it."
        ),
    ),

    DiagnosticType.UNUSED_VAR: Explanation(
        error_summary="A variable was created but never used.",
        what_happened=(
            "Your program creates a variable and stores a value in it, but the "
            "value is never read or needed."
        ),
        common_causes=[
            "The variable was left behind from an earlier version of the code.",
            "A typo or logic mistake caused the variable to never be used.",
            "The variable was created but the code using it was never added.",
        ],
        how_to_fix=(
            "Remove the variable if it is unnecessary, or use it in the part of "
            "the program where it is needed."
        ),
    ),

    DiagnosticType.UNKNOWN: Explanation(
        error_summary="We found a problem, but we could not identify its cause yet.",
        what_happened=(
            "The debugger recognized an issue but does not have enough information "
            "to classify it."
        ),
        common_causes=[
            "The error type is not currently supported by the debugger.",
            "The compiler message uses unfamiliar wording.",
            "Additional context is needed to understand the problem.",
        ],
        how_to_fix=(
            "Review the highlighted code, check recent changes, and look at the "
            "original compiler message for more details."
        ),
    ),
}

def lookup(diagnostic_type: DiagnosticType) -> Explanation:
    return KNOWLEDGE_BASE.get(
        diagnostic_type,
        KNOWLEDGE_BASE[DiagnosticType.UNKNOWN],
    )