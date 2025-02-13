"""Test the star module."""

import pytest

from .bases import PolygonsLineModuleTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.lines, pytest.mark.polygons]


class TestStar(PolygonsLineModuleTestBase):
    """Test the Star class."""

    shape_name = 'star'
    distance_test_cases = (((20, 50), 5.856516), ((30, 60), 3.709127))
    expected_line_count = 10
