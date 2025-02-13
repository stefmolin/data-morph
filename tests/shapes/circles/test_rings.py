"""Test the rings module."""

import numpy as np
import pytest

from .bases import CIRCLE_REPR, CirclesModuleTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.circles]


class TestRings(CirclesModuleTestBase):
    """Test the Rings class."""

    shape_name = 'rings'
    distance_test_cases = (((20, 50), 3.16987), ((10, 25), 9.08004))
    repr_regex = (
        r'^<Rings>\n'
        r'  circles=\n'
        r'          ' + CIRCLE_REPR + '\n'
        r'          ' + CIRCLE_REPR + '\n'
        r'          ' + CIRCLE_REPR + '\n'
        r'          ' + CIRCLE_REPR + '$'
    )

    @pytest.mark.parametrize('num_rings', [3, 5])
    def test_init(self, shape_factory, num_rings):
        """Test that the Rings contains multiple concentric circles."""
        shape = shape_factory.generate_shape(self.shape_name, num_rings=num_rings)

        assert len(shape.circles) == num_rings
        assert all(
            np.array_equal(circle.center, shape.circles[0].center)
            for circle in shape.circles[1:]
        )
        assert len({circle.radius for circle in shape.circles}) == num_rings

    @pytest.mark.parametrize('num_rings', ['3', -5, 1, True])
    def test_num_rings_is_valid(self, shape_factory, num_rings):
        """Test that num_rings input validation is working."""
        if isinstance(num_rings, int):
            with pytest.raises(ValueError, match='num_rings must be greater than 1'):
                _ = shape_factory.generate_shape(self.shape_name, num_rings=num_rings)
        else:
            with pytest.raises(TypeError, match='num_rings must be an integer'):
                _ = shape_factory.generate_shape(self.shape_name, num_rings=num_rings)
