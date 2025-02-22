"""Test the circle module."""

import numpy as np
import pytest

from .bases import CIRCLE_REPR, CirclesModuleTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.circles]


class TestCircle(CirclesModuleTestBase):
    """Test the Circle class."""

    shape_name = 'circle'
    center_x, center_y = (20, 65)
    radius = 20.49038105676658
    distance_test_cases = (
        ((center_x, center_y + radius), 0),  # north
        ((center_x, center_y - radius), 0),  # south
        ((center_x + radius, center_y), 0),  # east
        ((center_x - radius, center_y), 0),  # west
        ((center_x, center_y), radius),  # center of circle
        ((10, 25), 20.740675199410028),  # inside the circle
        ((-20, 0), 55.831306555602154),  # outside the circle
    )
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
