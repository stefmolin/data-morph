"""Utility functions for static plotting."""

import os

import matplotlib.pyplot as plt
import pandas as pd

from ..data.stats import get_values
from .style import plot_with_custom_style


@plot_with_custom_style
def plot(df: pd.DataFrame, save_to: str, decimals: int, **save_kwds) -> None:
    """
    Plot the dataset and summary statistics.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataset to plot.
    save_to : str
        Path to save the plot frame to.
    decimals : int
        The number of integers to highlight as preserved.
    **save_kwds
        Additional keyword arguments that will be passed down to
        :meth:`matplotlib.figure.Figure.savefig`.
    """
    y_offset = 0
    fig, ax = plt.subplots(figsize=(12, 5), layout='constrained')
    ax.scatter(df.x, df.y, s=50, alpha=0.7, color='black')
    ax.set(xlim=(0, 105), ylim=(y_offset, 105))

    res = get_values(df)
    fs = 30

    labels = ('X Mean', 'Y Mean', 'X SD', 'Y SD', 'Corr.')
    max_label_length = max([len(label) for label in labels])

    # If `max_label_length = 10`, this string will be "{:<10}: {:0.7f}", then we
    # can pull the `.format` method for that string to reduce typing it
    # repeatedly
    formatter = '{{:<{pad}}}: {{:0.7f}}'.format(pad=max_label_length).format
    corr_formatter = '{{:<{pad}}}: {{:+.7f}}'.format(pad=max_label_length).format
    stat_clip = 7 - decimals

    opts = dict(fontsize=fs, alpha=0.3)
    ax.text(110, y_offset + 80, formatter(labels[0], res.x_mean), **opts)
    ax.text(110, y_offset + 65, formatter(labels[1], res.y_mean), **opts)
    ax.text(110, y_offset + 50, formatter(labels[2], res.x_stdev), **opts)
    ax.text(110, y_offset + 35, formatter(labels[3], res.y_stdev), **opts)
    ax.text(
        110,
        y_offset + 20,
        corr_formatter(labels[4], res.correlation, pad=max_label_length),
        **opts,
    )

    opts['alpha'] = 1
    ax.text(110, y_offset + 80, formatter(labels[0], res.x_mean)[:-stat_clip], **opts)
    ax.text(110, y_offset + 65, formatter(labels[1], res.y_mean)[:-stat_clip], **opts)
    ax.text(110, y_offset + 50, formatter(labels[2], res.x_stdev)[:-stat_clip], **opts)
    ax.text(110, y_offset + 35, formatter(labels[3], res.y_stdev)[:-stat_clip], **opts)
    ax.text(
        110,
        y_offset + 20,
        corr_formatter(labels[4], res.correlation, pad=max_label_length)[:-stat_clip],
        **opts,
    )

    if not save_to:
        return ax

    dirname = os.path.dirname(save_to)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    fig.savefig(save_to, **save_kwds)
    plt.close(fig)
