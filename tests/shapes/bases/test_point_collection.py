"""Test point_collection module."""

import re

import pytest

from data_morph.shapes.bases.point_collection import PointCollection


@pytest.mark.points
@pytest.mark.shapes
class TestPointCollection:
    """Test the PointCollection class."""

    point_collection = PointCollection([0, 0], [20, 50])

    def test_distance_zero(self):
        """Test the distance() method on points in the collection."""
        for point in self.point_collection.points:
            assert self.point_collection.distance(*point) == 0

    @pytest.mark.parametrize(
        ['point', 'expected_distance'], [[(-1, 0), 1], [(-1, -1), 1.414214]]
    )
    def test_distance_nonzero(self, point, expected_distance):
        """Test the distance() method on points not in the collection."""
        assert (
            pytest.approx(self.point_collection.distance(*point)) == expected_distance
        )

    def test_repr(self):
        """Test that the __repr__() method is working."""
        assert (
            re.match(r'^<PointCollection of \d* points>$', repr(self.point_collection))
            is not None
        )
