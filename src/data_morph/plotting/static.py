"""Utility functions for static plotting."""

from __future__ import annotations

from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import EngFormatter

from ..data.stats import get_summary_statistics
from .style import plot_with_custom_style

if TYPE_CHECKING:
    from collections.abc import Iterable
    from numbers import Number

    import pandas as pd
    from matplotlib.axes import Axes

_STATISTIC_DISPLAY_NAME_MAPPING: dict[str, str] = {
    'x_mean': 'X Mean',
    'y_mean': 'Y Mean',
    'x_stdev': 'X SD',
    'y_stdev': 'Y SD',
    'x_median': 'X Med.',
    'y_median': 'Y Med.',
    'correlation': 'Corr.',
}


@plot_with_custom_style
def plot(
    data: pd.DataFrame,
    x_bounds: Iterable[Number],
    y_bounds: Iterable[Number],
    save_to: str | Path,
    decimals: int,
    with_median: bool,
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
    with_median : bool
        Whether to include the median.
    **save_kwds
        Additional keyword arguments that will be passed down to
        :meth:`matplotlib.figure.Figure.savefig`.

    Returns
    -------
    matplotlib.axes.Axes or None
        When ``save_to`` is falsey, an :class:`~matplotlib.axes.Axes` object is returned.
    """
    fig, ax = plt.subplots(
        figsize=(7, 3), layout='constrained', subplot_kw={'aspect': 'equal'}
    )
    fig.get_layout_engine().set(w_pad=1.4, h_pad=0.2, wspace=0)

    ax.scatter(data.x, data.y, s=1, alpha=0.7, color='black')
    ax.set(xlim=x_bounds, ylim=y_bounds)

    tick_formatter = EngFormatter()
    ax.xaxis.set_major_formatter(tick_formatter)
    ax.yaxis.set_major_formatter(tick_formatter)

    res = get_summary_statistics(data, with_median=with_median)

    if with_median:
        fields = (
            'x_mean',
            'x_median',
            'x_stdev',
            'y_mean',
            'y_median',
            'y_stdev',
            'correlation',
        )
        locs = [0.9, 0.78, 0.66, 0.5, 0.38, 0.26, 0.1]
    else:
        fields = ('x_mean', 'y_mean', 'x_stdev', 'y_stdev', 'correlation')
        locs = np.linspace(0.8, 0.2, num=len(fields))

    labels = [_STATISTIC_DISPLAY_NAME_MAPPING[field] for field in fields]
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
        1.05,
        fontsize=15,
        transform=ax.transAxes,
        va='center',
    )
    for loc, field in zip(locs, fields):
        label = _STATISTIC_DISPLAY_NAME_MAPPING[field]
        stat = getattr(res, field)

        if field == 'correlation':
            correlation_str = corr_formatter(labels[-1], res.correlation)
            for alpha, text in zip(
                [0.3, 1], [correlation_str, correlation_str[:-stat_clip]]
            ):
                add_stat_text(
                    locs[-1],
                    text,
                    alpha=alpha,
                )
        else:
            add_stat_text(loc, formatter(label, stat), alpha=0.3)
            add_stat_text(loc, formatter(label, stat)[:-stat_clip])

    if not save_to:
        return ax

    save_to = Path(save_to)
    dirname = save_to.parent
    if not dirname.is_dir():
        dirname.mkdir(parents=True, exist_ok=True)

    fig.savefig(save_to, bbox_inches='tight', **save_kwds)
    return plt.close(fig)
