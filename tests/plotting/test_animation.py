"""Test the animation module."""

from contextlib import suppress

import numpy as np
import pytest
from PIL import Image

from data_morph.plotting import animation
from data_morph.plotting.animation import stitch_gif_animation
from data_morph.plotting.static import plot

pytestmark = pytest.mark.plotting


@pytest.mark.parametrize('forward_only', [True, False])
def test_frame_stitching(sample_data, tmp_path, forward_only):
    """Test stitching frames into a GIF animation."""
    start_shape = 'sample'
    target_shape = 'circle'
    bounds = [-5, 105]
    frame_numbers = list(range(10))
    rng = np.random.default_rng()

    for frame in frame_numbers:
        plot(
            data=sample_data + rng.standard_normal(),
            x_bounds=bounds,
            y_bounds=bounds,
            save_to=(tmp_path / f'{start_shape}-to-{target_shape}-{frame}.png'),
            decimals=2,
        )

    duration_multipliers = [0, 0, 0, 0, 1, 1, *frame_numbers[2:], frame_numbers[-1]]
    stitch_gif_animation(
        output_dir=tmp_path,
        start_shape=start_shape,
        target_shape=target_shape,
        frame_numbers=duration_multipliers,
        keep_frames=False,
        forward_only_animation=forward_only,
    )

    animation_file = tmp_path / f'{start_shape}_to_{target_shape}.gif'
    assert animation_file.is_file()
    assert not (tmp_path / f'{start_shape}-to-{target_shape}-{frame}.png').is_file()

    with Image.open(animation_file) as img:
        # we subtract one when playing in reverse as well because the middle frame (last
        # in the forward direction) is combined into a single frame with the start of the
        # reversal as part of PIL's optimization
        assert img.n_frames == (
            len(frame_numbers) if forward_only else len(frame_numbers) * 2 - 1
        )
        for frame in range(len(frame_numbers)):
            with suppress(KeyError):
                # if we play in reverse, the midpoint will have double duration since
                # those two frames are combined
                rewind_multiplier = (
                    2 if not forward_only and frame == len(frame_numbers) - 1 else 1
                )
                # duration only seems to be present on frames where it is different
                if frame_duration := img.info['duration']:
                    assert (
                        frame_duration
                        == duration_multipliers.count(frame) * 5 * rewind_multiplier
                    )
            with suppress(EOFError):
                # move to the next frame
                img.seek(img.tell() + 1)


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
