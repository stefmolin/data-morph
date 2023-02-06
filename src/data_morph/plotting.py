"""Utility functions for plotting and animating."""

from functools import wraps
import glob
from importlib.resources import files, as_file
import os

import matplotlib.pyplot as plt
from PIL import Image

from . import MAIN_DIR
from .stats import get_values


# TODO: docstrings

def plot_with_custom_style(plotting_function):
    @wraps(plotting_function)
    def plot_in_style(*args, **kwargs):
        style = files(MAIN_DIR).joinpath('config/plot_style.mplstyle')
        with as_file(style) as style_path:
            with plt.style.context(style_path):
                output = plotting_function(*args, **kwargs)
        return output
    return plot_in_style

@plot_with_custom_style
def plot(df, save_to, **save_kwds):
    """Creates a plot which shows both the plot and the statistical summary

    Args:
        df (pd.DataFrame):  The data set to plot
    """
    y_offset = 0
    fig, ax = plt.subplots(figsize=(12, 5), layout='constrained')
    ax.scatter(df.x, df.y, s=50, alpha=0.7, color='black')
    ax.set(xlim=(0, 105), ylim=(y_offset, 105))

    res = get_values(df)
    fs = 30

    labels = ('X Mean', 'Y Mean', 'X SD', 'Y SD', 'Corr.')
    max_label_length = max([len(l) for l in labels])

    # If `max_label_length = 10`, this string will be "{:<10}: {:0.9f}", then we
    # can pull the `.format` method for that string to reduce typing it
    # repeatedly
    formatter = '{{:<{pad}}}: {{:0.9f}}'.format(pad=max_label_length).format
    corr_formatter = '{{:<{pad}}}: {{:+.9f}}'.format(pad=max_label_length).format

    opts = dict(fontsize=fs, alpha=0.3)
    ax.text(110, y_offset + 80, formatter(labels[0], res[0])[:-2], **opts)
    ax.text(110, y_offset + 65, formatter(labels[1], res[1])[:-2], **opts)
    ax.text(110, y_offset + 50, formatter(labels[2], res[2])[:-2], **opts)
    ax.text(110, y_offset + 35, formatter(labels[3], res[3])[:-2], **opts)
    ax.text(110, y_offset + 20, corr_formatter(labels[4], res[4], pad=max_label_length)[:-2], **opts)

    opts['alpha'] = 1
    ax.text(110, y_offset + 80, formatter(labels[0], res[0])[:-7], **opts)
    ax.text(110, y_offset + 65, formatter(labels[1], res[1])[:-7], **opts)
    ax.text(110, y_offset + 50, formatter(labels[2], res[2])[:-7], **opts)
    ax.text(110, y_offset + 35, formatter(labels[3], res[3])[:-7], **opts)
    ax.text(110, y_offset + 20, corr_formatter(labels[4], res[4], pad=max_label_length)[:-7], **opts)

    if not save_to:
        return ax

    dirname = os.path.dirname(save_to)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    fig.savefig(save_to, **save_kwds)
    plt.close(fig)

def stitch_gif_animation(output_dir, start_shape, target_shape, keep_frames=False, forward_only_animation=False):
    # find the frames and sort them
    imgs = sorted(glob.glob(os.path.join(output_dir, f'{start_shape}-to-{target_shape}*.png')))
    
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
        loop=0
    )

    if not keep_frames:
        # remove the image files
        for img in imgs:
            os.remove(img)
