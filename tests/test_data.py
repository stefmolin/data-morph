"""Tests for data_morph.data subpackage."""

import os

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


@pytest.mark.parametrize(
    ['limits', 'inclusive'],
    [([0, 10], True), (None, False)],
    ids=['numeric + inclusive', 'empty'],
)
def test_bounds_init_and_bool(limits, inclusive):
    """Test that Bounds can be initialized and works as truthy/falsey value."""
    bounds = Bounds(limits, inclusive)
    assert bounds.bounds == limits
    assert bounds.inclusive == inclusive
    if bounds:
        assert limits is not None
    else:
        assert limits is None


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
        (None, False, 10, True),
    ],
    ids=[
        '0 in [0, 10]',
        '10 in [0, 10]',
        '5 in [0, 10]',
        '5 in (0, 10)',
        '0 not in (0, 10)',
        '10 not in (0, 10)',
        '10 in no limit',
    ],
)
def test_bounds_contains(limits, inclusive, value, expected):
    """Test that checking if a value is in the Bounds works."""
    bounds = Bounds(limits, inclusive)
    if expected:
        assert value in bounds
    else:
        assert value not in bounds


@pytest.mark.parametrize(
    'value',
    [[1, 1], True, (1, -1), {2}, 's', dict()],
    ids=['list', 'bool', 'tuple', 'set', 'str', 'dict'],
)
def test_bounds_contains_invalid(value):
    """Test that Bounds.__contains__() requires a numeric value."""
    with pytest.raises(TypeError, match='only supported for numeric values'):
        _ = value in Bounds()


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
