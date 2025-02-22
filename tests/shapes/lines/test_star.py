"""Test the star module."""

import pytest

from .bases import PolygonsLineModuleTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.lines, pytest.mark.polygons]


class TestStar(PolygonsLineModuleTestBase):
    """Test the Star class."""

    shape_name = 'star'
    distance_test_cases = (
        ((8, 68), 0),
        ((17, 68), 0),
        ((20, 77), 0),
        ((23, 68), 0),
        ((32, 68), 0),
        ((24.5, 62), 0),
        ((27.5, 53), 0),
        ((20, 59), 0),
        ((12.5, 53), 0),
        ((15.5, 62), 0),
        ((20, 50), 7.027819284987274),
        ((30, 60), 4.58530260724415),
    )
    expected_line_count = 10
