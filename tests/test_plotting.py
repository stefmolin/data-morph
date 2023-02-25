"""Tests for the data_morph.plotting subpackage."""

import os

import numpy as np
import pytest

from data_morph.plotting.animation import stitch_gif_animation
from data_morph.plotting.static import plot


@pytest.mark.parametrize('file_path', ['test_plot.png', None])
def test_plot(sample_data, file_path):
    """Test static plot creation."""
    bounds = [-5, 105]
    if file_path:
        temp_dir = 'does-not-exist'
        save_to = os.path.join(temp_dir, file_path)

        plot(
            df=sample_data,
            x_bounds=bounds,
            y_bounds=bounds,
            save_to=save_to,
            decimals=2,
        )
        assert os.path.isfile(save_to)

        # clean up
        os.remove(save_to)
        os.rmdir(temp_dir)
    else:
        ax = plot(
            df=sample_data, x_bounds=bounds, y_bounds=bounds, save_to=None, decimals=2
        )

        # confirm that the stylesheet was used
        assert ax.texts[0].get_fontfamily() == ['monospace']


def test_frame_stitching(sample_data, tmpdir):
    """Test stitching frames into a GIF animation."""
    start_shape = 'sample'
    target_shape = 'circle'
    bounds = [-5, 105]

    for frame in range(10):
        plot(
            df=sample_data + np.random.randn(),
            x_bounds=bounds,
            y_bounds=bounds,
            save_to=os.path.join(
                tmpdir, f'{start_shape}-to-{target_shape}-{frame}.png'
            ),
            decimals=2,
        )

    stitch_gif_animation(
        output_dir=tmpdir,
        start_shape=start_shape,
        target_shape=target_shape,
        keep_frames=False,
        forward_only_animation=False,
    )

    animation_file = os.path.join(tmpdir, f'{start_shape}_to_{target_shape}.gif')
    assert os.path.isfile(animation_file)
    assert not os.path.isfile(
        os.path.join(tmpdir, f'{start_shape}-to-{target_shape}-{frame}.png')
    )
