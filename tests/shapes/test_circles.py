"""Test circles module."""

import re
from numbers import Number
from typing import Iterable, Tuple

import numpy as np
import pytest

pytestmark = [pytest.mark.shapes, pytest.mark.circles]


class CirclesModuleTestBase:
    """Base for testing circle shapes."""

    shape_name: str
    distance_test_cases: Iterable[Tuple[Iterable[Number], float]]
    repr_regex: str

    @pytest.fixture(scope='class')
    def shape(self, shape_factory):
        """Fixture to get the shape for testing."""
        return shape_factory.generate_shape(self.shape_name)

    def test_distance(self, shape, test_point, expected_distance):
        """
        Test the distance() method parametrized by distance_test_cases
        (see conftest.py).
        """
        assert pytest.approx(shape.distance(*test_point)) == expected_distance

    def test_repr(self, shape):
        """Test that the __repr__() method is working."""
        assert re.match(self.repr_regex, repr(shape)) is not None


class TestBullseye(CirclesModuleTestBase):
    """Test the Bullseye class."""

    shape_name = 'bullseye'
    distance_test_cases = [[(20, 50), 3.660254], [(10, 25), 9.08004]]
    repr_regex = (
        r'^<Bullseye>\n'
        r'  circles=\n'
        r'          <Circle cx=(\d+\.*\d*) cy=(\d+\.*\d*) r=(\d+\.*\d*)>\n'
        r'          <Circle cx=(\d+\.*\d*) cy=(\d+\.*\d*) r=(\d+\.*\d*)>$'
    )

    def test_init(self, shape):
        """Test that the Bullseye contains two concentric circles."""
        assert len(shape.circles) == 2

        a, b = shape.circles
        assert a.cx == b.cx
        assert a.cy == b.cy
        assert a.r != b.r


class TestCircle(CirclesModuleTestBase):
    """Test the Circle class."""

    shape_name = 'circle'
    distance_test_cases = [[(20, 50), 10.490381], [(10, 25), 15.910168]]
    repr_regex = r'^<Circle cx=(\d+\.*\d*) cy=(\d+\.*\d*) r=(\d+\.*\d*)>$'

    def test_is_circle(self, shape):
        """Test that the Circle is a valid circle (mathematically)."""
        angles = np.arange(0, 361, 45)
        for x, y in zip(
            shape.cx + shape.r * np.cos(angles),
            shape.cy + shape.r * np.sin(angles),
        ):
            assert pytest.approx(shape.distance(x, y)) == 0


class TestRings(CirclesModuleTestBase):
    """Test the Rings class."""

    shape_name = 'rings'
    distance_test_cases = [[(20, 50), 3.16987], [(10, 25), 9.08004]]
    repr_regex = (
        r'^<Rings>\n'
        r'  circles=\n'
        r'          <Circle cx=(\d+\.*\d*) cy=(\d+\.*\d*) r=(\d+\.*\d*)>\n'
        r'          <Circle cx=(\d+\.*\d*) cy=(\d+\.*\d*) r=(\d+\.*\d*)>'
    )

    @pytest.mark.parametrize('num_rings', [3, 5])
    def test_init(self, shape_factory, num_rings):
        """Test that the Rings contains multiple concentric circles."""
        shape = shape_factory.generate_shape(self.shape_name, num_rings=num_rings)

        assert len(shape.circles) == num_rings
        assert all(
            getattr(circle, center_coord) == getattr(shape.circles[0], center_coord)
            for circle in shape.circles[1:]
            for center_coord in ['cx', 'cy']
        )
        assert len({circle.r for circle in shape.circles}) == num_rings

    @pytest.mark.parametrize('num_rings', ['3', -5, 1, True])
    def test_num_rings_is_valid(self, shape_factory, num_rings):
        """Test that num_rings input validation is working."""
        if isinstance(num_rings, int):
            with pytest.raises(ValueError, match='num_rings must be greater than 1'):
                _ = shape_factory.generate_shape(self.shape_name, num_rings=num_rings)
        else:
            with pytest.raises(TypeError, match='num_rings must be an integer'):
                _ = shape_factory.generate_shape(self.shape_name, num_rings=num_rings)
