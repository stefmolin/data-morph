"""Test the hearts module."""

import pytest

from .bases import PointsModuleTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.points]


class TestHeart(PointsModuleTestBase):
    """Test the Heart class."""

    shape_name = 'heart'
    distance_test_cases = (
        ((19.89946048, 54.82281916), 0.0),
        ((10.84680454, 70.18556376), 0.0),
        ((29.9971295, 67.66402445), 0.0),
        ((27.38657942, 62.417184), 0.0),
        ((20, 50), 4.567369),
        ((10, 80), 8.564365),
    )
