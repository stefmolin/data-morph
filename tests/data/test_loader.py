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
        ('name', 'file'), [('dino', 'dino.csv'), ('sheep', 'sheep.csv')]
    )
    def test_load_dataset(self, name, file, starter_shapes_dir):
        """Confirm that loading the dataset by name and file works."""
        dataset_from_pkg = DataLoader.load_dataset(name)
        dataset_from_file = DataLoader.load_dataset(starter_shapes_dir / file)

        assert isinstance(dataset_from_pkg, Dataset)
        assert isinstance(dataset_from_file, Dataset)
        assert dataset_from_pkg.name == dataset_from_file.name
        assert_frame_equal(dataset_from_pkg.data, dataset_from_file.data)

    @pytest.mark.input_validation
    @pytest.mark.parametrize('dataset', ['does_not_exist', 'does_not_exist.csv'])
    def test_load_dataset_unknown_data(self, dataset):
        """Confirm that trying to load non-existent datasets raises an exception."""
        with pytest.raises(ValueError, match='Unknown dataset'):
            _ = DataLoader.load_dataset(dataset)

    @pytest.mark.parametrize(
        ('provided_name', 'expected_name'),
        [('python', 'Python'), ('Python', 'Python'), ('sds', 'SDS'), ('SDS', 'SDS')],
    )
    def test_load_dataset_proper_nouns(self, provided_name, expected_name):
        """
        Confirm that datasets with names that are proper nouns and abbreviations
        are being handled properly.
        """
        assert DataLoader.load_dataset(provided_name).name == expected_name

    @pytest.mark.parametrize('subset', [2, 3, 5, None])
    def test_plot_available_datasets(self, monkeypatch, subset):
        """Test the plot_available_datasets() method."""
        if subset:
            monkeypatch.setattr(
                DataLoader,
                'AVAILABLE_DATASETS',
                DataLoader.AVAILABLE_DATASETS[:subset],
            )

        axs = DataLoader.plot_available_datasets()
        if subset is None or subset > 3:
            assert len(axs) > 1
        else:
            assert len(axs) == axs.size

        populated_axs = [ax for ax in axs.flatten() if ax.get_figure()]
        assert len(populated_axs) == len(DataLoader.AVAILABLE_DATASETS)
        assert all(ax.get_xlabel() == ax.get_ylabel() == '' for ax in populated_axs)

        for dataset, ax in zip(DataLoader.AVAILABLE_DATASETS, populated_axs):
            subplot_title = ax.get_title()
            assert subplot_title.startswith(dataset)
            assert subplot_title.endswith(' points)')
            if dataset in ['Python', 'SDS']:
                assert 'logo' in subplot_title
            assert ax.get_aspect() == 1
