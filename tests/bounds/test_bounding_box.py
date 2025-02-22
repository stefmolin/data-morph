"""Test the bounding_box module."""

import re

import pytest

from data_morph.bounds.bounding_box import BoundingBox
from data_morph.bounds.interval import Interval


@pytest.mark.bounds
class TestBoundingBox:
    """Test the BoundingBox class."""

    @pytest.mark.input_validation
    @pytest.mark.parametrize(
        ('x_bounds', 'y_bounds'),
        [
            (None, None),
            ([0, 1], None),
            (None, [0, 1]),
            (Interval([0, 1]), None),
            (None, Interval([0, 1])),
        ],
        ids=[
            'neither',
            'just x',
            'just y',
            'just x with Interval',
            'just y with Interval',
        ],
    )
    def test_input_validation_bounds(self, x_bounds, y_bounds):
        """Test that the __init__() method checks for valid bounds."""
        with pytest.raises(ValueError, match='BoundingBox requires bounds'):
            _ = BoundingBox(x_bounds, y_bounds)

    @pytest.mark.input_validation
    @pytest.mark.parametrize('inclusive', ['ss', [True, True, False], [1, 2]])
    def test_input_validation_inclusive(self, inclusive):
        """Test that the __init__() method checks for valid inclusive value work."""
        with pytest.raises(ValueError, match='inclusive must be'):
            _ = BoundingBox([0, 1], [0, 1], inclusive)

    @pytest.mark.parametrize(
        ('x_bounds', 'y_bounds', 'inclusive', 'expected'),
        [
            ([0, 1], [0, 1], True, (True, True)),
            ([0, 1], [0, 1], False, (False, False)),
            (Interval([0, 1], True), Interval([0, 1], True), True, (True, True)),
            (Interval([0, 1], True), Interval([0, 1], True), False, (True, True)),
            (Interval([0, 1], True), [0, 1], True, (True, True)),
            ([0, 1], Interval([0, 1], True), True, (True, True)),
            (Interval([0, 1], True), [0, 1], False, (True, False)),
            ([0, 1], Interval([0, 1], True), False, (False, True)),
        ],
    )
    def test_init(self, x_bounds, y_bounds, inclusive, expected):
        """Test that the __init__() method is working."""

        bbox = BoundingBox(x_bounds, y_bounds, inclusive)
        assert bbox.x_bounds._inclusive == expected[0]
        assert bbox.y_bounds._inclusive == expected[1]

        # make sure the bounds were cloned
        if isinstance(x_bounds, Interval):
            assert bbox.x_bounds == x_bounds
            bbox.adjust_bounds(x=2)
            assert bbox.x_bounds != x_bounds

        if isinstance(y_bounds, Interval):
            assert bbox.y_bounds == y_bounds
            bbox.adjust_bounds(y=2)
            assert bbox.y_bounds != y_bounds

    @pytest.mark.parametrize(
        ('value', 'inclusive', 'expected'),
        [
            ([1, 1], True, True),
            ([1, 1], False, True),
            ([0, 0], True, True),
            ([0, 0], False, False),
        ],
        ids=[
            'inside box - inclusive',
            'inside box - exclusive',
            'on corner - inclusive',
            'on corner - exclusive',
        ],
    )
    def test_contains(self, value, inclusive, expected):
        """Test that [x, y] in BoundingBox is working."""
        bbox = BoundingBox([0, 10], [0, 10], inclusive)
        assert (value in bbox) == expected

    @pytest.mark.input_validation
    @pytest.mark.parametrize(
        'value',
        [
            [True, False],
            '12',
            12,
            False,
        ],
        ids=['list of Booleans', 'string of 2 numbers', 'two-digit integer', 'False'],
    )
    def test_contains_input_validation(self, value):
        """Test that input validation for `[x, y] in BoundingBox` is working."""
        bbox = BoundingBox([0, 10], [0, 10])
        with pytest.raises(ValueError, match='must be an iterable of 2 numeric values'):
            _ = value in bbox

    @pytest.mark.input_validation
    @pytest.mark.parametrize('other', [1, True, Interval([0, 1])])
    def test_eq_input_validation(self, other):
        """Test that input validation for the __eq__() method is working."""
        bbox = BoundingBox([0, 10], [0, 10])
        with pytest.raises(TypeError, match='only defined between BoundingBox objects'):
            _ = bbox == other

    def test_eq(self):
        """Test that the __eq__() method is working."""
        limits = ([0, 10], [0, 10])
        bbox1 = BoundingBox(*limits)
        bbox2 = BoundingBox(*limits)
        assert bbox1 == bbox2

        bbox1.adjust_bounds(x=1)
        assert bbox1 != bbox2

    def test_repr(self):
        """Test that the __repr__() method is working."""
        assert re.match(
            '<BoundingBox>\n. x=<Interval .+>\n  y=<Interval.+>',
            repr(BoundingBox([0, 10], [0, 10])),
        )

    @pytest.mark.input_validation
    @pytest.mark.parametrize(
        ('x', 'y'),
        [
            (True, True),
            (None, True),
            ('s', None),
            (None, 's'),
            ('s', 's'),
        ],
    )
    def test_adjust_bounds_input_validation(self, x, y):
        """Test that input validation on the adjust_bounds() method is working."""
        bbox = BoundingBox([0, 10], [0, 10])
        with pytest.raises(TypeError, match='value must be a numeric value'):
            bbox.adjust_bounds(x, y)

    @pytest.mark.parametrize(('x', 'y'), [(10, 10), (0, 10), (10, 0)])
    def test_adjust_bounds(self, x, y):
        """Test that the adjust_bounds() method is working."""
        start = [10, 90]
        bbox = BoundingBox(start, start)
        initial_range_x, initial_range_y = bbox.range

        bbox.adjust_bounds(x, y)
        new_range_x, new_range_y = bbox.range
        assert new_range_x == initial_range_x + x
        assert new_range_y == initial_range_y + y

    @pytest.mark.parametrize(
        ('x', 'y', 'shrink', 'expected_range'),
        [
            ([10, 90], [500, 600], False, 100),
            ([500, 600], [10, 90], True, 80),
            ([10, 90], [10, 90], False, 80),
        ],
    )
    def test_align_aspect_ratio(self, x, y, shrink, expected_range):
        """Test that the align_aspect_ratio() method is working."""
        bbox = BoundingBox(x, y)
        bbox.align_aspect_ratio(shrink)
        assert pytest.approx(bbox.aspect_ratio) == 1
        assert bbox.x_bounds.range == bbox.y_bounds.range == expected_range

    def test_clone(self):
        """Test that the clone() method is working."""
        bbox1 = BoundingBox([0, 10], [5, 10])
        bbox2 = bbox1.clone()
        assert bbox1 == bbox2

        bbox2.adjust_bounds(x=2, y=2)
        assert bbox1 != bbox2

    @pytest.mark.parametrize(
        ('x', 'y', 'expected'),
        [
            ([10, 90], [500, 600], 0.8),
            ([500, 600], [10, 90], 1.25),
            ([0, 10], [5, 10], 2),
            ([10, 90], [10, 90], 1),
        ],
    )
    def test_aspect_ratio(self, x, y, expected):
        """Test that the aspect_ratio property is working."""
        bbox = BoundingBox(x, y)
        assert bbox.aspect_ratio == expected

    def test_range(self):
        """Test that the range property is working."""
        bbox = BoundingBox([0, 10], [5, 10])
        assert bbox.range == (10, 5)

    def test_center(self):
        """Test that the center property is working."""
        bbox = BoundingBox([0, 10], [5, 10])
        assert bbox.center == (5, 7.5)
