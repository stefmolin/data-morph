"""Test line_collection module."""

import itertools
import re

import pytest

from data_morph.shapes.bases.line_collection import LineCollection


@pytest.mark.lines
@pytest.mark.shapes
class TestLineCollection:
    """Test the LineCollection class."""

    @pytest.fixture(scope='class')
    def line_collection(self):
        """An instance of LineCollection."""
        return LineCollection(
            [[0, 0], [0, 1]],
            [[1, 0], [1, 1]],
            [[10.5, 11.5], [11, 10]],
        )

    def test_distance_zero(self, line_collection):
        """Test the distance() method on points on lines in the collection."""
        for point in itertools.chain(*line_collection.lines):
            assert line_collection.distance(*point) == 0

    @pytest.mark.parametrize(
        ('point', 'expected_distance'), [((-1, 0), 1), ((-1, -1), 1.414214)], ids=str
    )
    def test_distance_nonzero(self, line_collection, point, expected_distance):
        """Test the distance() method on points not on lines in the collection."""
        assert pytest.approx(line_collection.distance(*point)) == expected_distance

    @pytest.mark.parametrize('line', [[(0, 0), (0, 0)], [(-1, -1), (-1, -1)]], ids=str)
    def test_line_as_point(self, line):
        """Test LineCollection raises a ValueError for small line magnitudes."""
        with pytest.raises(ValueError, match='same start and end'):
            LineCollection(line)

    def test_repr(self, line_collection):
        """Test that the __repr__() method is working."""
        assert (
            re.match(
                r"""<LineCollection>\n  lines=\n {8}array\(\[\[\d+""",
                repr(line_collection),
            )
            is not None
        )
