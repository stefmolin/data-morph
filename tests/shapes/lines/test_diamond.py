"""Test the diamond module."""

import numpy as np
import pytest

from .bases import PolygonsLineModuleTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.lines, pytest.mark.polygons]


class TestDiamond(PolygonsLineModuleTestBase):
    """Test the Diamond class."""

    shape_name = 'diamond'
    distance_test_cases = (
        ((20, 50), 0),
        ((20, 77), 0),
        ((11, 63.5), 0),
        ((29, 63.5), 0),
        ((30, 63.5), 1),
        ((30, 60), 2.773501),
    )
    expected_line_count = 4

    def test_slopes(self, slopes):
        """Test that the slopes are as expected."""
        np.testing.assert_array_equal(np.sort(slopes).flatten(), [-1.5, -1.5, 1.5, 1.5])
