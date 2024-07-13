"""Test points module."""

from numbers import Number
from typing import Iterable, Tuple

import numpy as np
import pytest

pytestmark = [pytest.mark.shapes, pytest.mark.points]


class PointsModuleTestBase:
    """Base for testing point-based shapes."""

    shape_name: str
    distance_test_cases: Iterable[Tuple[Iterable[Number], float]]

    @pytest.fixture(scope='class')
    def shape(self, shape_factory):
        """Fixture to get the shape for testing."""
        return shape_factory.generate_shape(self.shape_name)

    def test_distance(self, shape, test_point, expected_distance):
        """
        Test the distance() method parametrized by distance_test_cases
        (see conftest.py).
        """
        assert pytest.approx(shape.distance(*test_point), abs=1e-5) == expected_distance


class TestDotsGrid(PointsModuleTestBase):
    """Test the DotsGrid class."""

    shape_name = 'dots'
    distance_test_cases = [[(20, 50), 0.0], [(30, 60), 3.640055]]
    expected_point_count = 9

    def test_init(self, shape):
        """Test that the shape consists of the correct number points."""
        num_unique_points, *_ = np.unique(shape.points, axis=0).shape
        assert num_unique_points == self.expected_point_count

    def test_points_form_symmetric_grid(self, shape):
        """Test that the points form a 3x3 symmetric grid."""
        points = sorted(shape.points.tolist())

        top_row = points[:3]
        middle_row = points[3:6]
        bottom_row = points[6:]

        # check x values
        for row in [top_row, middle_row, bottom_row]:
            # check x values are the same for all points in the column
            assert row[0][0] == row[1][0] == row[2][0]

            # check that the middle column is truly in the middle
            col_midpoint = (row[0][0] + row[2][0]) / 2
            assert col_midpoint == row[1][0]

        # check y values
        for point in range(3):
            # check y values are the same for all points in the column
            assert top_row[point][1] == middle_row[point][1] == bottom_row[point][1]

            # check that the middle row is truly in the middle
            row_midpoint = (top_row[point][1] + bottom_row[point][1]) / 2
            assert row_midpoint == middle_row[point][1]


class TestHeart(PointsModuleTestBase):
    """Test the Heart class."""

    shape_name = 'heart'
    distance_test_cases = [
        [(19.89946048, 54.82281916), 0.0],
        [(10.84680454, 70.18556376), 0.0],
        [(29.9971295, 67.66402445), 0.0],
        [(27.38657942, 62.417184), 0.0],
        [(20, 50), 4.567369],
        [(10, 80), 8.564365],
    ]


class TestScatter(PointsModuleTestBase):
    """Test the Scatter class."""

    shape_name = 'scatter'
    distance_test_cases = [[(20, 50), 0.0], [(30, 60), 0.0], [(-500, -150), 0.0]]


class TestSpiral(PointsModuleTestBase):
    """Test the Spiral class."""

    shape_name = 'spiral'
    distance_test_cases = [[(20, 60), 0.0], [(70, 90), 50.0]]


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


class TestDownParabola(ParabolaTestBase):
    """Test the DownParabola class."""

    shape_name = 'down_parab'
    distance_test_cases = [[(20, 50), 7.929688], [(30, 60), 3.455534]]
    positive_quadratic_term = False
    x_index = 0
    y_index = 1


class TestLeftParabola(ParabolaTestBase):
    """Test the LeftParabola class."""

    shape_name = 'left_parab'
    distance_test_cases = [[(50, 20), 46.31798], [(10, 77), 0.0]]
    positive_quadratic_term = False
    x_index = 1
    y_index = 0


class TestRightParabola(ParabolaTestBase):
    """Test the RightParabola class."""

    shape_name = 'right_parab'
    distance_test_cases = [[(50, 20), 38.58756], [(10, 77), 7.740692]]
    positive_quadratic_term = True
    x_index = 1
    y_index = 0


class TestUpParabola(ParabolaTestBase):
    """Test the UpParabola class."""

    shape_name = 'up_parab'
    distance_test_cases = [[(0, 0), 53.774155], [(30, 60), 5.2576809]]
    positive_quadratic_term = True
    x_index = 0
    y_index = 1
