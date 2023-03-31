"""Test polygons module."""

from numbers import Number
from typing import Iterable, Tuple

import numpy as np
import pytest

pytestmark = [pytest.mark.shapes, pytest.mark.lines, pytest.mark.polygons]


class PolygonsModuleTestBase:
    """Base for testing polygon shapes."""

    shape_name: str
    distance_test_cases: Iterable[Tuple[Iterable[Number], float]]
    expected_line_count: int

    @pytest.fixture(scope='class')
    def shape(self, shape_factory):
        """Fixture to get the shape for testing."""
        return shape_factory.generate_shape(self.shape_name)

    def test_init(self, shape):
        """Test that the shape consists of the correct number of distinct lines."""
        num_unique_lines, *_ = np.unique(shape.lines, axis=0).shape
        assert num_unique_lines == self.expected_line_count

    def test_distance(self, shape):
        """Test the distance() method."""
        for test_point, expected_distance in self.distance_test_cases:
            assert pytest.approx(shape.distance(*test_point)) == expected_distance

    def test_lines_form_polygon(self, shape):
        """Test that the lines form a polygon."""
        endpoints = np.array(shape.lines).reshape(-1, 2)
        assert np.unique(endpoints, axis=0).shape[0] == self.expected_line_count


class TestRectangle(PolygonsModuleTestBase):
    """Test the Rectangle class."""

    shape_name = 'rectangle'
    distance_test_cases = [[(20, 50), 0.0], [(30, 60), 2.0]]
    expected_line_count = 4


class TestStar(PolygonsModuleTestBase):
    """Test the Star class."""

    shape_name = 'star'
    distance_test_cases = [[(20, 50), 5.856516], [(30, 60), 3.709127]]
    expected_line_count = 10
