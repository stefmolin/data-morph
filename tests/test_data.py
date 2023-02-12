"""Tests for data_morph.data subpackage."""

import os

import pytest
from numpy.testing import assert_equal

from data_morph.data.loader import DataLoader


@pytest.fixture
def datasets_dir(request):
    """Fixture for the datasets directory."""
    return os.path.join(
        request.config.rootdir,
        'src',
        'data_morph',
        'data',
        'datasets',
    )


def test_data_load(datasets_dir):
    """Confirm that loading the dataset by name and by path work."""
    loader = DataLoader([0, 100])
    dino_from_pkg = loader.load_dataset('dino')
    dino_from_file = loader.load_dataset(os.path.join(datasets_dir, 'dino.csv'))

    assert dino_from_pkg[0] == dino_from_file[0]
    assert dino_from_pkg[1].equals(dino_from_file[1])


def test_data_normalization():
    """Confirm that data normalization is working by checking min and max."""

    bounds = [0, 100]
    loader = DataLoader(bounds)

    _, data = loader.load_dataset('dino')

    assert_equal(data.min().to_numpy(), [bounds[0]] * 2)
    assert_equal(data.max().to_numpy(), [bounds[1]] * 2)
