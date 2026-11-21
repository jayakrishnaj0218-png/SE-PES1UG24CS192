"""Property-based fuzz tests for processor.py.

Run: python -m pytest -v test_processor.py
The tests assert both valid-output properties and safe rejection of invalid data.
"""
import math

import pytest
from hypothesis import given, settings, strategies as st

from processor import calculate_average, normalize_username, parse_int_list


# Function 1: comma-separated integer parser
@given(st.lists(st.integers(), max_size=100))
@settings(max_examples=150)
def test_parse_int_list_round_trip(numbers):
    source = ",".join(str(number) for number in numbers)
    assert parse_int_list(source) == numbers


@given(st.text())
@settings(max_examples=150)
def test_parse_int_list_never_leaks_unexpected_exception(text):
    try:
        result = parse_int_list(text)
    except ValueError:
        # Malformed CSV integers are rejected intentionally.
        return
    assert isinstance(result, list)
    assert all(type(item) is int for item in result)


@given(st.one_of(st.none(), st.integers(), st.floats(allow_nan=True, allow_infinity=True), st.binary()))
def test_parse_int_list_rejects_non_string(value):
    with pytest.raises(TypeError):
        parse_int_list(value)


@given(st.integers())
def test_parse_int_list_single_integer(number):
    assert parse_int_list(str(number)) == [number]


# Function 2: numeric average
@given(st.lists(st.floats(allow_nan=False, allow_infinity=False, width=32), min_size=1, max_size=100))
@settings(max_examples=150)
def test_calculate_average_is_between_min_and_max(numbers):
    result = calculate_average(numbers)
    assert math.isfinite(result)
    assert min(numbers) <= result <= max(numbers)


@given(st.lists(st.integers(), min_size=1, max_size=100))
@settings(max_examples=100)
def test_calculate_average_integer_list(numbers):
    assert calculate_average(numbers) == pytest.approx(sum(numbers) / len(numbers))


@given(st.one_of(st.none(), st.text(), st.binary(), st.integers()))
def test_calculate_average_rejects_non_iterable_or_text(value):
    with pytest.raises(TypeError):
        calculate_average(value)


def test_calculate_average_rejects_empty_collection():
    with pytest.raises(ValueError):
        calculate_average([])


@given(st.sampled_from([float("nan"), float("inf"), float("-inf")]))
def test_calculate_average_rejects_non_finite_numbers(number):
    with pytest.raises(ValueError):
        calculate_average([1, number])


@given(st.lists(st.one_of(st.text(), st.none(), st.booleans()), min_size=1, max_size=10))
def test_calculate_average_rejects_non_numeric_elements(values):
    with pytest.raises(TypeError):
        calculate_average(values)


# Function 3: username normalization
@given(st.from_regex(r"[A-Za-z][A-Za-z0-9_]{2,19}", fullmatch=True))
@settings(max_examples=150)
def test_normalize_username_valid_ascii_username(username):
    assert normalize_username(username) == username.lower()


@given(st.text())
@settings(max_examples=150)
def test_normalize_username_output_is_normalized_or_rejected(username):
    try:
        result = normalize_username(username)
    except ValueError:
        return
    assert result == result.lower()
    assert 3 <= len(result) <= 20
    assert result[0].isalpha()
    assert all(char.isascii() and (char.isalnum() or char == "_") for char in result)


@given(st.one_of(st.none(), st.integers(), st.binary(), st.booleans()))
def test_normalize_username_rejects_non_string(value):
    with pytest.raises(TypeError):
        normalize_username(value)


@given(st.text(min_size=1).filter(lambda value: not value.isascii()))
def test_normalize_username_rejects_unicode(value):
    with pytest.raises(ValueError):
        normalize_username(value)


@pytest.mark.parametrize("username", ["ab", "this_username_is_way_too_long", "1abc", "_abc", "a b", "ab!", ""])
def test_normalize_username_rejects_invalid_boundaries(username):
    with pytest.raises(ValueError):
        normalize_username(username)


def test_normalize_username_trims_outer_whitespace():
    assert normalize_username("  Alice_01  ") == "alice_01"
