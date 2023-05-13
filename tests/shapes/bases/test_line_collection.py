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
        ['point', 'expected_distance'], [[(-1, 0), 1], [(-1, -1), 1.414214]], ids=str
    )
    def test_distance_nonzero(self, line_collection, point, expected_distance):
        """Test the distance() method on points not on lines in the collection."""
        assert pytest.approx(line_collection.distance(*point)) == expected_distance

    @pytest.mark.parametrize('line', [[(0, 0), (0, 0)], [(-1, -1), (-1, -1)]], ids=str)
    def test_distance_to_small_line_magnitude(self, line_collection, line):
        """Test _distance_point_to_line() for small line magnitudes."""
        distance = line_collection._distance_point_to_line((30, 50), line)
        assert distance == 9999

    def test_repr(self, line_collection):
        """Test that the __repr__() method is working."""
        lines = r'\n        '.join(
            [r'\[\[\d+\.*\d*, \d+\.*\d*\], \[\d+\.*\d*, \d+\.*\d*\]\]']
            * len(line_collection.lines)
        )
        assert (
            re.match(
                (r'^<LineCollection>\n  lines=\n        ' + lines),
                repr(line_collection),
            )
            is not None
        )
