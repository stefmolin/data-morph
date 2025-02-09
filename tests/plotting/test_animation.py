"""Test the animation module."""

import numpy as np
import pytest

from data_morph.plotting import animation
from data_morph.plotting.animation import stitch_gif_animation
from data_morph.plotting.static import plot

pytestmark = pytest.mark.plotting


def test_frame_stitching(sample_data, tmp_path):
    """Test stitching frames into a GIF animation."""
    start_shape = 'sample'
    target_shape = 'circle'
    bounds = [-5, 105]
    rng = np.random.default_rng()

    for frame in range(10):
        plot(
            data=sample_data + rng.standard_normal(),
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


@pytest.mark.parametrize(
    ('ease_function', 'step', 'expected'),
    [
        ('linear', 0.1, 0.1),
        ('linear', 0.5, 0.5),
        ('linear', 0.9, 0.9),
        ('ease_in_sine', 0.1, 0.012312),
        ('ease_in_sine', 0.5, 0.292893),
        ('ease_in_sine', 0.9, 0.843566),
        ('ease_out_sine', 0.1, 0.156434),
        ('ease_out_sine', 0.5, 0.707107),
        ('ease_out_sine', 0.9, 0.987688),
        ('ease_in_out_sine', 0.1, 0.024472),
        ('ease_in_out_sine', 0.5, 0.5),
        ('ease_in_out_sine', 0.9, 0.975528),
        ('ease_in_out_quadratic', 0.1, 0.02),
        ('ease_in_out_quadratic', 0.5, 0.5),
        ('ease_in_out_quadratic', 0.9, 0.98),
    ],
)
def test_easing_functions(ease_function, step, expected):
    """Test that easing functions return expected values."""
    ease_func = getattr(animation, ease_function)
    assert round(ease_func(step), ndigits=6) == expected


@pytest.mark.parametrize(
    'invalid_step',
    [
        'string',
        -1,
        2,
    ],
)
@pytest.mark.parametrize(
    'ease_function',
    [
        'linear',
        'ease_in_sine',
        'ease_out_sine',
        'ease_in_out_sine',
        'ease_in_out_quadratic',
    ],
)
def test_invalid_easing_step(ease_function, invalid_step):
    """Test that an invalid step type will produce a ValueError when passed to an easing function."""
    ease_func = getattr(animation, ease_function)

    with pytest.raises(
        ValueError, match='Step must be an integer or float, between 0 and 1.'
    ):
        ease_func(invalid_step)
