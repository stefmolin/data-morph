"""Test the loader module."""

import pytest
from pandas.testing import assert_frame_equal

from data_morph.data.dataset import Dataset
from data_morph.data.loader import DataLoader


class TestDataLoader:
    """Test the DataLoader class."""

    def test_static_class(self):
        """Make sure DataLoader can't be instantiated."""
        with pytest.raises(NotImplementedError):
            _ = DataLoader()

    @pytest.mark.dataset
    @pytest.mark.parametrize(
        ['name', 'file'], [['dino', 'dino.csv'], ['sheep', 'sheep.csv']]
    )
    def test_load_dataset(self, name, file, starter_shapes_dir):
        """Confirm that loading the dataset by name and file works."""
        dataset_from_pkg = DataLoader.load_dataset(name)
        dataset_from_file = DataLoader.load_dataset(starter_shapes_dir / file)

        assert isinstance(dataset_from_pkg, Dataset)
        assert isinstance(dataset_from_file, Dataset)
        assert dataset_from_pkg.name == dataset_from_file.name
        assert_frame_equal(dataset_from_pkg.df, dataset_from_file.df)

    @pytest.mark.input_validation
    @pytest.mark.parametrize('dataset', ['does_not_exist', 'does_not_exist.csv'])
    def test_load_dataset_unknown_data(self, dataset):
        """Confirm that trying to load non-existent datasets raises an exception."""
        with pytest.raises(ValueError, match='Unknown dataset'):
            _ = DataLoader.load_dataset(dataset)
