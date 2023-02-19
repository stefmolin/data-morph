"""Utility functions for static plotting."""

import os
from typing import Union

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes

from ..data.stats import get_values
from .style import plot_with_custom_style


@plot_with_custom_style
def plot(
    df: pd.DataFrame, save_to: str, decimals: int, **save_kwds
) -> Union[Axes, None]:
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

    Returns
    -------
    matplotlib.axes.Axes or None
        When ``save_to`` is falsey, an Axes object is returned.
    """
    y_offset = -5
    fig, ax = plt.subplots(figsize=(12, 5), layout='constrained')
    ax.scatter(df.x, df.y, s=50, alpha=0.7, color='black')
    ax.set(xlim=(-5, 105), ylim=(y_offset, 105))

    res = get_values(df)

    locs = [80, 65, 50, 35, 20]
    labels = ('X Mean', 'Y Mean', 'X SD', 'Y SD', 'Corr.')
    max_label_length = max([len(label) for label in labels])

    # If `max_label_length = 10`, this string will be "{:<10}: {:0.7f}", then we
    # can pull the `.format` method for that string to reduce typing it
    # repeatedly
    visible_decimals = 7
    formatter = '{{:<{pad}}}: {{:0.{decimals}f}}'.format(
        pad=max_label_length, decimals=visible_decimals
    ).format
    corr_formatter = '{{:<{pad}}}: {{:+.{decimals}f}}'.format(
        pad=max_label_length, decimals=visible_decimals
    ).format
    stat_clip = visible_decimals - decimals

    for label, loc, stat in zip(labels[:-1], locs, res):
        ax.text(110, y_offset + loc, formatter(label, stat), fontsize=30, alpha=0.3)
        ax.text(110, y_offset + loc, formatter(label, stat)[:-stat_clip], fontsize=30)

    correlation_str = corr_formatter(labels[-1], res.correlation, pad=max_label_length)
    for alpha, text in zip([0.3, 1], [correlation_str, correlation_str[:-stat_clip]]):
        ax.text(
            110,
            y_offset + locs[-1],
            text,
            fontsize=30,
            alpha=alpha,
        )

    if not save_to:
        return ax

    dirname = os.path.dirname(save_to)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    fig.savefig(save_to, **save_kwds)
    plt.close(fig)
