"""Test the static module."""

import pytest

from data_morph.plotting.static import plot

pytestmark = pytest.mark.plotting


@pytest.mark.parametrize(
    ('file_path', 'with_median'),
    [
        ('test_plot.png', False),
        (None, True),
        (None, False),
    ],
)
def test_plot(sample_data, tmp_path, file_path, with_median):
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
            with_median=with_median,
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
