
from hypothesis import given, strategies as st
import pytest

from self_storage import parse_rental, duration_average, payable_rent


# =====================================================
# 1. PARSE_RENTAL TESTS
# =====================================================

# 1. Valid rental inputs
@given(
    unit=st.text(min_size=1).filter(lambda x: ':' not in x),
    months=st.floats(
        min_value=0,
        max_value=120,
        allow_nan=False,
        allow_infinity=False
    )
)
def test_parse_rental_valid(unit, months):
    result = parse_rental(f"{unit}:{months}")

    assert result[0] == unit.strip().title()
    assert result[1] == months


# 2. Malformed rental inputs
@given(s=st.text().filter(lambda x: x.count(':') != 1))
def test_parse_rental_invalid(s):
    with pytest.raises(ValueError):
        parse_rental(s)


# 3. Empty unit should be rejected
def test_parse_rental_empty_unit():
    with pytest.raises(ValueError):
        parse_rental(":6")


# 4. Negative rental duration should be rejected
def test_parse_rental_negative_months():
    with pytest.raises(ValueError):
        parse_rental("medium:-2")


# =====================================================
# 2. DURATION_AVERAGE TESTS
# =====================================================

# 5. Valid integer lists
@given(
    values=st.lists(
        st.integers(min_value=0),
        min_size=1,
        max_size=50
    )
)
def test_duration_average_valid(values):
    csv = ','.join(map(str, values))
    expected = sum(values) // len(values)

    assert duration_average(csv) == expected


# 6. Empty input
def test_duration_average_empty():
    with pytest.raises(ValueError):
        duration_average("")


# 7. Large non-negative integers
@given(
    values=st.lists(
        st.integers(min_value=0),
        min_size=1,
        max_size=100
    )
)
def test_duration_average_large_values(values):
    csv = ','.join(map(str, values))

    assert duration_average(csv) == sum(values) // len(values)


# 8. Decimal values should be rejected
@given(
    value=st.floats(
        allow_nan=False,
        allow_infinity=False
    )
)
def test_duration_average_rejects_decimals(value):
    with pytest.raises(ValueError):
        duration_average(str(value))


# 9. Empty entries should be rejected
def test_duration_average_empty_entry():
    with pytest.raises(ValueError):
        duration_average("3,,6")


# 10. Negative rental durations should be rejected
def test_duration_average_negative_values():
    with pytest.raises(ValueError):
        duration_average("3,-6,12")


# =====================================================
# 3. PAYABLE_RENT TESTS
# =====================================================

# 11. Valid rent and discount
@given(
    rent=st.floats(
        min_value=0,
        max_value=100000,
        allow_nan=False,
        allow_infinity=False
    ),
    discount=st.floats(
        min_value=0,
        max_value=100000,
        allow_nan=False,
        allow_infinity=False
    )
)
def test_payable_rent_valid(rent, discount):
    result = payable_rent(f"{rent}|{discount}")
    expected = max(rent * 1.18 - discount, 0)

    assert result == pytest.approx(expected)


# 12. Malformed rent inputs
@given(s=st.text().filter(lambda x: x.count('|') != 1))
def test_payable_rent_invalid(s):
    with pytest.raises(ValueError):
        payable_rent(s)


# 13. Result should never be negative
@given(
    rent=st.floats(
        min_value=0,
        max_value=100000,
        allow_nan=False,
        allow_infinity=False
    ),
    discount=st.floats(
        min_value=0,
        max_value=100000,
        allow_nan=False,
        allow_infinity=False
    )
)
def test_payable_rent_never_negative(rent, discount):
    assert payable_rent(f"{rent}|{discount}") >= 0


# 14. Large discount should make payable amount zero
@given(
    rent=st.floats(
        min_value=0,
        max_value=100000,
        allow_nan=False,
        allow_infinity=False
    )
)
def test_payable_rent_large_discount(rent):
    assert payable_rent(f"{rent}|{rent * 2}") == 0


# 15. Negative rent should be rejected
def test_payable_rent_negative_rent():
    with pytest.raises(ValueError):
        payable_rent("-100|0")


# 16. Negative discount should be rejected
def test_payable_rent_negative_discount():
    with pytest.raises(ValueError):
        payable_rent("100|-20")
