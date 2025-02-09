"""Utility functions for calculating summary statistics."""

from collections import namedtuple

import pandas as pd

SummaryStatistics = namedtuple(
    'SummaryStatistics', ['x_mean', 'y_mean', 'x_stdev', 'y_stdev', 'correlation']
)
SummaryStatistics.__doc__ = (
    'Named tuple containing the summary statistics for plotting/analysis.'
)


def get_summary_statistics(data: pd.DataFrame) -> SummaryStatistics:
    """
    Calculate the summary statistics for the given set of points.

    Parameters
    ----------
    data : pandas.DataFrame
        A dataset with columns x and y.

    Returns
    -------
    SummaryStatistics
        Named tuple consisting of mean and standard deviations of x and y,
        along with the Pearson correlation coefficient between the two.
    """
    return SummaryStatistics(
        data.x.mean(),
        data.y.mean(),
        data.x.std(),
        data.y.std(),
        data.corr().x.y,
    )
