import pytest

from self_storage import access_allowed, payment_status, rent_due


@pytest.mark.parametrize(
    "unit_size, months, climate, member, expected",
    [
        ("small", 1, False, False, 0),       # no extra months
        ("small", 3, False, False, 160),     # non-climate, short extra period
        ("small", 3, True, False, 240),      # climate, short extra period
        ("small", 9, False, False, 560),     # non-climate, extra > 6
        ("small", 9, True, False, 840),      # climate, extra > 6
        ("small", 3, False, True, 80),       # member gets one extra covered month
        ("medium", 4, False, True, 80),      # member, non-large unit
        ("large", 5, False, True, 160),      # large members get no extra coverage
    ],
)
def test_rent_due_all_valid_branches(unit_size, months, climate, member, expected):
    assert rent_due(unit_size, months, climate, member) == expected


@pytest.mark.parametrize(
    "unit_size, months, message",
    [
        ("unknown", 2, "unknown unit size"),
        ("small", -1, "invalid months"),
    ],
)
def test_rent_due_invalid_inputs(unit_size, months, message):
    with pytest.raises(ValueError, match=message):
        rent_due(unit_size, months, False, False)


@pytest.mark.parametrize(
    "hour, visitors, owner, expected",
    [
        (12, 4, True, True),    # owner within limit
        (12, 5, True, False),   # owner over limit
        (5, 1, False, False),   # before access hours
        (23, 1, False, False),  # after access hours
        (6, 2, False, True),    # lower boundary, within visitor limit
        (22, 2, False, True),   # upper boundary, within visitor limit
        (12, 3, False, False),  # non-owner over visitor limit
    ],
)
def test_access_allowed_all_branches(hour, visitors, owner, expected):
    assert access_allowed(hour, visitors, owner) is expected


@pytest.mark.parametrize(
    "days, autopay, prior_late, expected",
    [
        (0, True, False, "current"),       # autopay cutoff 0
        (-1, True, False, "grace"),
        (-16, True, False, "lien"),
        (5, False, False, "current"),      # manual-pay cutoff 5
        (-10, False, False, "grace"),
        (-11, False, False, "lien"),
        (15, True, True, "current"),       # prior late adds 10
        (0, False, True, "grace"),
        (-6, False, True, "lien"),
    ],
)
def test_payment_status_all_branches(days, autopay, prior_late, expected):
    assert payment_status(days, autopay, prior_late) == expected
