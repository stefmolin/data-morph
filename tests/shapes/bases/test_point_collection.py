"""Test point_collection module."""

import re

import matplotlib.pyplot as plt
import pytest

from data_morph.shapes.bases.point_collection import PointCollection


@pytest.mark.points
@pytest.mark.shapes
class TestPointCollection:
    """Test the PointCollection class."""

    @pytest.fixture(scope='class')
    def point_collection(self):
        """An instance of PointCollection."""
        return PointCollection([0, 0], [20, 50])

    def test_distance_zero(self, point_collection):
        """Test the distance() method on points in the collection."""
        for point in point_collection.points:
            assert point_collection.distance(*point) == 0

    @pytest.mark.parametrize(
        ('point', 'expected_distance'), [((-1, 0), 1), ((-1, -1), 1.414214)], ids=str
    )
    def test_distance_nonzero(self, point_collection, point, expected_distance):
        """Test the distance() method on points not in the collection."""
        assert pytest.approx(point_collection.distance(*point)) == expected_distance

    def test_repr(self, point_collection):
        """Test that the __repr__() method is working."""
        assert (
            re.match(r'^<PointCollection of \d* points>$', repr(point_collection))
            is not None
        )

    @pytest.mark.parametrize('ax', [None, plt.subplots()[1]])
    def test_plot(self, point_collection, ax):
        """Test that plotting is working."""
        ax = point_collection.plot(ax)
        assert len(ax.collections[0].get_offsets().data) == len(point_collection.points)
        assert pytest.approx(ax.get_aspect()) == 1.0
