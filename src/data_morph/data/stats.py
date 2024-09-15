"""Utility functions for calculating summary statistics."""

from collections import namedtuple
from collections.abc import Mapping, Sequence
from numbers import Number
from typing import Iterable, Optional

import numpy as np
from avltree import AvlTree

SummaryStatistics = namedtuple(
    'SummaryStatistics',
    ['x_mean', 'y_mean', 'x_med', 'y_med', 'x_stdev', 'y_stdev', 'correlation'],
)
SummaryStatistics.__doc__ = (
    'Named tuple containing the summary statistics for plotting/analysis.'
)


class SortedCounter:
    """
    A version of ``collections.Counter`` that is ordered.

    Notes
    -----
    The time complexity of lookup, insertion, and deletion is O(log n).
    """

    def __init__(self, iterable: Optional[Iterable] = None, /):
        """
        Create a ``SortedCounter`` from an iterable or a mapping.
        """
        self._tree = AvlTree()
        # internal counter for how many elements are there (= size of
        # container)
        self._counter = 0

        if iterable is not None:
            if isinstance(iterable, Iterable):
                for item in iterable:
                    self.add(item)
            elif isinstance(iterable, Mapping):
                for key, value in iterable.items():
                    self.add(key, times=value)
            else:
                raise TypeError(
                    f'Type {type(iterable)} not supported for SortedCounter container.'
                )

        self._counter = sum(self._tree[key] for key in self._tree)

    def add(self, key, /, times: int = 1):
        """
        Add a value to the container (possibly multiple times).

        Raises
        ------
        ValueError
            If ``times`` is < 0.
        """
        if times <= 0:
            raise ValueError(
                f'Cannot add {times} item {key} to container; # of items to add must be > 0'
            )

        try:
            self._tree[key] += times
        except KeyError:
            self._tree[key] = times
        self._counter += times

    def remove(self, key, /, times: int = 1):
        """
        Remove a value from the container (possibly multiple times).

        Raises
        ------
        ValueError
            If ``times`` is < 0.

        Notes
        -----
        If ``key`` is not present in the container, does nothing.
        If ``times`` is larger than the current number of items in the
        container, ``key`` is removed from the container.
        """
        if times <= 0:
            raise ValueError(
                f'Cannot remove item {key} {times} times from container; # of items to remove must be > 0'
            )

        if self._tree[key] - times <= 0:
            del self._tree[key]
        else:
            self._tree[key] -= times
        self._counter -= times

    def __getitem__(self, key):
        return self._tree[key]

    def __len__(self):
        return self._counter

    def maximum(self):
        """
        Return the maximum value stored in the container.
        """
        return self._tree.maximum()

    def minimum(self):
        """
        Return the minimum value stored in the container.
        """
        return self._tree.minimum()

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(dict(self._tree))})'


def create_median_tree(data: Sequence, /) -> tuple[SortedCounter, SortedCounter]:
    """
    Return a tuple of low and high ``SortedCounter``s from input data.

    Parameters
    ----------
    data
        The input data as an iterable

    Returns
    -------
    tuple[SortedCounter, SortedCounter]
        The low and high ``SortedCounter``s.

    Notes
    -----
    The time complexity of the execution of the function is O(n log n) due to
    the sorting operation done beforehand.
    """
    # make sure the data is sorted
    data = sorted(data)
    half = len(data) // 2
    return SortedCounter(data[:half]), SortedCounter(data[half:])


def shifted_mean(
    mean_old: float,
    value_old: float,
    value_new: float,
    size: int,
) -> float:
    """
    Return the shifted mean by perturbing one point.

    Parameters
    ----------
    mean_old : float
        The old value of the mean of the data.
    value_old : float
        The old value of the point (before perturbation).
    value_new : float
        The new value of the point (after perturbation).
    size : int
        The size of the dataset.

    Returns
    -------
    float
        The new value of the mean of the data.
    """
    return (mean_old - value_old / size) + value_new / size


def shifted_var(
    mean_old: float,
    var_old: float,
    value_old: float,
    value_new: float,
    size: int,
    *,
    ddof: float = 0,
) -> float:
    """
    Compute the shifted variance by perturbing one point.

    Parameters
    ----------
    mean_old : float
        The old value of the mean of the data.
    var_old : float
        The old value of the variance of the data.
    value_old : float
        The old value of the point (before perturbation).
    value_new : float
        The new value of the point (after perturbation).
    size : int
        The size of the dataset.
    ddof : float, optional
        “Delta Degrees of Freedom”: the divisor used in the calculation is ``N
        - ddof``, where ``N`` represents the number of elements. By default
        ``ddof`` is zero.

    Returns
    -------
    float
        The new value of the covariance of the data.
    """
    return (
        var_old
        + 2 * (value_new - value_old) * (value_old - mean_old) / (size - ddof)
        + (value_new - value_old) ** 2 * (1 / (size - ddof) - 1 / (size - ddof) / size)
    )


def shifted_stdev(*args, **kwargs):
    """
    Compute the shifted standard deviation by perturbing one point.

    Parameters
    ----------
    *args
        The positional arguments passed to :attr:``shifted_cov``.
    **kwargs
        The keyword arguments passed to :attr:``shifted_cov``.

    Returns
    -------
    float
        The new value of the standard deviation of the data.
    """
    return np.sqrt(shifted_var(*args, **kwargs))


def shifted_corrcoef(
    x_old: float,
    y_old: float,
    x_new: float,
    y_new: float,
    meanx_old: float,
    meany_old: float,
    xy_old: float,
    varx_old: float,
    vary_old: float,
    size: int,
) -> float:
    """
    Compute the shifted correlation of the data by perturbing one point.

    Parameters
    ----------
    x_old : float
        The old value of the point ``x`` (before perturbation).
    y_old : float
        The old value of the point ``y`` (before perturbation).
    x_new : float
        The new value of the point ``x`` (after perturbation).
    y_new : float
        The new value of the point ``y`` (after perturbation).
    meanx_old : float
        The old value of the mean of the data ``x``.
    meany_old : float
        The old value of the mean of the data ``y``.
    xy_old : float
        The old value of the mean of ``x * y``.
    varx_old : float
        The old value of the variance of ``x``.
    vary_old : float
        The old value of the variance of ``y``.
    size : int
        The size of the dataset.

    Returns
    -------
    float
        The new correlation coefficient of the data.
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


def shifted_median(
    xlow: SortedCounter,
    xhigh: SortedCounter,
    value_old: float,
    value_new: float,
) -> float:
    """
    Compute the shifted median using two ``SortedCounter``s.

    Parameters
    ----------
    xlow : SortedCounter
        The lower part of the data (below the median).

    xhigh : SortedCounter
        The higher part of the data (above the median).

    value_old : float
        The old value of the point (before perturbation).

    value_new : float
        The new value of the point (after perturbation).

    Returns
    -------
    float
        The new value of the median of the data.

    Notes
    -----
    Modifies ``xlow`` and ``xhigh`` in-place.
    """

    # notation:
    # S1 = lower half of data values
    # S2 = upper half of data values
    # G  = range of values <max(S1), min(S2)>. Note that it can be empty in case of duplicates
    # L  = range <-inf, min(S1)>
    # H  = range <max(S2), inf>
    # xi = old value of the data point
    # xi'= new value of the data point
    #
    # constraints:
    # at the end of the computation, we need abs(len(S2) - len(S1)) = 0
    # if len(S1) + len(S2) is even, 1 if odd

    low_max = xlow.maximum()
    high_min = xhigh.minimum()

    # xi is guaranteed to be in either S1 or S2
    if value_old <= low_max:
        xlow.remove(value_old)
    elif value_old >= high_min:
        xhigh.remove(value_old)

    # it doesn't really matter where we insert it since we are rebalancing
    # later anyway
    if value_new <= xlow.maximum():
        xlow.add(value_new)
    else:
        xhigh.add(value_new)

    # Rebalance the two SortedCounters if their sizes differ by more than 1
    # NOTE: this operation is O(log n) since we are always doing it only a
    # handful (fixed number) of times

    # remove items from xlow and add them in xhigh
    while len(xlow) > len(xhigh):
        low_max = xlow.maximum()
        xlow.remove(low_max)
        xhigh.add(low_max)

    # remove items from xhigh and add them in xlow
    while len(xhigh) > len(xlow):
        high_min = xhigh.minimum()
        xhigh.remove(high_min)
        xlow.add(high_min)

    # Compute the median based on the sizes of xlow and xhigh
    if len(xlow) == len(xhigh):
        return (xlow.maximum() + xhigh.minimum()) / 2
    if len(xlow) > len(xhigh):
        return xlow.maximum()

    return xhigh.minimum()


class Statistics:
    """
    Container for computing various statistics of the data.

    Parameters
    ----------
    x : iterable of float
        The ``x`` value of the data as an iterable.
    y : iterable of float
        The ``y`` value of the data as an iterable.
    """

    def __init__(self, x: Iterable[Number], y: Iterable[Number]):
        if len(x) != len(y):
            raise ValueError('The two datasets should have the same size')

        self._x = np.copy(x)
        self._y = np.copy(y)
        self._size = len(self._x)
        self._x_mean = np.mean(self._x)
        self._y_mean = np.mean(self._y)
        self._x_median = np.median(self._x)
        self._y_median = np.median(self._y)
        self._x_low, self._x_high = create_median_tree(self._x)
        self._y_low, self._y_high = create_median_tree(self._y)
        self._x_var = np.var(self._x, ddof=0)
        self._x_stdev = np.sqrt(self._x_var)
        self._y_var = np.var(self._y, ddof=0)
        self._y_stdev = np.sqrt(self._y_var)
        self._corrcoef = np.corrcoef(self._x, self._y)[0, 1]
        self._xy_mean = np.mean(self._x * self._y)

    @property
    def x_mean(self) -> float:
        """
        Return the mean of the ``x`` data.

        Returns
        -------
        float
            The mean of the ``x`` data.
        """
        return self._x_mean

    @property
    def y_mean(self) -> float:
        """
        Return the mean of the ``y`` data.

        Returns
        -------
        float
            The mean of the ``y`` data.
        """
        return self._y_mean

    @property
    def x_stdev(self) -> float:
        """
        Return the std of the ``x`` data.

        Returns
        -------
        float
            The standard deviation of the ``x`` data.
        """
        return self._x_stdev

    @property
    def y_stdev(self) -> float:
        """
        Return the std of the ``y`` data.

        Returns
        -------
        float
            The standard deviation of the ``y`` data.
        """
        return self._y_stdev

    @property
    def corrcoef(self) -> float:
        """
        Return the correlation coefficient of the ``x`` and ``y`` data.

        Returns
        -------
        float
            The correlation coefficient between ``x`` and ``y`` data.
        """
        return self._corrcoef

    def __len__(self):
        """
        Return the size of the dataset.

        Returns
        -------
        int
            The size of the dataset.
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

        Parameters
        ----------
        index : int
            The index of the point we wish to perturb.

        deltax : float
            The amount by which to perturb the ``x`` point.

        deltay : float
            The amount by which to perturb the ``y`` point.

        update : bool, optional
            Whether to actually update the data (default: False).

        Returns
        -------
        SummaryStatistics
            The new summary statistics.
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

        # `shifted_median` updates the containers in-place; in case
        # `update=False`, we put it back
        x_median = shifted_median(
            xlow=self._x_low,
            xhigh=self._x_high,
            value_old=self._x[index],
            value_new=self._x[index] + deltax,
        )

        y_median = shifted_median(
            xlow=self._y_low,
            xhigh=self._y_high,
            value_old=self._y[index],
            value_new=self._y[index] + deltay,
        )

        if update:
            self._x_mean = x_mean
            self._y_mean = y_mean
            self._x_median = x_median
            self._y_median = y_median
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
        else:
            shifted_median(
                xlow=self._x_low,
                xhigh=self._x_high,
                value_old=self._x[index] + deltax,
                value_new=self._x[index],
            )

            shifted_median(
                xlow=self._y_low,
                xhigh=self._y_high,
                value_old=self._y[index] + deltay,
                value_new=self._y[index],
            )

        return SummaryStatistics(
            x_mean,
            y_mean,
            x_median,
            y_median,
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
        np.median(x),
        np.median(y),
        np.std(x, ddof=1),
        np.std(y, ddof=1),
        np.corrcoef(x, y)[0, 1],
    )
