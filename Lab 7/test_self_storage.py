from hypothesis import given, strategies as st
from self_storage import parse_rental, duration_average, payable_rent

@given(st.text() | st.none())
def test_parse_rental_no_crash(s):

@given(st.text() | st.none())
def test_duration_average_no_crash(s):

@given(st.text() | st.none())
def test_payable_rent_no_crash(s):
