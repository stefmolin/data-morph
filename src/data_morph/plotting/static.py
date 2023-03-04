"""Utility functions for static plotting."""

import os
from functools import partial
from numbers import Number
from typing import Iterable, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes

from ..data.stats import get_values
from .style import plot_with_custom_style


@plot_with_custom_style
def plot(
    df: pd.DataFrame,
    x_bounds: Iterable[Number],
    y_bounds: Iterable[Number],
    save_to: str,
    decimals: int,
    **save_kwds,
) -> Union[Axes, None]:
    """
    Plot the dataset and summary statistics.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataset to plot.
    x_bounds, y_bounds : Iterable[Number]
        The plotting limits.
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
    fig, ax = plt.subplots(figsize=(12, 5), layout='constrained')
    fig.get_layout_engine().set(w_pad=0.2, h_pad=0.2)

    ax.scatter(df.x, df.y, s=50, alpha=0.7, color='black')
    ax.set(xlim=x_bounds, ylim=y_bounds)

    res = get_values(df)

    labels = ('X Mean', 'Y Mean', 'X SD', 'Y SD', 'Corr.')
    locs = np.linspace(0.8, 0.2, num=len(labels))
    max_label_length = max([len(label) for label in labels])
    max_stat = int(np.log10(np.max(np.abs(res)))) + 1

    # If `max_label_length = 10`, this string will be "{:<10}: {:0.7f}", then we
    # can pull the `.format` method for that string to reduce typing it
    # repeatedly
    visible_decimals = 7
    formatter = '{{:<{pad}}}: {{:+{stat_pad}.{decimals}f}}'.format(
        pad=max_label_length,
        stat_pad=max_stat + visible_decimals + 2,
        decimals=visible_decimals,
    ).format
    corr_formatter = '{{:<{pad}}}: {{:+{corr_pad}.{decimals}f}}'.format(
        pad=max_label_length,
        corr_pad=max_stat + visible_decimals + 2,
        decimals=visible_decimals,
    ).format
    stat_clip = visible_decimals - decimals

    add_stat_text = partial(
        ax.text,
        1.03,
        fontsize=30,
        transform=ax.transAxes,
        va='center',
    )
    for label, loc, stat in zip(labels[:-1], locs, res):
        add_stat_text(loc, formatter(label, stat), alpha=0.3)
        add_stat_text(loc, formatter(label, stat)[:-stat_clip])

    correlation_str = corr_formatter(labels[-1], res.correlation)
    for alpha, text in zip([0.3, 1], [correlation_str, correlation_str[:-stat_clip]]):
        add_stat_text(
            locs[-1],
            text,
            alpha=alpha,
        )

    if not save_to:
        return ax

    dirname = os.path.dirname(save_to)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    fig.savefig(save_to, **save_kwds)
    plt.close(fig)
