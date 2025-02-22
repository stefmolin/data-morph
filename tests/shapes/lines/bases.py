"""Base test classes for line shapes."""

from __future__ import annotations

from numbers import Number

import numpy as np
import pytest


class LinesModuleTestBase:
    """Base for testing line-based shapes."""

    shape_name: str
    distance_test_cases: tuple[tuple[tuple[Number], float]]
    expected_line_count: int
    expected_slopes: tuple[Number] | Number

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

    def test_slopes(self, slopes):
        """Test that the slopes are as expected."""
        expected = (
            [self.expected_slopes]
            if isinstance(self.expected_slopes, Number)
            else self.expected_slopes
        )
        assert np.array_equal(np.unique(slopes), expected)


class ParallelLinesModuleTestBase(LinesModuleTestBase):
    """Base for testing parallel line-based shapes."""

    def test_lines_are_parallel(self, slopes):
        """Test that the lines are parallel (slopes are equal)."""
        assert np.unique(slopes).size == 1


class PolygonsLineModuleTestBase:
    """Base for testing polygon shapes."""

    shape_name: str
    distance_test_cases: tuple[tuple[tuple[Number], float]]
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
        actual_distance = shape.distance(*test_point)
        assert pytest.approx(actual_distance) == expected_distance

    def test_lines_form_polygon(self, shape):
        """Test that the lines form a polygon."""
        endpoints = np.array(shape.lines).reshape(-1, 2)
        assert np.unique(endpoints, axis=0).shape[0] == self.expected_line_count
