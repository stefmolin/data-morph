"""Test the wide_lines module."""

import numpy as np
import pytest

from .bases import ParallelLinesModuleTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.lines]


class TestWideLines(ParallelLinesModuleTestBase):
    """Test the WideLines class."""

    shape_name = 'wide_lines'
    distance_test_cases = (((26, 50), 0), ((30, 60), 4.0))
    expected_line_count = 2
    expected_slopes = np.inf
