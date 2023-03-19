"""Base class for shapes that are composed of points."""

from numbers import Number
from typing import Iterable

import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from ...plotting.style import plot_with_custom_style
from .shape import Shape


class PointCollection(Shape):
    """
    Class representing a shape formed by a collection of points.

    Parameters
    ----------
    *points : Iterable[Iterable[numbers.Number]]
        An iterable of (x, y) values representing an arrangement of points.
    """

    def __init__(self, *points: Iterable[Iterable[Number]]) -> None:
        self.points = points
        """Iterable[Iterable[numbers.Number]]: An iterable of (x, y) values
        representing an arrangement of points."""

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
        return min(self._euclidean_distance((x, y), point) for point in self.points)

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
        for point in self.points:
            ax.scatter(*point, s=20, color='k')
            ax.axis('equal')
        return ax
