"""Test the static module."""

import matplotlib.pyplot as plt
import numpy as np
import pytest

from data_morph.plotting.static import plot

pytestmark = pytest.mark.plotting


@pytest.mark.parametrize(
    ('file_path', 'with_median', 'classic'),
    [
        ('test_plot.png', False, True),
        (None, True, True),
        (None, False, True),
        (None, True, False),
        (None, False, False),
    ],
)
def test_plot(sample_data, tmp_path, file_path, with_median, classic):
    """Test static plot creation."""
    bounds = (-5.0, 105.0)

    marginals = (
        None if classic else (np.histogram(sample_data.x), np.histogram(sample_data.y))
    )

    if file_path:
        save_to = tmp_path / 'another-level' / file_path

        plot(
            data=sample_data,
            x_bounds=bounds,
            y_bounds=bounds,
            save_to=save_to,
            decimals=2,
            with_median=with_median,
            marginals=marginals,
        )
        assert save_to.is_file()

    else:
        ax = plot(
            data=sample_data,
            x_bounds=bounds,
            y_bounds=bounds,
            save_to=None,
            decimals=2,
            with_median=with_median,
            marginals=marginals,
        )

        # confirm that the stylesheet was used
        assert ax.texts[0].get_fontfamily() == ['monospace']

        # confirm that bounds are correct
        assert ax.get_xlim() == bounds
        assert ax.get_ylim() == bounds

        # confirm that the right number of stats was drawn
        expected_stats = 7 if with_median else 5
        expected_texts = 2 * expected_stats  # label and the number
        assert len(ax.texts) == expected_texts

        # if marginals should be there, check for two inset Axes
        expected_insets = 0 if classic else 2
        inset_axes = [
            child for child in ax.get_children() if isinstance(child, plt.Axes)
        ]
        assert len(inset_axes) == expected_insets
