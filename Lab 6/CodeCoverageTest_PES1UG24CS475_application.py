import pytest

from self_storage import access_allowed, payment_status, rent_due


@pytest.mark.parametrize(
    "unit_size, months, climate, member, expected",
    [
        ("small", 1, False, False, 0),
        ("small", 4, False, True, 160),
        ("medium", 5, True, False, 360),
        ("large", 10, False, True, 490),
        ("small", 9, True, False, 840),  # climate rate reduction when extra > 6
    ],
)
def test_rent_due_valid_cases(unit_size, months, climate, member, expected):
    assert rent_due(unit_size, months, climate, member) == expected


@pytest.mark.parametrize(
    "unit_size, months, message",
    [
        ("extra-large", 3, "unknown unit size"),
        ("small", -1, "invalid months"),
    ],
)
def test_rent_due_validation(unit_size, months, message):
    with pytest.raises(ValueError, match=message):
        rent_due(unit_size, months, False, False)


@pytest.mark.parametrize(
    "hour, visitors, owner, expected",
    [
        (12, 1, False, True),
        (23, 1, False, False),
        (12, 3, False, False),
        (12, 5, True, False),
    ],
)
def test_access_allowed_cases(hour, visitors, owner, expected):
    assert access_allowed(hour, visitors, owner) is expected


@pytest.mark.parametrize(
    "days, autopay, prior_late, expected",
    [
        (0, True, False, "current"),
        (-10, False, False, "grace"),
        (-11, False, False, "lien"),
        (5, False, True, "grace"),
    ],
)
def test_payment_status_cases(days, autopay, prior_late, expected):
    assert payment_status(days, autopay, prior_late) == expected
