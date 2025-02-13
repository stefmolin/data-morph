"""Test the horizontal_lines module."""

import pytest

from .bases import ParallelLinesModuleTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.lines]


class TestHorizontalLines(ParallelLinesModuleTestBase):
    """Test the HorizontalLines class."""

    shape_name = 'h_lines'
    distance_test_cases = (((20, 50), 0.0), ((30, 60), 2.5))
    expected_line_count = 5
    expected_slopes = 0
