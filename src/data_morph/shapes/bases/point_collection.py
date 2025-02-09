"""Base class for shapes that are composed of points."""

from __future__ import annotations

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np

from ...plotting.style import plot_with_custom_style
from .shape import Shape

if TYPE_CHECKING:
    from collections.abc import Iterable
    from numbers import Number

    from matplotlib.axes import Axes


class PointCollection(Shape):
    """
    Class representing a shape formed by a collection of points.

    Parameters
    ----------
    *points : Iterable[numbers.Number]
        An iterable of (x, y) values representing an arrangement of points.
    """

    def __init__(self, *points: Iterable[Number]) -> None:
        self.points = np.array(points)
        """numpy.ndarray: An array of (x, y) values
        representing an arrangement of points."""

        self._alpha = 1

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} of {len(self.points)} points>'

    def distance(self, x: Number, y: Number) -> float:
        """
        Calculate the minimum distance from the points of this shape
        to a point (x, y).

        Parameters
        ----------
        x, y : numbers.Number
            Coordinates of a point in 2D space.

        Returns
        -------
        float
            The minimum distance from the points of this shape
            to the point (x, y).
        """
        return np.min(
            np.linalg.norm(np.array(self.points) - np.array((x, y)), ord=2, axis=1)
        )

    @plot_with_custom_style
    def plot(self, ax: Axes | None = None) -> Axes:
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
        _ = ax.scatter(*self.points.T, s=5, color='k', alpha=self._alpha)
        return ax
