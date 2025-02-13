"""Test the vertical_lines module."""

import numpy as np
import pytest

from .bases import ParallelLinesModuleTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.lines]


class TestVerticalLines(ParallelLinesModuleTestBase):
    """Test the VerticalLines class."""

    shape_name = 'v_lines'
    distance_test_cases = (((35, 60), 5.0), ((30, 60), 0.0))
    expected_line_count = 5
    expected_slopes = np.inf
