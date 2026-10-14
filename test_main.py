import pytest
from main import calculate_grade


@pytest.mark.parametrize(
    "percentage, expected",
    [
        (95, "A+"),
        (85, "A"),
        (75, "B"),
        (65, "C"),
        (55, "D"),
        (40, "F"),
        (90, "A+"),
        (0, "F"),
    ],
)
def test_calculate_grade(percentage, expected):
    assert calculate_grade(percentage) == expected