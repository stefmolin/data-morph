"""Utility functions for animations."""

import glob
import os
from typing import Union

from PIL import Image

from ..shapes.bases.shape import Shape


def stitch_gif_animation(
    output_dir: str,
    start_shape: str,
    target_shape: Union[str, Shape],
    keep_frames: bool = False,
    forward_only_animation: bool = False,
) -> None:
    """
    Stitch frames together into a GIF animation.

    Parameters
    ----------
    output_dir : str
        The output directory to save the animation to.
    start_shape : str
        The starting shape.
    target_shape : str or Shape
        The target shape for the morphing.
    keep_frames : bool, default False
        Whether to keep the individual frames after creating the animation.
    forward_only_animation : bool, default False
        Whether to play the animation in the forward direction rather than
        animating in both forward and reverse.
    """
    # find the frames and sort them
    imgs = sorted(
        glob.glob(os.path.join(output_dir, f'{start_shape}-to-{target_shape}*.png'))
    )

    # add the final frame for a bit
    start_image = Image.open(imgs[0])
    frames = [start_image for _ in range(100)]

    for img in imgs:
        new_frame = Image.open(img)
        frames.append(new_frame)

    # add the final frame for a bit
    end_image = Image.open(imgs[-1])
    frames.extend([end_image for _ in range(50)])

    if not forward_only_animation:
        # add the animation in reverse
        frames.extend(frames[::-1])

    frames[0].save(
        os.path.join(output_dir, f'{start_shape}_to_{target_shape}.gif'),
        format='GIF',
        append_images=frames[1:],
        save_all=True,
        duration=5,
        loop=0,
    )

    if not keep_frames:
        # remove the image files
        for img in imgs:
            os.remove(img)
