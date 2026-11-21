"""Input processing utilities for Lab 7 fuzz-testing exercise.

The functions accept untrusted input and reject invalid values with documented,
consistent exceptions rather than leaking incidental TypeError/ValueError errors.
"""
from __future__ import annotations

import math
from typing import Any, List


def parse_int_list(value: Any) -> List[int]:
    """Parse a comma-separated string into integers.

    Surrounding whitespace is accepted. Empty input maps to an empty list.
    Empty elements, non-integers, and non-string input are rejected.
    """
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    if value.strip() == "":
        return []
    parts = value.split(",")
    parsed: List[int] = []
    for index, part in enumerate(parts):
        item = part.strip()
        if item == "":
            raise ValueError(f"empty integer at position {index}")
        try:
            parsed.append(int(item))
        except ValueError as exc:
            raise ValueError(f"invalid integer at position {index}: {item!r}") from exc
    return parsed


def calculate_average(values: Any) -> float:
    """Return the arithmetic mean of a non-empty iterable of finite numbers."""
    if isinstance(values, (str, bytes, bytearray)):
        raise TypeError("values must be an iterable of numbers, not text")
    try:
        items = list(values)
    except (TypeError, ValueError) as exc:
        raise TypeError("values must be an iterable of numbers") from exc
    if not items:
        raise ValueError("at least one value is required")

    numbers = []
    for index, item in enumerate(items):
        if isinstance(item, bool) or not isinstance(item, (int, float)):
            raise TypeError(f"value at position {index} must be numeric")
        try:
            number = float(item)
        except OverflowError as exc:
            raise ValueError(f"value at position {index} is outside the supported numeric range") from exc
        if not math.isfinite(number):
            raise ValueError(f"value at position {index} must be finite")
        numbers.append(number)
    # Divide before summing to reduce overflow risk for large finite values.
    try:
        return math.fsum(number / len(numbers) for number in numbers)
    except OverflowError as exc:
        raise ValueError("average is outside the supported numeric range") from exc


def normalize_username(value: Any) -> str:
    """Validate and normalize a username (3-20 ASCII letters/digits/underscores)."""
    if not isinstance(value, str):
        raise TypeError("username must be a string")
    normalized = value.strip()
    if not 3 <= len(normalized) <= 20:
        raise ValueError("username must contain between 3 and 20 characters")
    if not normalized.isascii():
        raise ValueError("username must contain ASCII characters only")
    if not all(char.isalnum() or char == "_" for char in normalized):
        raise ValueError("username may contain only letters, digits, and underscores")
    if not normalized[0].isalpha():
        raise ValueError("username must start with a letter")
    return normalized.lower()


def main() -> None:
    """Run a small demonstration of all three utilities."""
    print("LAB 7 — INPUT VALIDATION PROCESSOR")
    print("-" * 42)
    print("Parsed integers:", parse_int_list("10, 20, -3, 40"))
    print("Average:", calculate_average([10, 20, 30, 40]))
    print("Normalized username:", normalize_username("  Jay_2026  "))
    print("\nInvalid-input demonstrations:")
    examples = [
        ("parse_int_list", lambda: parse_int_list("1,,3")),
        ("calculate_average", lambda: calculate_average([])),
        ("normalize_username", lambda: normalize_username("ab!")),
    ]
    for name, operation in examples:
        try:
            operation()
        except (TypeError, ValueError) as exc:
            print(f"{name}: safely rejected ({type(exc).__name__}: {exc})")


if __name__ == "__main__":
    main()
