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
    distance_test_cases = [[(35, 60), 5.0], [(30, 60), 0.0]]
    expected_line_count = 5
    expected_slopes = np.inf


class TestWideLines(ParallelLinesModuleTestBase):
    """Test the WideLines class."""

    shape_name = 'wide_lines'
    distance_test_cases = [[(26, 50), 0], [(30, 60), 4.0]]
    expected_line_count = 2
    expected_slopes = np.inf


class TestXLines(LinesModuleTestBase):
    """Test the XLines class."""

    shape_name = 'x'
    distance_test_cases = [
        [(8, 83), 0],  # edge of X line
        [(20, 65), 0],  # middle of X (intersection point)
        [(19, 64), 0.277350],  # off the X
        [(10, 20), 27.073973],  # off the X
    ]
    expected_line_count = 2
    expected_slopes = [-1.5, 1.5]

    def test_lines_form_an_x(self, shape):
        """Test that the lines form an X."""
        lines = np.array(shape.lines)

        # check perpendicular
        xs, ys = lines.T
        runs = np.diff(xs, axis=0)
        rises = np.diff(ys, axis=0)
        assert np.dot(rises, runs.T) == 0

        # check that the lines intersect in the middle
        midpoints = np.mean(lines.T, axis=1)[0].T
        assert np.unique(midpoints).size == 1
