"""Base test class for circle shapes."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from numbers import Number

CIRCLE_REPR = r'<Circle center=\((\d+\.*\d*), (\d+\.*\d*)\) radius=(\d+\.*\d*)>'


class CirclesModuleTestBase:
    """Base for testing circle shapes."""

    shape_name: str
    distance_test_cases: tuple[tuple[tuple[Number], float]]
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
        actual_distance = shape.distance(*test_point)
        assert pytest.approx(actual_distance) == expected_distance

    def test_repr(self, shape):
        """Test that the __repr__() method is working."""
        assert re.match(self.repr_regex, repr(shape)) is not None
