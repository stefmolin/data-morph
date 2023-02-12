"""Tests for the data_morph.plotting subpackage."""

import os

import pytest

from data_morph.plotting.static import plot


@pytest.fixture
def viz_dir():
    """A fixture to allow creation of a new directory, with cleanup."""
    temp_dir = 'temp'
    yield temp_dir

    try:
        os.rmdir(temp_dir)
    except FileNotFoundError:  # we only need to delete if this is accessed
        pass


@pytest.mark.parametrize('file_path', ['test_plot.png', None])
def test_plot(sample_data, viz_dir, file_path):
    """Test static plot creation."""
    if file_path:
        save_to = os.path.join(viz_dir, file_path)
        plot(df=sample_data, save_to=save_to, decimals=2)
        os.remove(save_to)
    else:
        ax = plot(df=sample_data, save_to=None, decimals=2)

        # confirm that the stylesheet was used
        assert ax.texts[0].get_fontfamily() == ['monospace']
