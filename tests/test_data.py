"""Tests for data_morph.data subpackage."""

import os

import pytest

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
