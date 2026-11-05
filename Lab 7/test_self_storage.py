from hypothesis import given, strategies as st
import pytest

from self_storage import parse_rental, duration_average, payable_rent


# 1. parse_rental: valid rental inputs
@given(
    unit=st.text(min_size=1).filter(lambda x: ':' not in x),
    months=st.floats(min_value=0, max_value=120, allow_nan=False, allow_infinity=False)
)
def test_parse_rental_valid(unit, months):
    result = parse_rental(f"{unit}:{months}")
    assert result[0] == unit.strip().title()
    assert result[1] == months


# 2. parse_rental: malformed inputs
@given(s=st.text().filter(lambda x: x.count(':') != 1))
def test_parse_rental_invalid(s):
    with pytest.raises(ValueError):
        parse_rental(s)


# 3. duration_average: valid integer lists
@given(values=st.lists(st.integers(), min_size=1, max_size=50))
def test_duration_average_valid(values):
    csv = ','.join(map(str, values))
    expected = sum(values) // len(values)
    assert duration_average(csv) == expected


# 4. duration_average: empty input
def test_duration_average_empty():
    with pytest.raises(ValueError):
        duration_average("")


# 5. payable_rent: valid rent and discount
@given(
    rent=st.floats(min_value=0, max_value=100000, allow_nan=False, allow_infinity=False),
    discount=st.floats(min_value=0, max_value=100000, allow_nan=False, allow_infinity=False)
)
def test_payable_rent_valid(rent, discount):
    result = payable_rent(f"{rent}|{discount}")
    expected = max(rent * 1.18 - discount, 0)
    assert result == pytest.approx(expected)


# 6. payable_rent: malformed inputs
@given(s=st.text().filter(lambda x: x.count('|') != 1))
def test_payable_rent_invalid(s):
    with pytest.raises(ValueError):
        payable_rent(s)


# 7. duration_average: negative and large integers
@given(values=st.lists(st.integers(), min_size=1, max_size=100))
def test_duration_average_negative_and_large(values):
    csv = ','.join(map(str, values))
    assert duration_average(csv) == sum(values) // len(values)


# 8. duration_average: decimal values are rejected
@given(value=st.floats(allow_nan=False, allow_infinity=False))
def test_duration_average_rejects_decimals(value):
    with pytest.raises(ValueError):
        duration_average(str(value))


# 9. payable_rent: result cannot be negative
@given(
    rent=st.floats(min_value=0, max_value=100000, allow_nan=False, allow_infinity=False),
    discount=st.floats(min_value=0, max_value=100000, allow_nan=False, allow_infinity=False)
)
def test_payable_rent_never_negative(rent, discount):
    assert payable_rent(f"{rent}|{discount}") >= 0


# 10. payable_rent: large discount makes payable amount zero
@given(rent=st.floats(min_value=0, max_value=100000, allow_nan=False, allow_infinity=False))
def test_payable_rent_large_discount(rent):
    assert payable_rent(f"{rent}|{rent * 2}") == 0
