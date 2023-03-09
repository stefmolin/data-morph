"""Tests for data_morph.bounds subpackage."""

import re

import pytest

from data_morph.bounds.bounding_box import BoundingBox
from data_morph.bounds.interval import Interval
from data_morph.bounds.utils import _validate_2d


@pytest.mark.parametrize(
    ['data', 'msg'],
    [
        (True, 'must be an iterable of 2 numeric values'),
        ({1, 2}, 'must be an iterable of 2 numeric values'),
        ('12', 'must be an iterable of 2 numeric values'),
        ([0, False], 'must be an iterable of 2 numeric values'),
        ([1, 2], False),
    ],
    ids=['True', '{1, 2}', '12', '[0, False]', '[1, 2]'],
)
def test_validate_2d(data, msg):
    """Test that 2D numeric value check is working."""
    if msg:
        with pytest.raises(ValueError, match=msg):
            _ = _validate_2d(data, 'test')
    else:
        assert data == _validate_2d(data, 'test')


def test_bounds_init():
    """Test that Interval can be initialized."""
    limits, inclusive = [0, 10], True
    bounds = Interval(limits, inclusive)
    assert bounds.bounds == limits
    assert bounds.inclusive == inclusive


@pytest.mark.parametrize(
    'limits',
    [[1, 1], [1.0, 1], [1, -1]],
    ids=['no range', 'no range, float vs. int', 'right <= left bound'],
)
def test_bounds_invalid(limits):
    """Test that Interval requires a valid range."""
    with pytest.raises(ValueError, match='must be strictly greater than'):
        _ = Interval(limits)


@pytest.mark.parametrize(
    ['limits', 'inclusive', 'value', 'expected'],
    [
        ([0, 10], True, 0, True),
        ([0, 10], True, 10, True),
        ([0, 10], True, 5, True),
        ([0, 10], False, 5, True),
        ([0, 10], False, 0, False),
        ([0, 10], False, 10, False),
    ],
    ids=[
        '0 in [0, 10]',
        '10 in [0, 10]',
        '5 in [0, 10]',
        '5 in (0, 10)',
        '0 not in (0, 10)',
        '10 not in (0, 10)',
    ],
)
def test_bounds_contains(limits, inclusive, value, expected):
    """Test that checking if a value is in the Interval works."""
    bounds = Interval(limits, inclusive)
    assert (value in bounds) == expected


@pytest.mark.parametrize(
    'value',
    [[1, 1], True, (1, -1), {2}, 's', dict(), None],
    ids=str,
)
def test_bounds_contains_invalid(value):
    """Test that Interval.__contains__() requires a numeric value."""
    with pytest.raises(TypeError, match='only supported for numeric values'):
        _ = value in Interval([0, 10])


@pytest.mark.parametrize(
    ['limits', 'inclusive', 'expected'],
    [
        ([0, 1], True, True),
        ([0, 1], False, False),
        ([-1, 1], True, False),
        ([-1, 1], False, False),
    ],
)
def test_bounds_eq(limits, inclusive, expected):
    """Test that Interval equality check is working."""
    assert (Interval([0, 1], True) == Interval(limits, inclusive)) == expected


@pytest.mark.parametrize('other', ['s', [], {}, 7])
def test_bounds_eq_type(other):
    """Test that Interval equality check only works for Interval objects."""
    with pytest.raises(TypeError, match='only defined between Interval objects'):
        _ = Interval([0, 1], True) == other


def test_bounds_getitem():
    """Test that Interval.__getitem__() is working."""
    limits = [0, 1]
    bounds = Interval(limits)
    assert bounds[0] == limits[0]
    assert bounds[1] == limits[1]


def test_bounds_iter():
    """Test that Interval.__iter__() is working."""
    limits = [0, 1]
    for bound, limit in zip(Interval(limits), limits):
        assert bound == limit


@pytest.mark.parametrize(
    ['inclusive', 'expected'],
    [
        (True, '<Interval inclusive [0, 1]>'),
        (False, '<Interval exclusive (0, 1)>'),
    ],
)
def test_bounds_repr(inclusive, expected):
    """Test that Interval.__repr__() is working."""
    bounds = Interval([0, 1], inclusive)
    assert repr(bounds) == expected


@pytest.mark.parametrize(
    ['value', 'expected_msg', 'exc_class'],
    [
        (0, 'value must be non-zero', ValueError),
        (None, 'value must be a numeric value', TypeError),
        ('s', 'value must be a numeric value', TypeError),
        (True, 'value must be a numeric value', TypeError),
    ],
)
def test_bounds_adjust_bounds_input_validation(value, expected_msg, exc_class):
    """Test that input validation on Interval.adjust_bounds() is working."""
    bounds = Interval([10, 90])

    with pytest.raises(exc_class, match=expected_msg):
        bounds.adjust_bounds(value)


@pytest.mark.parametrize('value', [2, -8])
def test_bounds_adjust_bounds(value):
    """Test that Interval.adjust_bounds() value update is working."""
    start = [10, 90]
    bounds = Interval(start)
    initial_range = bounds.range

    bounds.adjust_bounds(value)
    assert bounds.range == initial_range + value
    assert bounds[0] == start[0] - value / 2
    assert bounds[1] == start[1] + value / 2


@pytest.mark.parametrize(
    ['limits', 'inclusive'],
    [
        ([10, 90], True),
        ([10, 90], False),
    ],
    ids=['inclusive', 'exclusive'],
)
def test_bounds_clone(limits, inclusive):
    """Test that Interval.clone() and equality check is working."""
    bounds = Interval(limits, inclusive)
    bounds_clone = bounds.clone()

    # confirm it is a new object
    assert bounds is not bounds_clone

    # confirm equality of values
    assert bounds.bounds == bounds_clone.bounds
    assert bounds.inclusive == bounds_clone.inclusive
    assert bounds == bounds_clone

    # confirm deep copy of bounds
    bounds_clone.adjust_bounds(2)
    assert bounds.bounds != bounds_clone.bounds
    assert bounds != bounds_clone


@pytest.mark.parametrize('inclusive', [True, False])
@pytest.mark.parametrize(
    ['limits', 'expected'],
    [
        ([-10, -5], 5),
        ([-1, 1], 2),
        ([2, 100], 98),
    ],
    ids=str,
)
def test_bounds_range(limits, inclusive, expected):
    """Test that Interval.range is working."""
    bounds = Interval(limits, inclusive)
    assert bounds.range == expected


@pytest.mark.parametrize(
    ['x_bounds', 'y_bounds'],
    [
        [None, None],
        [[0, 1], None],
        [None, [0, 1]],
        [Interval([0, 1]), None],
        [None, Interval([0, 1])],
    ],
    ids=[
        'neither',
        'just x',
        'just y',
        'just x with Interval',
        'just y with Interval',
    ],
)
def test_bounding_box_input_validation_bounds(x_bounds, y_bounds):
    """Test that BoundingBox.__init__() checks for valid bounds."""
    with pytest.raises(ValueError, match='BoundingBox requires bounds'):
        _ = BoundingBox(x_bounds, y_bounds)


@pytest.mark.parametrize('inclusive', ['ss', [True, True, False], [1, 2]])
def test_bounding_box_input_validation_inclusive(inclusive):
    """Test that BoundingBox.__init__() checks for valid inclusive value work."""
    with pytest.raises(ValueError, match='inclusive must be'):
        _ = BoundingBox([0, 1], [0, 1], inclusive)


@pytest.mark.parametrize(
    ['x_bounds', 'y_bounds', 'inclusive', 'expected'],
    [
        [[0, 1], [0, 1], True, (True, True)],
        [[0, 1], [0, 1], False, (False, False)],
        [Interval([0, 1], True), Interval([0, 1], True), True, (True, True)],
        [Interval([0, 1], True), Interval([0, 1], True), False, (True, True)],
        [Interval([0, 1], True), [0, 1], True, (True, True)],
        [[0, 1], Interval([0, 1], True), True, (True, True)],
        [Interval([0, 1], True), [0, 1], False, (True, False)],
        [[0, 1], Interval([0, 1], True), False, (False, True)],
    ],
)
def test_bounding_box_init(x_bounds, y_bounds, inclusive, expected):
    """Test that BoundingBox.__init__() is working."""

    bbox = BoundingBox(x_bounds, y_bounds, inclusive)
    assert bbox.x_bounds.inclusive == expected[0]
    assert bbox.y_bounds.inclusive == expected[1]

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
    ['value', 'inclusive', 'expected'],
    [
        [[1, 1], True, True],
        [[1, 1], False, True],
        [[0, 0], True, True],
        [[0, 0], False, False],
    ],
    ids=[
        'inside box - inclusive',
        'inside box - exclusive',
        'on corner - inclusive',
        'on corner - exclusive',
    ],
)
def test_bounding_box_contains(value, inclusive, expected):
    """Test that [x, y] in BoundingBox is working."""
    bbox = BoundingBox([0, 10], [0, 10], inclusive)
    assert (value in bbox) == expected


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
def test_bounding_box_contains_input_validation(value):
    """Test that [x, y] in BoundingBox is working."""
    bbox = BoundingBox([0, 10], [0, 10])
    with pytest.raises(ValueError, match='must be an iterable of 2 numeric values'):
        _ = value in bbox


@pytest.mark.parametrize('other', [1, True, Interval([0, 1])])
def test_bounding_box_eq_input_validation(other):
    """Test that input validation for BoundingBox.__eq__() is working."""
    bbox = BoundingBox([0, 10], [0, 10])
    with pytest.raises(TypeError, match='only defined between BoundingBox objects'):
        _ = bbox == other


def test_bounding_box_eq():
    """Test that BoundingBox.__eq__() is working."""
    limits = ([0, 10], [0, 10])
    bbox1 = BoundingBox(*limits)
    bbox2 = BoundingBox(*limits)
    assert bbox1 == bbox2

    bbox1.adjust_bounds(x=1)
    assert bbox1 != bbox2


def test_bounding_box_repr():
    """Test that BoundingBox.__repr__() is working."""
    assert re.match(
        '<BoundingBox>\n. x=<Interval .+>\n  y=<Interval.+>',
        repr(BoundingBox([0, 10], [0, 10])),
    )


@pytest.mark.parametrize(
    ['x', 'y'],
    [
        [True, True],
        [None, True],
        ['s', None],
        [None, 's'],
        ['s', 's'],
    ],
)
def test_bounding_box_adjust_bounds_input_validation(x, y):
    """Test that input validation on BoundingBox.adjust_bounds() is working."""
    bbox = BoundingBox([0, 10], [0, 10])
    with pytest.raises(TypeError, match='value must be a numeric value'):
        bbox.adjust_bounds(x, y)


@pytest.mark.parametrize(['x', 'y'], [[10, 10], [0, 10], [10, 0]])
def test_bounding_box_adjust_bounds(x, y):
    """Test that BoundingBox.adjust_bounds() is working."""
    start = [10, 90]
    bbox = BoundingBox(start, start)
    initial_range_x, initial_range_y = bbox.range

    bbox.adjust_bounds(x, y)
    new_range_x, new_range_y = bbox.range
    assert new_range_x == initial_range_x + x
    assert new_range_y == initial_range_y + y


@pytest.mark.parametrize(
    ['x', 'y'],
    [
        ([10, 90], [500, 600]),
        ([500, 600], [10, 90]),
        ([10, 90], [10, 90]),
    ],
)
def test_bounding_box_align_aspect_ratio(x, y):
    """Test that BoundingBox.align_aspect_ratio() is working."""
    bbox = BoundingBox(x, y)
    bbox.align_aspect_ratio()
    assert pytest.approx(bbox.aspect_ratio) == 1


def test_bounding_box_clone():
    """Test that BoundingBox.clone() is working."""
    bbox1 = BoundingBox([0, 10], [5, 10])
    bbox2 = bbox1.clone()
    assert bbox1 == bbox2

    bbox2.adjust_bounds(x=2, y=2)
    assert bbox1 != bbox2


@pytest.mark.parametrize(
    ['x', 'y', 'expected'],
    [
        ([10, 90], [500, 600], 0.8),
        ([500, 600], [10, 90], 1.25),
        ([0, 10], [5, 10], 2),
        ([10, 90], [10, 90], 1),
    ],
)
def test_bounding_box_aspect_ratio(x, y, expected):
    """Test that BoundingBox.aspect_ratio is working."""
    bbox = BoundingBox(x, y)
    assert bbox.aspect_ratio == expected


def test_bounding_box_range():
    """Test that BoundingBox.range is working."""
    bbox = BoundingBox([0, 10], [5, 10])
    assert bbox.range == (10, 5)
