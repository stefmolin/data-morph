"""Test the rings module."""

import numpy as np
import pytest

from .bases import CIRCLE_REPR, CirclesModuleTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.circles]


class TestRings(CirclesModuleTestBase):
    """Test the Rings class."""

    shape_name = 'rings'
    center_x, center_y = (20, 65)
    radii = (3.666666666666667, 7.333333333333334, 11)
    mid_radii = (sum(radii[:2]) / 2, sum(radii[1:]) / 2)
    distance_test_cases = (
        ((center_x, center_y + radii[0]), 0),  # north on inner ring
        ((center_x, center_y + radii[1]), 0),  # north on middle ring
        ((center_x, center_y + radii[2]), 0),  # north on outer ring
        ((center_x, center_y - radii[0]), 0),  # south on inner ring
        ((center_x, center_y - radii[1]), 0),  # south on middle ring
        ((center_x, center_y - radii[2]), 0),  # south on outer ring
        ((center_x + radii[0], center_y), 0),  # east on inner ring
        ((center_x + radii[1], center_y), 0),  # east on middle ring
        ((center_x + radii[2], center_y), 0),  # east on outer ring
        ((center_x - radii[0], center_y), 0),  # west on inner ring
        ((center_x - radii[1], center_y), 0),  # west on middle ring
        ((center_x - radii[2], center_y), 0),  # west on outer ring
        ((center_x, center_y), radii[0]),  # center of all rings
        (
            (center_x, center_y + mid_radii[0]),
            radii[0] / 2,
        ),  # between the inner circles (north)
        (
            (center_x, center_y - mid_radii[0]),
            radii[0] / 2,
        ),  # between the inner circles (south)
        (
            (center_x + mid_radii[0], center_y),
            radii[0] / 2,
        ),  # between the inner circles (east)
        (
            (center_x - mid_radii[0], center_y),
            radii[0] / 2,
        ),  # between the inner circles (west)
        (
            (center_x, center_y + mid_radii[1]),
            radii[0] / 2,
        ),  # between the outer circles (north)
        (
            (center_x, center_y - mid_radii[1]),
            radii[0] / 2,
        ),  # between the outer circles (south)
        (
            (center_x + mid_radii[1], center_y),
            radii[0] / 2,
        ),  # between the outer circles (east)
        (
            (center_x - mid_radii[1], center_y),
            radii[0] / 2,
        ),  # between the outer circles (west)
        ((center_x, center_y + radii[2] * 2), radii[2]),  # north of all circles
        ((center_x - radii[2] * 1.5, center_y), radii[2] / 2),  # west of all circles
    )
    repr_regex = (
        r'^<Rings>\n'
        r'  circles=\n'
        r'          ' + CIRCLE_REPR + '\n'
        r'          ' + CIRCLE_REPR + '\n'
        r'          ' + CIRCLE_REPR + '$'
    )

    def test_init(self, shape_factory):
        """Test that the Rings contains three concentric circles."""
        shape = shape_factory.generate_shape(self.shape_name)

        num_rings = 3
        assert len(shape.circles) == num_rings
        assert all(
            np.array_equal(circle.center, shape.circles[0].center)
            for circle in shape.circles[1:]
        )
        assert len({circle.radius for circle in shape.circles}) == num_rings
