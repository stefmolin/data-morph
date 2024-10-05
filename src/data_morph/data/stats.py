"""Utility functions for calculating summary statistics."""

from collections import namedtuple
from numbers import Number
from typing import Iterable

import numpy as np

SummaryStatistics = namedtuple(
    'SummaryStatistics', ['x_mean', 'y_mean', 'x_stdev', 'y_stdev', 'correlation']
)
SummaryStatistics.__doc__ = (
    'Named tuple containing the summary statistics for plotting/analysis.'
)


def get_values(x: Iterable[Number], y: Iterable[Number]) -> SummaryStatistics:
    """
    Calculate the summary statistics for the given set of points.

    Parameters
    ----------
    x : Iterable[Number]
        The ``x`` value of the dataset.

    y : Iterable[Number]
        The ``y`` value of the dataset.

    Returns
    -------
    SummaryStatistics
        Named tuple consisting of mean and standard deviations of x and y,
        along with the Pearson correlation coefficient between the two.
    """
    return SummaryStatistics(
        np.mean(x),
        np.mean(y),
        np.std(x, ddof=1),
        np.std(y, ddof=1),
        np.corrcoef(x, y)[0, 1],
    )
