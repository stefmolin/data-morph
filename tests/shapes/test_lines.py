"""Test lines module."""

from numbers import Number
from typing import Iterable, Tuple, Union

import numpy as np
import pytest

pytestmark = [pytest.mark.shapes, pytest.mark.lines]


class LinesModuleTestBase:
    """Base for testing line-based shapes."""

    shape_name: str
    distance_test_cases: Iterable[Tuple[Iterable[Number], float]]
    expected_line_count: int
    expected_slopes: Union[Iterable[Number], Number]

    def _slope(self, start: Iterable[Number], end: Iterable[Number]) -> Number:
        """Calculate the slope of a line given the endpoints."""
        rise = end[1] - start[1]
        run = end[0] - start[0]
        if not run:
            return np.inf
        return rise / run

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
        assert len(shape.lines) == self.expected_line_count

    def test_distance(self, shape):
        """Test the distance() method."""
        for test_point, expected_distance in self.distance_test_cases:
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


class TestHighLines(ParallelLinesModuleTestBase):
    """Test the HighLines class."""

    shape_name = 'high_lines'
    distance_test_cases = [[(20, 50), 6.0], [(30, 60), 4.0]]
    expected_line_count = 2
    expected_slopes = 0


class TestHorizontalLines(ParallelLinesModuleTestBase):
    """Test the HorizontalLines class."""

    shape_name = 'h_lines'
    distance_test_cases = [[(20, 50), 0.0], [(30, 60), 2.5]]
    expected_line_count = 5
    expected_slopes = 0


class TestSlantDownLines(ParallelLinesModuleTestBase):
    """Test the SlantDownLines class."""

    shape_name = 'slant_down'
    distance_test_cases = [[(20, 50), 1.664101], [(30, 60), 0.554700]]
    expected_line_count = 5
    expected_slopes = -1.5


class TestSlantUpLines(ParallelLinesModuleTestBase):
    """Test the SlantUpLines class."""

    shape_name = 'slant_up'
    distance_test_cases = [[(20, 50), 1.664101], [(30, 60), 1.109400]]
    expected_line_count = 5
    expected_slopes = 1.5


class TestVerticalLines(ParallelLinesModuleTestBase):
    """Test the VerticalLines class."""

    shape_name = 'v_lines'
    distance_test_cases = [[(20, 50), 30.0], [(30, 60), 0.0]]
    expected_line_count = 5
    expected_slopes = np.inf


class TestWideLines(ParallelLinesModuleTestBase):
    """Test the WideLines class."""

    shape_name = 'wide_lines'
    distance_test_cases = [[(20, 50), 30.594117], [(30, 60), 4.0]]
    expected_line_count = 2
    expected_slopes = np.inf


class TestXLines(LinesModuleTestBase):
    """Test the XLines class."""

    shape_name = 'x'
    distance_test_cases = [[(20, 50), 8.3205029], [(0, 0), 83.384650]]
    expected_line_count = 2
    expected_slopes = [-1.5, 1.5]

    # TODO need to test that the lines are perpendicular and intersect
