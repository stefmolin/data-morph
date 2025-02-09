"""Test the static module."""

import pytest

from data_morph.plotting.static import plot

pytestmark = pytest.mark.plotting


@pytest.mark.parametrize('file_path', ['test_plot.png', None])
def test_plot(sample_data, tmp_path, file_path):
    """Test static plot creation."""
    bounds = (-5.0, 105.0)
    if file_path:
        save_to = tmp_path / 'another-level' / file_path

        plot(
            data=sample_data,
            x_bounds=bounds,
            y_bounds=bounds,
            save_to=save_to,
            decimals=2,
        )
        assert save_to.is_file()

    else:
        ax = plot(
            data=sample_data, x_bounds=bounds, y_bounds=bounds, save_to=None, decimals=2
        )

        # confirm that the stylesheet was used
        assert ax.texts[0].get_fontfamily() == ['monospace']

        # confirm that bounds are correct
        assert ax.get_xlim() == bounds
        assert ax.get_ylim() == bounds
