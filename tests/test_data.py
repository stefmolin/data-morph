"""Tests for data_morph.data subpackage."""

import os

import pandas as pd
import pytest
from numpy.testing import assert_equal
from pandas.testing import assert_frame_equal

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


@pytest.mark.parametrize('bounds', [[0, 100], (0, 100), None])
def test_dataset_normalization(bounds, datasets_dir):
    """Confirm that data normalization is working by checking min and max."""

    dataset = DataLoader.load_dataset('dino', bounds)

    if bounds:
        assert dataset._bounds == bounds
        assert_equal(dataset.df.min().to_numpy(), [bounds[0]] * 2)
        assert_equal(dataset.df.max().to_numpy(), [bounds[1]] * 2)
    else:
        df = pd.read_csv(os.path.join(datasets_dir, 'dino.csv'))
        assert dataset._bounds == [df.min().min(), df.max().max()]
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


def test_data_stats():
    """Test that summary statistics tuple is correct."""

    data = DataLoader.load_dataset('dino').df

    stats = get_values(data)

    assert stats.x_mean == data.x.mean()
    assert stats.y_mean == data.y.mean()
    assert stats.x_stdev == data.x.std()
    assert stats.y_stdev == data.y.std()
    assert stats.correlation == data.corr().x.y
