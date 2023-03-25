"""Tests for data_morph.data subpackage."""

from pathlib import Path

import pandas as pd
import pytest
from numpy.testing import assert_equal
from pandas.testing import assert_frame_equal

from data_morph.bounds.bounding_box import BoundingBox
from data_morph.data.dataset import Dataset
from data_morph.data.loader import DataLoader
from data_morph.data.stats import get_values


@pytest.fixture
def datasets_dir(request):
    """Fixture for the datasets directory."""
    return (
        Path(request.config.rootdir) / 'src' / 'data_morph' / 'data' / 'starter_shapes'
    )


def test_data_loader_static_class():
    """Make sure DataLoader can't be instantiated."""
    with pytest.raises(NotImplementedError):
        _ = DataLoader()


def test_data_loader_known_data(datasets_dir):
    """Confirm that loading the dataset by name and by path work."""
    dino_from_pkg = DataLoader.load_dataset('dino')
    dino_from_file = DataLoader.load_dataset(datasets_dir / 'dino.csv')

    assert dino_from_pkg.name == dino_from_file.name
    assert_frame_equal(dino_from_pkg.df, dino_from_file.df)


@pytest.mark.parametrize('dataset', ['does_not_exist', 'does_not_exist.csv'])
def test_data_loader_unknown_data(dataset):
    """Confirm that trying to load non-existent datasets raises an error."""
    with pytest.raises(ValueError, match='Unknown dataset'):
        _ = DataLoader.load_dataset(dataset)


@pytest.mark.parametrize('scale', [10, 0.5, None])
def test_dataset_scale_data(scale, datasets_dir):
    """Confirm that data scaling is working by checking min and max."""

    original_df = pd.read_csv(datasets_dir / 'dino.csv')
    original_min = original_df.min()
    original_max = original_df.max()

    dataset = DataLoader.load_dataset('dino', scale=scale)

    if scale:
        assert_equal(dataset.df.min().to_numpy(), original_min / scale)
        assert_equal(dataset.df.max().to_numpy(), original_max / scale)
    else:
        assert_frame_equal(dataset.df, original_df)


@pytest.mark.parametrize(
    'scale',
    [[3], (), '', '12', True, False, 0],
    ids=str,
)
def test_dataset_scale_data_valid_scale(scale):
    """Confirm that scaling doesn't happen unless scale is valid."""
    if scale is not False and scale == 0:
        exc = ValueError
        msg = 'scale must be non-zero'
    else:
        exc = TypeError
        msg = 'scale must be a numeric value'

    with pytest.raises(exc, match=msg):
        _ = DataLoader.load_dataset('dino', scale=scale)


def test_dataset_validation_missing_columns(datasets_dir):
    """Confirm that creation of a Dataset validates the DataFrame columns."""

    df = pd.read_csv(datasets_dir / 'dino.csv').rename(columns={'x': 'a'})

    with pytest.raises(ValueError, match='Columns "x" and "y" are required.'):
        _ = Dataset('dino', df)


def test_dataset_validation_fix_column_casing(datasets_dir):
    """Confirm that creating a Dataset with correct names but in wrong casing works."""

    df = pd.read_csv(datasets_dir / 'dino.csv').rename(columns={'x': 'X'})
    dataset = Dataset('dino', df)
    assert not dataset.df[dataset._REQUIRED_COLUMNS].empty


@pytest.mark.parametrize(
    ['scale', 'morph_bounds', 'plot_bounds'],
    [
        (
            10,
            [[1.4717959999999999, 10.579484], [-0.670515, 10.914105]],
            [[-0.7320549999999985, 12.783335], [-1.6359, 11.879489999999999]],
        ),
        (
            0.5,
            [[29.43592, 211.58968000000002], [-13.4103, 218.2821]],
            [[-14.641100000000009, 255.66670000000005], [-32.718, 237.58980000000003]],
        ),
        (
            None,
            [[14.71796, 105.79484000000001], [-6.70515, 109.14105]],
            [[-7.320550000000004, 127.83335000000002], [-16.359, 118.79490000000001]],
        ),
    ],
)
def test_dataset_derive_bounds(scale, morph_bounds, plot_bounds):
    """Test that Dataset._derive_bounds() is working."""
    dataset = DataLoader.load_dataset('dino', scale=scale)

    assert dataset.morph_bounds == BoundingBox(*morph_bounds)
    assert dataset.plot_bounds == BoundingBox(*plot_bounds)


@pytest.mark.parametrize('scale', [10, None])
def test_dataset_repr(scale):
    """Check Dataset.__repr__()."""

    dataset = DataLoader.load_dataset('dino', scale=scale)
    assert repr(dataset) == (f'<Dataset name=dino scaled={scale is not None}>')


def test_data_stats():
    """Test that summary statistics tuple is correct."""

    data = DataLoader.load_dataset('dino').df

    stats = get_values(data)

    assert stats.x_mean == data.x.mean()
    assert stats.y_mean == data.y.mean()
    assert stats.x_stdev == data.x.std()
    assert stats.y_stdev == data.y.std()
    assert stats.correlation == data.corr().x.y
