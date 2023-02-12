"""Tests for data_morph.data subpackage."""

import os

from data_morph.data.loader import DataLoader

DATASETS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'src/data_morph/data/datasets',
)


def test_data_load():
    """Confirm that loading the dataset by name and by path work."""
    loader = DataLoader([0, 100])
    dino_from_pkg = loader.load_dataset('dino')
    dino_from_file = loader.load_dataset(os.path.join(DATASETS_DIR, 'dino.csv'))

    assert dino_from_pkg[0] == dino_from_file[0]
    assert dino_from_pkg[1].equals(dino_from_file[1])
