"""Test the slant_down module."""

import pytest

from .bases import ParallelLinesModuleTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.lines]


class TestSlantDownLines(ParallelLinesModuleTestBase):
    """Test the SlantDownLines class."""

    shape_name = 'slant_down'
    distance_test_cases = (((20, 50), 1.664101), ((30, 60), 0.554700))
    expected_line_count = 5
    expected_slopes = -1.5
