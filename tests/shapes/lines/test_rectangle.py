"""Test the rectangle module."""

import numpy as np
import pytest

from .bases import PolygonsLineModuleTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.lines, pytest.mark.polygons]


class TestRectangle(PolygonsLineModuleTestBase):
    """Test the Rectangle class."""

    shape_name = 'rectangle'
    distance_test_cases = (
        ((12, 60), 0),
        ((28, 60), 0),
        ((20, 50), 0),
        ((20, 74), 0),
        ((20, 75), 1),
        ((30, 80), 6.324555320336759),
    )
    expected_line_count = 4

    def test_slopes(self, slopes):
        """Test that the slopes are as expected."""
        np.testing.assert_array_equal(np.sort(slopes).flatten(), [0, 0, np.inf, np.inf])
