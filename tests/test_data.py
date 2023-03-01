"""Tests for data_morph.data subpackage."""

import os
import re

import pandas as pd
import pytest
from numpy.testing import assert_equal
from pandas.testing import assert_frame_equal

from data_morph.data.bounds import BoundingBox, Bounds, _validate_2d
from data_morph.data.dataset import Dataset
from data_morph.data.loader import DataLoader
from data_morph.data.stats import get_values


@pytest.fixture
def datasets_dir(request):
    """Fixture for the datasets directory."""
    return os.path.join(
        request.config.rootdir,
        'src',
        'data_morph',
        'data',
        'starter_shapes',
    )


def test_data_loader_static_class():
    """Make sure DataLoader can't be instantiated."""
    with pytest.raises(NotImplementedError):
        _ = DataLoader()


def test_data_loader_known_data(datasets_dir):
    """Confirm that loading the dataset by name and by path work."""
    dino_from_pkg = DataLoader.load_dataset('dino')
    dino_from_file = DataLoader.load_dataset(os.path.join(datasets_dir, 'dino.csv'))

    assert dino_from_pkg.name == dino_from_file.name
    assert_frame_equal(dino_from_pkg.df, dino_from_file.df)


@pytest.mark.parametrize('dataset', ['does_not_exist', 'does_not_exist.csv'])
def test_data_loader_unknown_data(dataset):
    """Confirm that trying to load non-existent datasets raises an error."""
    with pytest.raises(ValueError, match='Unknown dataset'):
        _ = DataLoader.load_dataset(dataset)


@pytest.mark.parametrize('bounds', [[-20, 120], (-20, 120), None])
def test_dataset_normalization(bounds, datasets_dir):
    """Confirm that data normalization is working by checking min and max."""

    dataset = DataLoader.load_dataset('dino', bounds)

    if bounds:
        assert_equal(dataset.df.min().to_numpy(), [bounds[0]] * 2)
        assert_equal(dataset.df.max().to_numpy(), [bounds[1]] * 2)
    else:
        df = pd.read_csv(os.path.join(datasets_dir, 'dino.csv'))
        assert_frame_equal(dataset.df, df)


@pytest.mark.parametrize(
    'bounds',
    [[], (), '', [3], [1, 2, 3], '12', [True, False]],
    ids=[
        'empty list',
        'empty tuple',
        'empty string',
        'too few dimensions',
        'too many dimensions',
        'not list or tuple',
        'booleans',
    ],
)
def test_dataset_normalization_valid_bounds(bounds):
    """Confirm that normalization doesn't happen unless bounds are valid."""
    with pytest.raises(ValueError, match='bounds must be an iterable'):
        _ = DataLoader.load_dataset('dino', bounds)


def test_dataset_validation_missing_columns(datasets_dir):
    """Confirm that creation of a Dataset validates the DataFrame columns."""

    df = pd.read_csv(os.path.join(datasets_dir, 'dino.csv')).rename(columns={'x': 'a'})

    with pytest.raises(ValueError, match='Columns "x" and "y" are required.'):
        _ = Dataset('dino', df)


def test_dataset_validation_fix_column_casing(datasets_dir):
    """Confirm that creating a Dataset with correct names but in wrong casing works."""

    df = pd.read_csv(os.path.join(datasets_dir, 'dino.csv')).rename(columns={'x': 'X'})
    dataset = Dataset('dino', df)
    assert not dataset.df[dataset.REQUIRED_COLUMNS].empty


@pytest.mark.parametrize(
    ['limits', 'morph_bounds', 'plot_bounds'],
    [
        ([10, 90], [2, 98], [-6, 106]),
        ([0, 100], [-10, 110], [-20, 120]),
    ],
)
def test_dataset_derive_bounds(limits, morph_bounds, plot_bounds):
    """Test that Dataset._derive_bounds() is working."""
    dataset = DataLoader.load_dataset('dino', limits)

    assert dataset.morph_bounds == BoundingBox(morph_bounds, morph_bounds)
    assert dataset.plot_bounds == BoundingBox(plot_bounds, plot_bounds)


@pytest.mark.parametrize('bounds', [[10, 90], None])
def test_dataset_repr(bounds):
    """Check Dataset.__repr__()."""

    dataset = DataLoader.load_dataset('dino', bounds=bounds)
    assert repr(dataset) == (f'<Dataset name=dino normalized={bounds is not None}>')


def test_data_stats():
    """Test that summary statistics tuple is correct."""

    data = DataLoader.load_dataset('dino').df

    stats = get_values(data)

    assert stats.x_mean == data.x.mean()
    assert stats.y_mean == data.y.mean()
    assert stats.x_stdev == data.x.std()
    assert stats.y_stdev == data.y.std()
    assert stats.correlation == data.corr().x.y


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
    """Test that Bounds can be initialized."""
    limits, inclusive = [0, 10], True
    bounds = Bounds(limits, inclusive)
    assert bounds.bounds == limits
    assert bounds.inclusive == inclusive


@pytest.mark.parametrize(
    'limits',
    [[1, 1], [1.0, 1], [1, -1]],
    ids=['no range', 'no range, float vs. int', 'right <= left bound'],
)
def test_bounds_invalid(limits):
    """Test that Bounds requires a valid range."""
    with pytest.raises(ValueError, match='must be strictly greater than'):
        _ = Bounds(limits)


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
    """Test that checking if a value is in the Bounds works."""
    bounds = Bounds(limits, inclusive)
    assert (value in bounds) == expected


@pytest.mark.parametrize(
    'value',
    [[1, 1], True, (1, -1), {2}, 's', dict(), None],
    ids=['list', 'bool', 'tuple', 'set', 'str', 'dict', 'None'],
)
def test_bounds_contains_invalid(value):
    """Test that Bounds.__contains__() requires a numeric value."""
    with pytest.raises(TypeError, match='only supported for numeric values'):
        _ = value in Bounds([0, 10])


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
    """Test that Bounds equality check is working."""
    assert (Bounds([0, 1], True) == Bounds(limits, inclusive)) == expected


@pytest.mark.parametrize('other', ['s', [], {}, 7])
def test_bounds_eq_type(other):
    """Test that Bounds equality check only works for Bounds objects."""
    with pytest.raises(TypeError, match='only defined between Bounds objects'):
        _ = Bounds([0, 1], True) == other


def test_bounds_getitem():
    """Test that Bounds.__getitem__() is working."""
    limits = [0, 1]
    bounds = Bounds(limits)
    assert bounds[0] == limits[0]
    assert bounds[1] == limits[1]


def test_bounds_iter():
    """Test that Bounds.__iter__() is working."""
    limits = [0, 1]
    for bound, limit in zip(Bounds(limits), limits):
        assert bound == limit


@pytest.mark.parametrize(
    ['inclusive', 'expected'],
    [
        (True, '<Bounds inclusive [0, 1]>'),
        (False, '<Bounds exclusive (0, 1)>'),
    ],
)
def test_bounds_repr(inclusive, expected):
    """Test that Bounds.__repr__() is working."""
    bounds = Bounds([0, 1], inclusive)
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
    """Test that input validation on Bounds.adjust_bounds() is working."""
    bounds = Bounds([10, 90])

    with pytest.raises(exc_class, match=expected_msg):
        bounds.adjust_bounds(value)


@pytest.mark.parametrize('value', [2, -8])
def test_bounds_adjust_bounds(value):
    """Test that Bounds.adjust_bounds() value update is working."""
    start = [10, 90]
    bounds = Bounds(start)
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
    """Test that Bounds.clone() and equality check is working."""
    bounds = Bounds(limits, inclusive)
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
def test_bounds_range(inclusive):
    """Test that Bounds.range is working."""
    bounds = Bounds([-1, 1], inclusive)
    assert bounds.range == 2


@pytest.mark.parametrize(
    ['x_bounds', 'y_bounds'],
    [
        [None, None],
        [[0, 1], None],
        [None, [0, 1]],
        [Bounds([0, 1]), None],
        [None, Bounds([0, 1])],
    ],
    ids=[
        'neither',
        'just x',
        'just y',
        'just x with Bounds',
        'just y with Bounds',
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
        [Bounds([0, 1], True), Bounds([0, 1], True), True, (True, True)],
        [Bounds([0, 1], True), Bounds([0, 1], True), False, (True, True)],
        [Bounds([0, 1], True), [0, 1], True, (True, True)],
        [[0, 1], Bounds([0, 1], True), True, (True, True)],
        [Bounds([0, 1], True), [0, 1], False, (True, False)],
        [[0, 1], Bounds([0, 1], True), False, (False, True)],
    ],
)
def test_bounding_box_init(x_bounds, y_bounds, inclusive, expected):
    """Test that BoundingBox.__init__() is working."""

    bbox = BoundingBox(x_bounds, y_bounds, inclusive)
    assert bbox.x_bounds.inclusive == expected[0]
    assert bbox.y_bounds.inclusive == expected[1]

    # make sure the bounds were cloned
    if isinstance(x_bounds, Bounds):
        assert bbox.x_bounds == x_bounds
        bbox.adjust_bounds(x=2)
        assert bbox.x_bounds != x_bounds

    if isinstance(y_bounds, Bounds):
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


@pytest.mark.parametrize('other', [1, True, Bounds([0, 1])])
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
        '<BoundingBox>\n. x=<Bounds .+>\n  y=<Bounds.+>',
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
