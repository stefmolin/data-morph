"""Utility functions for static plotting."""

from __future__ import annotations

from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import EngFormatter, MaxNLocator

from ..data.stats import get_summary_statistics
from .style import plot_with_custom_style

if TYPE_CHECKING:
    from collections.abc import Iterable
    from numbers import Number

    import pandas as pd
    from matplotlib.axes import Axes


@plot_with_custom_style
def plot(
    data: pd.DataFrame,
    x_bounds: Iterable[Number],
    y_bounds: Iterable[Number],
    x_marginal,
    y_marginal,
    save_to: str | Path,
    decimals: int,
    **save_kwds: Any,  # noqa: ANN401
) -> Axes | None:
    """
    Plot the dataset and summary statistics.

    Parameters
    ----------
    data : pandas.DataFrame
        The dataset to plot.
    x_bounds, y_bounds : Iterable[numbers.Number]
        The plotting limits.
    save_to : str or pathlib.Path
        Path to save the plot frame to.
    decimals : int
        The number of integers to highlight as preserved.
    **save_kwds
        Additional keyword arguments that will be passed down to
        :meth:`matplotlib.figure.Figure.savefig`.

    Returns
    -------
    matplotlib.axes.Axes or None
        When ``save_to`` is falsey, an :class:`~matplotlib.axes.Axes` object is returned.
    """
    fig, ax = plt.subplots(
        figsize=(9, 3), layout='constrained', subplot_kw={'aspect': 'equal'}
    )
    fig.get_layout_engine().set(w_pad=1.4, h_pad=0.2, wspace=0)

    ax.scatter(data.x, data.y, s=1, alpha=0.7, color='black')
    ax.set(xlim=x_bounds, ylim=y_bounds)

    ax_histx = ax.inset_axes([0, 1.05, 1, 0.25], sharex=ax)
    ax_histy = ax.inset_axes([1.05, 0, 0.25, 1], sharey=ax)

    x_marginal_counts, x_marginal_bins = x_marginal
    y_marginal_counts, y_marginal_bins = y_marginal

    ax_histx.set(xlim=x_bounds, ylim=(0, np.ceil(x_marginal_counts.max() * 2)))
    ax_histy.set(xlim=(0, np.ceil(y_marginal_counts.max() * 2)), ylim=y_bounds)

    # no labels on marginal axis that shares with scatter plot
    ax_histx.tick_params(axis='x', labelbottom=False)
    ax_histy.tick_params(axis='y', labelleft=False)

    # move marginal axis ticks that are visible to the corner and only show the non-zero label
    locator = MaxNLocator(2, integer=True, prune='lower')
    ax_histx.tick_params(axis='y', labelleft=False, labelright=True)
    ax_histx.yaxis.set_major_locator(locator)
    ax_histy.tick_params(axis='x', labelbottom=False, labeltop=True)
    ax_histy.xaxis.set_major_locator(locator)

    ax_histx.hist(data.x, bins=x_marginal_bins, color='gray', ec='black')
    ax_histy.hist(
        data.y, bins=y_marginal_bins, orientation='horizontal', color='gray', ec='black'
    )

    tick_formatter = EngFormatter()
    ax.xaxis.set_major_formatter(tick_formatter)
    ax_histy.xaxis.set_major_formatter(tick_formatter)
    ax.yaxis.set_major_formatter(tick_formatter)
    ax_histx.yaxis.set_major_formatter(tick_formatter)

    res = get_summary_statistics(data)

    labels = ('X Mean', 'Y Mean', 'X SD', 'Y SD', 'Corr.')
    locs = np.linspace(1.15, 0.1, num=len(labels))
    max_label_length = max([len(label) for label in labels])
    max_stat = int(np.log10(np.max(np.abs(res)))) + 1
    mean_x_digits, mean_y_digits = (
        int(x) + 1 for x in np.log10(np.abs([res.x_mean, res.y_mean]))
    )

    # If `max_label_length = 10`, this string will be "{:<10}: {:0.7f}", then we
    # can pull the `.format` method for that string to reduce typing it
    # repeatedly
    visible_decimals = 7
    offset = (
        2
        if (res.x_mean < 0 and mean_x_digits >= max_stat)
        or (res.y_mean < 0 and mean_y_digits >= max_stat)
        else 1
    )
    formatter = f'{{:<{max_label_length}}}: {{:{max_stat + visible_decimals + offset}.{visible_decimals}f}}'.format
    corr_formatter = f'{{:<{max_label_length}}}: {{:+{max_stat + visible_decimals + offset}.{visible_decimals}f}}'.format
    stat_clip = visible_decimals - decimals

    add_stat_text = partial(
        ax.text,
        1.4,
        fontsize=15,
        transform=ax.transAxes,
        va='center',
    )
    for label, loc, stat in zip(labels[:-1], locs, res, strict=False):
        add_stat_text(loc, formatter(label, stat), alpha=0.3)
        add_stat_text(loc, formatter(label, stat)[:-stat_clip])

    correlation_str = corr_formatter(labels[-1], res.correlation)
    for alpha, text in zip(
        [0.3, 1], [correlation_str, correlation_str[:-stat_clip]], strict=False
    ):
        add_stat_text(
            locs[-1],
            text,
            alpha=alpha,
        )

    if not save_to:
        return ax

    save_to = Path(save_to)
    dirname = save_to.parent
    if not dirname.is_dir():
        dirname.mkdir(parents=True, exist_ok=True)

    fig.savefig(save_to, bbox_inches='tight', **save_kwds)
    return plt.close(fig)
