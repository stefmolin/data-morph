"""Utility functions for calculating summary statistics."""

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from collections.abc import Generator

    import pandas as pd


class SummaryStatistics(NamedTuple):
    """Named tuple containing the summary statistics for plotting/analysis."""

    x_mean: float
    y_mean: float

    x_stdev: float
    y_stdev: float

    correlation: float

    x_median: float | None
    y_median: float | None

    def __iter__(self) -> Generator[float, None, None]:
        for statistic in self._fields:
            if (value := getattr(self, statistic)) is not None:
                yield value


def get_summary_statistics(data: pd.DataFrame, with_median: bool) -> SummaryStatistics:
    """
    Calculate the summary statistics for the given set of points.

    Parameters
    ----------
    data : pandas.DataFrame
        A dataset with columns ``x`` and ``y``.
    with_median : bool
        Whether to include the median of ``x`` and ``y``.

    Returns
    -------
    SummaryStatistics
        Named tuple consisting of mean and standard deviations of ``x`` and ``y``,
        along with the Pearson correlation coefficient between the two, and optionally,
        the median of ``x`` and ``y``.
    """
    return SummaryStatistics(
        x_mean=data.x.mean(),
        y_mean=data.y.mean(),
        x_stdev=data.x.std(),
        y_stdev=data.y.std(),
        correlation=data.corr().x.y,
        x_median=data.x.median() if with_median else None,
        y_median=data.y.median() if with_median else None,
    )
