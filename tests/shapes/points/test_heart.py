"""Test the hearts module."""

import pytest

from .bases import PointsModuleTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.points]


class TestHeart(PointsModuleTestBase):
    """Test the Heart class."""

    shape_name = 'heart'
    distance_test_cases = (
        ((22.424114, 59.471779), 0.0),
        ((10.405462, 70.897342), 0.0),
        ((21.064032, 72.065253), 0.0),
        ((16.035166, 60.868470), 0.0),
        ((20, 50), 6.065782511791651),
        ((10, 80), 7.173013322704914),
    )
