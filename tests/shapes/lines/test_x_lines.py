"""Test the x_lines module."""

import numpy as np
import pytest

from .bases import LinesModuleTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.lines]


class TestXLines(LinesModuleTestBase):
    """Test the XLines class."""

    shape_name = 'x'
    distance_test_cases = (
        ((8, 83), 0),  # edge of X line
        ((20, 65), 0),  # middle of X (intersection point)
        ((19, 64), 0.277350),  # off the X
        ((10, 20), 27.073973),  # off the X
    )
    expected_line_count = 2
    expected_slopes = (-1.5, 1.5)

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
