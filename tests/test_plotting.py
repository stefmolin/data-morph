"""Tests for the data_morph.plotting subpackage."""

import numpy as np
import pytest

from data_morph.plotting.animation import stitch_gif_animation
from data_morph.plotting.static import plot


@pytest.mark.parametrize('file_path', ['test_plot.png', None])
def test_plot(sample_data, tmp_path, file_path):
    """Test static plot creation."""
    bounds = (-5.0, 105.0)
    if file_path:
        save_to = tmp_path / 'another-level' / file_path

        plot(
            df=sample_data,
            x_bounds=bounds,
            y_bounds=bounds,
            save_to=save_to,
            decimals=2,
        )
        assert save_to.is_file()

    else:
        ax = plot(
            df=sample_data, x_bounds=bounds, y_bounds=bounds, save_to=None, decimals=2
        )

        # confirm that the stylesheet was used
        assert ax.texts[0].get_fontfamily() == ['monospace']

        # confirm that bounds are correct
        assert ax.get_xlim() == bounds
        assert ax.get_ylim() == bounds


def test_frame_stitching(sample_data, tmp_path):
    """Test stitching frames into a GIF animation."""
    start_shape = 'sample'
    target_shape = 'circle'
    bounds = [-5, 105]

    for frame in range(10):
        plot(
            df=sample_data + np.random.randn(),
            x_bounds=bounds,
            y_bounds=bounds,
            save_to=(tmp_path / f'{start_shape}-to-{target_shape}-{frame}.png'),
            decimals=2,
        )

    stitch_gif_animation(
        output_dir=tmp_path,
        start_shape=start_shape,
        target_shape=target_shape,
        keep_frames=False,
        forward_only_animation=False,
    )

    animation_file = tmp_path / f'{start_shape}_to_{target_shape}.gif'
    assert animation_file.is_file()
    assert not (tmp_path / f'{start_shape}-to-{target_shape}-{frame}.png').is_file()
