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


def shifted_mean(
    mean_old: float,
    value_old: float,
    value_new: float,
    size: int,
) -> float:
    """
    Return the shifted mean from the perturbed data.
    """
    return (mean_old - value_old / size) + value_new / size


def shifted_var(
    mean_old: float,
    var_old: float,
    value_old: float,
    value_new: float,
    size: int,
    *,
    ddof: int = 0,
) -> float:
    """
    Return the shifted covariance from the perturbed data.
    """
    return (
        var_old
        + 2 * (value_new - value_old) * (value_old - mean_old) / (size - ddof)
        + (value_new - value_old) ** 2 * (1 / (size - ddof) - 1 / (size - ddof) / size)
    )


def shifted_stdev(*args, **kwargs):
    return np.sqrt(shifted_var(*args, **kwargs))


def shifted_corrcoef(
    x_old: float,
    y_old: float,
    x_new: float,
    y_new: float,
    meanx_old: float,  # the mean <x>
    meany_old: float,  # the mean <y>
    xy_old: float,  # the mean <xy>
    varx_old: float,  # the variance <x^2> - <x>^2
    vary_old: float,  # the variance <y^2> - <y>^2
    size: int,
) -> float:
    """
    Return the shifted correlation coefficient of the perturbed data.
    """
    deltax = x_new - x_old
    deltay = y_new - y_old

    numerator = (
        xy_old
        + (deltax * y_old + deltay * x_old + deltax * deltay) / size
        - shifted_mean(mean_old=meanx_old, value_old=x_old, value_new=x_new, size=size)
        * shifted_mean(mean_old=meany_old, value_old=y_old, value_new=y_new, size=size)
    )

    denominator = np.sqrt(
        shifted_var(
            mean_old=meanx_old,
            var_old=varx_old,
            value_old=x_old,
            value_new=x_new,
            size=size,
        )
        * shifted_var(
            mean_old=meany_old,
            var_old=vary_old,
            value_old=y_old,
            value_new=y_new,
            size=size,
        )
    )

    return numerator / denominator


class Statistics:
    def __init__(self, x: Iterable[Number], y: Iterable[Number]):
        if len(x) != len(y):
            raise ValueError('The two datasets should have the same size')

        self._x = np.copy(x)
        self._y = np.copy(y)
        self._size = len(self._x)
        self._x_mean = np.mean(self._x)
        self._y_mean = np.mean(self._y)
        self._x_var = np.var(self._x, ddof=0)
        self._x_stdev = np.sqrt(self._x_var)
        self._y_var = np.var(self._y, ddof=0)
        self._y_stdev = np.sqrt(self._y_var)
        self._corrcoef = np.corrcoef(self._x, self._y)[0, 1]
        self._xy_mean = np.mean(self._x * self._y)

    @property
    def x_mean(self):
        """
        Return the mean of the ``x`` data.
        """
        return self._x_mean

    @property
    def y_mean(self):
        """
        Return the mean of the ``y`` data.
        """
        return self._y_mean

    @property
    def x_stdev(self):
        """
        Return the std of the ``x`` data.
        """
        return self._x_stdev

    @property
    def y_stdev(self):
        """
        Return the std of the ``y`` data.
        """
        return self._y_stdev

    @property
    def corrcoef(self):
        """
        Return the correlation coefficient of the ``x`` and ``y`` data.
        """
        return self._corrcoef

    def __len__(self):
        """
        Return the size of the dataset.
        """
        return len(self._x)

    def perturb(
        self,
        index: int,
        deltax: float,
        deltay: float,
        *,
        update: bool = False,
    ) -> SummaryStatistics:
        """
        Perturb a single point and return the new ``SummaryStatistics``.
        """
        x_mean = shifted_mean(
            mean_old=self.x_mean,
            value_old=self._x[index],
            value_new=self._x[index] + deltax,
            size=len(self),
        )
        y_mean = shifted_mean(
            mean_old=self.y_mean,
            value_old=self._y[index],
            value_new=self._y[index] + deltay,
            size=len(self),
        )

        x_var = shifted_var(
            mean_old=self.x_mean,
            var_old=self._x_var,
            value_old=self._x[index],
            value_new=self._x[index] + deltax,
            size=len(self),
        )

        y_var = shifted_var(
            mean_old=self.y_mean,
            var_old=self._y_var,
            value_old=self._y[index],
            value_new=self._y[index] + deltay,
            size=len(self),
        )

        corrcoef = shifted_corrcoef(
            x_old=self._x[index],
            y_old=self._y[index],
            x_new=self._x[index] + deltax,
            y_new=self._y[index] + deltay,
            meanx_old=self.x_mean,
            meany_old=self.y_mean,
            xy_old=self._xy_mean,
            varx_old=self._x_var,
            vary_old=self._y_var,
            size=len(self),
        )

        if update:
            self._x_mean = x_mean
            self._y_mean = y_mean
            self._x_var = x_var
            self._y_var = y_var
            self._x_stdev = np.sqrt(x_var)
            self._y_stdev = np.sqrt(y_var)
            self._corrcoef = corrcoef
            self._xy_mean += (
                deltax * self._y[index] + deltay * self._x[index] + deltax * deltay
            ) / len(self)

            self._x[index] += deltax
            self._y[index] += deltay

        return SummaryStatistics(
            x_mean,
            y_mean,
            np.sqrt(x_var),
            np.sqrt(y_var),
            corrcoef,
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
