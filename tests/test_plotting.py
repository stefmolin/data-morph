"""Tests for the data_morph.plotting subpackage."""

import os

import numpy as np
import pytest

from data_morph.plotting.animation import stitch_gif_animation
from data_morph.plotting.static import plot


@pytest.fixture
def viz_dir():
    """A fixture to allow creation of a new directory, with cleanup."""
    temp_dir = os.path.join('tests', 'plots')
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


def test_frame_stitching(sample_data, viz_dir):
    """Test stitching frames into a GIF animation."""
    start_shape = 'sample'
    target_shape = 'circle'

    for frame in range(10):
        plot(
            df=sample_data + np.random.randn(),
            save_to=os.path.join(
                viz_dir, f'{start_shape}-to-{target_shape}-{frame}.png'
            ),
            decimals=2,
        )

    stitch_gif_animation(
        output_dir=viz_dir,
        start_shape=start_shape,
        target_shape=target_shape,
        keep_frames=False,
        forward_only_animation=False,
    )

    animation_file = os.path.join(viz_dir, f'{start_shape}_to_{target_shape}.gif')
    assert os.path.isfile(animation_file)
    os.remove(animation_file)
