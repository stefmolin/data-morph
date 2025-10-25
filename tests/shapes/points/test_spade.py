"""Test the spade module."""

import pytest

from .bases import PointsModuleTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.points]


class TestSpade(PointsModuleTestBase):
    """Test the Spade class."""

    shape_name = 'spade'
    distance_test_cases = (
        ((19.818701, 60.065370), 0),
        ((23.750000, 55.532859), 0),
        ((20.067229, 60.463689), 0),
        ((18.935968, 58.467606), 0),
        ((20, 75), 0.5335993101603015),
        ((0, 0), 57.861566654807596),
        ((10, 80), 11.404000978114487),
    )
