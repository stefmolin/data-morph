"""Test the dots_grid module."""

import numpy as np
import pytest

from .bases import PointsModuleTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.points]


class TestDotsGrid(PointsModuleTestBase):
    """Test the DotsGrid class."""

    shape_name = 'dots'
    distance_test_cases = (((20, 50), 0.0), ((30, 60), 3.640055))
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
