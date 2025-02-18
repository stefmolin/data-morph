"""Base test classes for points shapes."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pytest

if TYPE_CHECKING:
    from numbers import Number


class PointsModuleTestBase:
    """Base for testing point-based shapes."""

    shape_name: str
    distance_test_cases: tuple[tuple[tuple[Number], float]]

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
        assert pytest.approx(actual_distance, abs=1e-5) == expected_distance


class ParabolaTestBase(PointsModuleTestBase):
    """Base test class for parabolic shapes."""

    positive_quadratic_term: bool
    x_index: int
    y_index: int

    def test_quadratic_term(self, shape):
        """Check the sign of the quadratic term."""
        poly = np.polynomial.Polynomial.fit(
            shape.points[:, self.x_index], shape.points[:, self.y_index], 2
        )
        assert (poly.coef[2] > 0) == self.positive_quadratic_term
