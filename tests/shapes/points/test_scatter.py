"""Test the scatter module."""

import pytest

from .bases import PointsModuleTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.points]


class TestScatter(PointsModuleTestBase):
    """Test the Scatter class."""

    shape_name = 'scatter'
    distance_test_cases = (((20, 50), 0.0), ((30, 60), 0.0), ((-500, -150), 0.0))
