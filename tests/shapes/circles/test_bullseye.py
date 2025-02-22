"""Test the bullseye module."""

import numpy as np
import pytest

from .bases import CIRCLE_REPR, CirclesModuleTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.circles]


class TestBullseye(CirclesModuleTestBase):
    """Test the Bullseye class."""

    shape_name = 'bullseye'
    center_x, center_y = (20, 65)
    inner_radius, outer_radius = (10.24519052838329, 20.49038105676658)
    mid_radius = (outer_radius + inner_radius) / 2
    distance_test_cases = (
        ((center_x, center_y + outer_radius), 0),  # north on outer ring
        ((center_x, center_y + inner_radius), 0),  # north on inner ring
        ((center_x, center_y - outer_radius), 0),  # south on outer ring
        ((center_x, center_y - inner_radius), 0),  # south on inner ring
        ((center_x + outer_radius, center_y), 0),  # east on outer ring
        ((center_x + inner_radius, center_y), 0),  # east on inner ring
        ((center_x - outer_radius, center_y), 0),  # west on outer ring
        ((center_x - inner_radius, center_y), 0),  # west on inner ring
        ((center_x, center_y), inner_radius),  # center of bullseye
        (
            (center_x, center_y + mid_radius),
            inner_radius / 2,
        ),  # between the circles (north)
        (
            (center_x, center_y - mid_radius),
            inner_radius / 2,
        ),  # between the circles (south)
        (
            (center_x + mid_radius, center_y),
            inner_radius / 2,
        ),  # between the circles (east)
        (
            (center_x - mid_radius, center_y),
            inner_radius / 2,
        ),  # between the circles (west)
        (
            (center_x, center_y + outer_radius * 2),
            outer_radius,
        ),  # north of both circles
        (
            (center_x - outer_radius * 1.5, center_y),
            inner_radius,
        ),  # west of both circles
    )
    repr_regex = (
        r'^<Bullseye>\n'
        r'  circles=\n'
        r'          ' + CIRCLE_REPR + '\n'
        r'          ' + CIRCLE_REPR + '$'
    )

    def test_init(self, shape):
        """Test that the Bullseye contains two concentric circles."""
        assert len(shape.circles) == 2

        a, b = shape.circles
        assert np.array_equal(a.center, b.center)
        assert a.radius != b.radius
