"""Rings shape."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from ...plotting.style import plot_with_custom_style
from ..bases.shape import Shape
from .circle import Circle

if TYPE_CHECKING:
    from numbers import Number

    from matplotlib.axes import Axes

    from ..data.dataset import Dataset


class Rings(Shape):
    """
    Class representing rings comprising three concentric circles.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.circles import Rings

        _ = Rings(DataLoader.load_dataset('panda')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.

    See Also
    --------
    Circle : The individual rings are represented as circles.
    """

    def __init__(self, dataset: Dataset) -> None:
        self.circles: list[Circle] = [
            Circle(dataset, radius) for radius in self._derive_radii(dataset)
        ]
        """The individual rings represented by :class:`Circle` objects."""

        self._centers = np.array([circle.center for circle in self.circles])
        self._radii = np.array([circle.radius for circle in self.circles])

    def __repr__(self) -> str:
        return self._recursive_repr('circles')

    @staticmethod
    def _derive_radii(dataset: Dataset) -> np.ndarray:
        """
        Derive the radii for the circles in the rings.

        Parameters
        ----------
        dataset : Dataset
            The starting dataset to morph into.

        Returns
        -------
        np.ndarray
            The radii for the circles in the rings.
        """
        stdev = (min(dataset.data_bounds.range) + min(dataset.morph_bounds.range)) / 4
        return np.linspace(stdev, 0, 3, endpoint=False)

    def distance(self, x: Number, y: Number) -> float:
        """
        Calculate the minimum absolute distance between any of this shape's
        circles' edges and a point (x, y).

        Parameters
        ----------
        x, y : numbers.Number
            Coordinates of a point in 2D space.

        Returns
        -------
        float
            The minimum absolute distance between any of this shape's
            circles' edges and the point (x, y).
        """
        point = np.array([x, y])
        return np.min(
            np.abs(np.linalg.norm(self._centers - point, axis=1) - self._radii)
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
        for circle in self.circles:
            ax = circle.plot(ax)
        return ax
