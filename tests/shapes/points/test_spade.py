"""Test the spade module."""

import pytest

from .bases import PointsModuleTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.points]


class TestSpade(PointsModuleTestBase):
    """Test the Spade class."""

    shape_name = 'spade'
    distance_test_cases = (
        ((19.97189615, 75.43271708), 0),
        ((23.75, 55), 0),
        ((11.42685318, 59.11304904), 0),
        ((20, 75), 0.2037185),
        ((0, 0), 57.350348),
        ((10, 80), 10.968080),
    )
