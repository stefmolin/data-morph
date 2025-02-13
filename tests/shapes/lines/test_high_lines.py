"""Test the high_lines module."""

import pytest

from .bases import ParallelLinesModuleTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.lines]


class TestHighLines(ParallelLinesModuleTestBase):
    """Test the HighLines class."""

    shape_name = 'high_lines'
    distance_test_cases = (((20, 50), 6.0), ((30, 60), 4.0))
    expected_line_count = 2
    expected_slopes = 0
