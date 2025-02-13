"""Test the circle module."""

import numpy as np
import pytest

from .bases import CIRCLE_REPR, CirclesModuleTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.circles]


class TestCircle(CirclesModuleTestBase):
    """Test the Circle class."""

    shape_name = 'circle'
    distance_test_cases = (((20, 50), 10.490381), ((10, 25), 15.910168))
    repr_regex = '^' + CIRCLE_REPR + '$'

    def test_is_circle(self, shape):
        """Test that the Circle is a valid circle (mathematically)."""
        angles = np.arange(0, 361, 45)
        cx, cy = shape.center
        for x, y in zip(
            cx + shape.radius * np.cos(angles),
            cy + shape.radius * np.sin(angles),
        ):
            assert pytest.approx(shape.distance(x, y)) == 0
