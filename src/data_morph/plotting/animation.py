"""Utility functions for animations."""

from __future__ import annotations

import math
import re
from functools import wraps
from pathlib import Path
from typing import TYPE_CHECKING, Callable

from PIL import Image

if TYPE_CHECKING:
    from ..shapes.bases.shape import Shape


def stitch_gif_animation(
    output_dir: str | Path,
    start_shape: str,
    target_shape: str | Shape,
    frame_numbers: list[int],
    keep_frames: bool = False,
    forward_only_animation: bool = False,
) -> None:
    """
    Stitch frames together into a GIF animation.

    Parameters
    ----------
    output_dir : str or pathlib.Path
        The output directory to save the animation to. Note that the frames to
        stitch together must be in here as well.
    start_shape : str
        The starting shape.
    target_shape : str or Shape
        The target shape for the morphing.
    frame_numbers : list[int]
        The saved frames to use in the GIF. Repeated consecutive frames will be shown
        as a single frame for a longer duration (i.e., x repeats, means x times longer
        than the default duration of 5 milliseconds).
    keep_frames : bool, default ``False``
        Whether to keep the individual frames after creating the animation.
    forward_only_animation : bool, default ``False``
        Whether to only play the animation in the forward direction rather than
        animating in both forward and reverse.

    See Also
    --------
    PIL.Image
        Frames are stitched together with Pillow.
    """
    output_dir = Path(output_dir)
    iteration_pattern = re.compile(r'\d+')
    default_frame_duration = 5  # milliseconds

    # find the frames and sort them
    imgs = sorted(output_dir.glob(f'{start_shape}-to-{target_shape}*.png'))

    frames = []
    durations = []
    for img_file in imgs:
        iteration_number = int(iteration_pattern.search(img_file.stem).group(0))
        frames.append(Image.open(img_file))
        durations.append(frame_numbers.count(iteration_number) * default_frame_duration)

    if not forward_only_animation:
        # add the animation in reverse
        frames.extend(frames[::-1])
        durations.extend(durations[::-1])

    frames[0].save(
        output_dir / f'{start_shape}_to_{target_shape}.gif',
        format='GIF',
        append_images=frames[1:],
        save_all=True,
        duration=durations,
        loop=0,
    )

    if not keep_frames:
        # remove the image files
        for img in imgs:
            Path(img).unlink()


def check_step(
    easing_function: Callable[[int | float], int | float],
) -> Callable[[int | float], int | float]:
    """
    Decorator to check if the step is a float or int and if it is between 0 and 1.

    Parameters
    ----------
    easing_function : Callable
        The easing function to be checked.

    Returns
    -------
    Callable
        The easing function with the check for the step.
    """

    @wraps(easing_function)
    def wrapper(step: int | float) -> int | float:
        """
        Wrapper function to check the step.

        Parameters
        ----------
        step : int or float
            The current step of the animation, from 0 to 1.

        Returns
        -------
        int or float
            The eased value at the current step, from 0.0 to 1.0.
        """
        if not (isinstance(step, (int, float)) and 0 <= step <= 1):
            raise ValueError('Step must be an integer or float, between 0 and 1.')
        return easing_function(step)

    return wrapper


@check_step
def ease_in_sine(step: int | float) -> float:
    """
    An ease-in sinusoidal function to generate animation steps (slow to fast).

    Parameters
    ----------
    step : int or float
        The current step of the animation, from 0 to 1.

    Returns
    -------
    float
        The eased value at the current step, from 0.0 to 1.0.
    """
    return -1 * math.cos(step * math.pi / 2) + 1


@check_step
def ease_out_sine(step: int | float) -> float:
    """
    An ease-out sinusoidal function to generate animation steps (fast to slow).

    Parameters
    ----------
    step : int or float
        The current step of the animation, from 0 to 1.

    Returns
    -------
    float
        The eased value at the current step, from 0.0 to 1.0.
    """
    return math.sin(step * math.pi / 2)


@check_step
def ease_in_out_sine(step: int | float) -> float:
    """
    An ease-in and ease-out sinusoidal function to generate animation steps (slow to fast to slow).

    Parameters
    ----------
    step : int or float
        The current step of the animation, from 0 to 1.

    Returns
    -------
    float
        The eased value at the current step, from 0.0 to 1.0.
    """
    return -0.5 * (math.cos(math.pi * step) - 1)


@check_step
def ease_in_out_quadratic(step: int | float) -> int | float:
    """
    An ease-in and ease-out quadratic function to generate animation steps (slow to fast to slow).

    Parameters
    ----------
    step : int or float
        The current step of the animation, from 0 to 1.

    Returns
    -------
    int or float
        The eased value at the current step, from 0.0 to 1.0.
    """
    if step < 0.5:
        return 2 * step**2
    step = step * 2 - 1
    return -0.5 * (step * (step - 2) - 1)


@check_step
def linear(step: int | float) -> int | float:
    """
    A linear function to generate animation steps.

    Parameters
    ----------
    step : int or float
        The current step of the animation, from 0 to 1.

    Returns
    -------
    int or float
        The eased value at the current step, from 0.0 to 1.0.
    """
    return step
