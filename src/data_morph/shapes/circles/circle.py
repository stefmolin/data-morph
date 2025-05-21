"""Circle shape."""

from __future__ import annotations

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np

from ...plotting.style import plot_with_custom_style
from ..bases.shape import Shape

if TYPE_CHECKING:
    from numbers import Number

    from matplotlib.axes import Axes

    from ..data.dataset import Dataset


class Circle(Shape):
    """
    Class representing a hollow circle.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.circles import Circle

        _ = Circle(DataLoader.load_dataset('panda')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    radius : numbers.Number, optional
        The radius of the circle.
    """

    def __init__(self, dataset: Dataset, radius: Number | None = None) -> None:
        self.center: tuple[Number, Number] = dataset.data_bounds.center
        """The (x, y) coordinates of the circle's center."""

        self.radius: Number = radius or dataset.data[['x', 'y']].std().mean() * 1.5
        """The radius of the circle."""

    def __repr__(self) -> str:
        x, y = self.center
        return f'<{self.__class__.__name__} center={(float(x), float(y))} radius={self.radius}>'

    def distance(self, x: Number, y: Number) -> float:
        """
        Calculate the absolute distance between this circle's edge and a point (x, y).

        Parameters
        ----------
        x, y : numbers.Number
            Coordinates of a point in 2D space.

        Returns
        -------
        float
            The absolute distance between this circle's edge and the point (x, y).
        """
        return abs(
            self._euclidean_distance(self.center, np.array([x, y])) - self.radius
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
        _ = ax.add_patch(plt.Circle(self.center, self.radius, ec='k', fill=False))
        _ = ax.autoscale()
        return ax
