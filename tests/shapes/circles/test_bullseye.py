"""Test the bullseye module."""

import numpy as np
import pytest

from .bases import CIRCLE_REPR, CirclesModuleTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.circles]


class TestBullseye(CirclesModuleTestBase):
    """Test the Bullseye class."""

    shape_name = 'bullseye'
    distance_test_cases = (((20, 50), 3.660254), ((10, 25), 9.08004))
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
