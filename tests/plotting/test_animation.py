"""Test the animation module."""

import numpy as np
import pytest

from data_morph.plotting.animation import stitch_gif_animation
from data_morph.plotting.static import plot

pytestmark = pytest.mark.plotting


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
