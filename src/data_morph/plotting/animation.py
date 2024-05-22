"""Utility functions for animations."""

import glob
import math
from pathlib import Path
from typing import Union

from PIL import Image

from ..shapes.bases.shape import Shape


def stitch_gif_animation(
    output_dir: Union[str, Path],
    start_shape: str,
    target_shape: Union[str, Shape],
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

    # find the frames and sort them
    imgs = sorted(glob.glob(str(output_dir / f'{start_shape}-to-{target_shape}*.png')))

    frames = [Image.open(img) for img in imgs]

    if not forward_only_animation:
        # add the animation in reverse
        frames.extend(frames[::-1])

    frames[0].save(
        output_dir / f'{start_shape}_to_{target_shape}.gif',
        format='GIF',
        append_images=frames[1:],
        save_all=True,
        duration=5,
        loop=0,
    )

    if not keep_frames:
        # remove the image files
        for img in imgs:
            Path(img).unlink()


def ease_in_sine(n: Union[int, float]) -> float:
    """
    An ease-in sinusoidal function to generate animation steps (slow to fast).

    Parameters
    ----------
    n : int or float
        The time progress of the animation, from 0 to 1.

    Returns
    -------
    float
        The value progress, starting at 0.0 and ending at 1.0.
    """
    return -1 * math.cos(n * math.pi / 2) + 1


def ease_out_sine(n: Union[int, float]) -> float:
    """
    An ease-out sinusoidal function to generate animation steps (fast to slow).

    Parameters
    ----------
    n : int or float
        The time progress of the animation, from 0 to 1.

    Returns
    -------
    float
        The value progress, starting at 0.0 and ending at 1.0.
    """
    return math.sin(n * math.pi / 2)


def ease_in_out_sine(n: Union[int, float]) -> float:
    """
    An ease-in and ease-out sinusoidal function to generate animation steps (slow to fast to slow).

    Parameters
    ----------
    n : int or float
        The time progress of the animation, from 0 to 1.

    Returns
    -------
    float
        The value progress, starting at 0.0 and ending at 1.0.
    """
    return -0.5 * (math.cos(math.pi * n) - 1)


def ease_in_out_quadratic(n: Union[int, float]) -> Union[int, float]:
    """
    An ease-in and ease-out quadratic function to generate animation steps (slow to fast to slow).

    Parameters
    ----------
    n : int or float
        The time progress of the animation, from 0 to 1.

    Returns
    -------
    int or float
        The value progress, starting at 0.0 and ending at 1.0.
    """
    if n < 0.5:
        return 2 * n**2
    else:
        n = n * 2 - 1
        return -0.5 * (n * (n - 2) - 1)


def linear(n: Union[int, float]) -> Union[int, float]:
    """
    A linear function to generate animation steps.

    Parameters
    ----------
    n : int or float
        The time progress of the animation, from 0 to 1.

    Returns
    -------
    int or float
        The value progress, starting at 0.0 and ending at 1.0.
    """
    return n
