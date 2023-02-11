"""Utility functions for calculating summary statistics."""

from collections import namedtuple

import pandas as pd

SummmaryStatistics = namedtuple(
    'SummmaryStatistics', ['x_mean', 'y_mean', 'x_stdev', 'y_stdev', 'correlation']
)


def get_values(df: pd.DataFrame) -> SummmaryStatistics:
    """
    Calculate the summary statistics for the given set of points.

    Parameters
    ----------
    df : pd.DataFrame
        A dataset with columns x and y.

    Returns
    -------
    SummmaryStatistics
        Named tuple consisting of mean and standard deviations of x and y,
        along with the Pearson correlation coefficient between the two.
    """
    return SummmaryStatistics(
        df.x.mean(),
        df.y.mean(),
        df.x.std(),
        df.y.std(),
        df.corr().x.y,
    )
