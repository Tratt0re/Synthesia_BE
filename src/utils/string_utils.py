def safe_concat_strings(*strings: str | None) -> str:
    """
    Concatenates an arbitrary number of strings, ensuring None values are ignored.

    Args:
        *strings: Arbitrary number of string arguments that may include None.

    Returns:
        A single concatenated string with None values treated as empty strings.
    """
    return " ".join(s for s in strings if s)
