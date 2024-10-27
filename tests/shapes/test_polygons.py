"""Test polygons module."""

from collections.abc import Iterable
from numbers import Number

import numpy as np
import pytest

pytestmark = [pytest.mark.shapes, pytest.mark.lines, pytest.mark.polygons]


class PolygonsModuleTestBase:
    """Base for testing polygon shapes."""

    shape_name: str
    distance_test_cases: Iterable[tuple[Iterable[Number], float]]
    expected_line_count: int

    @pytest.fixture(scope='class')
    def shape(self, shape_factory):
        """Fixture to get the shape for testing."""
        return shape_factory.generate_shape(self.shape_name)

    @pytest.fixture(scope='class')
    def slopes(self, shape):
        """Fixture to get the slopes of the lines."""
        xs, ys = np.array(shape.lines).T
        runs = np.diff(xs, axis=0)
        rises = np.diff(ys, axis=0)
        slopes = rises / np.ma.masked_array(runs, mask=runs == 0)
        return slopes.filled(np.inf)

    def test_init(self, shape):
        """Test that the shape consists of the correct number of distinct lines."""
        num_unique_lines, *_ = np.unique(shape.lines, axis=0).shape
        assert num_unique_lines == self.expected_line_count

    def test_distance(self, shape, test_point, expected_distance):
        """
        Test the distance() method parametrized by distance_test_cases
        (see conftest.py).
        """
        assert pytest.approx(shape.distance(*test_point)) == expected_distance

    def test_lines_form_polygon(self, shape):
        """Test that the lines form a polygon."""
        endpoints = np.array(shape.lines).reshape(-1, 2)
        assert np.unique(endpoints, axis=0).shape[0] == self.expected_line_count


class TestDiamond(PolygonsModuleTestBase):
    """Test the Diamond class."""

    shape_name = 'diamond'
    distance_test_cases = [[(20, 50), 0.0], [(30, 60), 2.773501]]
    expected_line_count = 4

    def test_slopes(self, slopes):
        """Test that the slopes are as expected."""
        np.testing.assert_array_equal(np.sort(slopes).flatten(), [-1.5, -1.5, 1.5, 1.5])


class TestRectangle(PolygonsModuleTestBase):
    """Test the Rectangle class."""

    shape_name = 'rectangle'
    distance_test_cases = [[(20, 50), 0.0], [(30, 60), 2.0]]
    expected_line_count = 4

    def test_slopes(self, slopes):
        """Test that the slopes are as expected."""
        np.testing.assert_array_equal(np.sort(slopes).flatten(), [0, 0, np.inf, np.inf])


class TestStar(PolygonsModuleTestBase):
    """Test the Star class."""

    shape_name = 'star'
    distance_test_cases = [[(20, 50), 5.856516], [(30, 60), 3.709127]]
    expected_line_count = 10
