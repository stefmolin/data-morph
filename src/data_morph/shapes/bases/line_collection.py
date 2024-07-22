"""Base class for shapes that are composed of lines."""

from numbers import Number
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from ...plotting.style import plot_with_custom_style
from .shape import Shape


class LineCollection(Shape):
    """
    Class representing a shape consisting of one or more lines.

    Parameters
    ----------
    *lines : Iterable[Iterable[numbers.Number]]
        An iterable of two (x, y) pairs representing the endpoints
        of a line.
    """

    def __init__(self, *lines: Iterable[Iterable[Number]]) -> None:
        # check that lines that have the same starting and ending points raise an error
        for line in lines:
            start, end = line
            if np.allclose(start, end):
                raise ValueError(f'Line {line} has the same start and end point')
        self.lines = lines
        """Iterable[Iterable[numbers.Number]]: An iterable
        of two (x, y) pairs representing the endpoints of a line."""

    def __repr__(self) -> str:
        return self._recursive_repr('lines')

    def distance(self, x: Number, y: Number) -> float:
        """
        Calculate the minimum distance from the lines of this shape
        to a point (x, y).

        Parameters
        ----------
        x, y : numbers.Number
            Coordinates of a point in 2D space.

        Returns
        -------
        float
            The minimum distance from the lines of this shape to the
            point (x, y).

        Notes
        -----
        Implementation based on `this Stack Overflow answer`_.

        .. _this Stack Overflow answer: https://stackoverflow.com/a/58781995
        """
        p = np.array([x, y])
        lines = np.array(self.lines)

        a = lines[:, 0, :]
        b = lines[:, 1, :]

        d_ba = b - a
        d = np.divide(d_ba, (np.hypot(d_ba[:, 0], d_ba[:, 1]).reshape(-1, 1)))

        # signed parallel distance components
        # rowwise dot products of 2D vectors
        s = np.multiply(a - p, d).sum(axis=1)
        t = np.multiply(p - b, d).sum(axis=1)

        # clamped parallel distance
        h = np.maximum.reduce([s, t, np.zeros(len(s))])

        # perpendicular distance component
        # rowwise cross products of 2D vectors
        d_pa = p - a
        c = d_pa[:, 0] * d[:, 1] - d_pa[:, 1] * d[:, 0]

        return np.min(np.hypot(h, c))

    @plot_with_custom_style
    def plot(self, ax: Axes = None) -> Axes:
        """
        Plot the shape.

        Parameters
        ----------
        ax : matplotlib.axes.Axes, optional
            An optional :class:`~matplotlib.axes.Axes` object to plot on.

        Returns
        -------
        matplotlib.axes.Axes
            The :class:`~matplotlib.axes.Axes` object containing the plot.
        """
        if not ax:
            fig, ax = plt.subplots(layout='constrained')
            fig.get_layout_engine().set(w_pad=0.2, h_pad=0.2)
        _ = ax.axis('equal')
        for start, end in self.lines:
            ax.plot(*list(zip(start, end)), 'k-')
        return ax
