"""Shapes that are circular in nature."""

from numbers import Number

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from ..data.dataset import Dataset
from ..plotting.style import plot_with_custom_style
from .bases.shape import Shape


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
    r : numbers.Number, optional
        The radius of the circle.
    """

    def __init__(self, dataset: Dataset, r: Number = None) -> None:
        self.cx: Number = dataset.df.x.mean()
        """numbers.Number: The x coordinate of the circle's center."""

        self.cy: Number = dataset.df.y.mean()
        """numbers.Number: The y coordinate of the circle's center."""

        self.r: Number = r or dataset.df.std().mean() * 1.5
        """numbers.Number: The radius of the circle."""

        self._center = np.array([self.cx, self.cy])

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} cx={self.cx} cy={self.cy} r={self.r}>'

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
        return abs(self._euclidean_distance(self._center, np.array([x, y])) - self.r)

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
        _ = ax.add_patch(plt.Circle((self.cx, self.cy), self.r, ec='k', fill=False))
        _ = ax.autoscale()
        return ax


class Rings(Shape):
    """
    Class representing rings comprising multiple concentric circles.

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
    num_rings : int, default 4
        The number of rings to include. Must be greater than 1.

    See Also
    --------
    Circle : The individual rings are represented as circles.
    """

    def __init__(self, dataset: Dataset, num_rings: int = 4) -> None:
        if not isinstance(num_rings, int):
            raise TypeError('num_rings must be an integer')
        if num_rings <= 1:
            raise ValueError('num_rings must be greater than 1')

        stdev = dataset.df.std().mean()
        self.circles: list[Circle] = [
            Circle(dataset, r)
            for r in np.linspace(stdev / num_rings * 2, stdev * 2, num_rings)
        ]
        """list[Circle]: The individual rings represented by :class:`Circle` objects."""

        self._centers = np.array([(circle.cx, circle.cy) for circle in self.circles])
        self._radii = np.array([circle.r for circle in self.circles])

    def __repr__(self) -> str:
        return self._recursive_repr('circles')

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

        See Also
        --------
        Circle.distance :
            Rings consists of multiple circles, so we use the minimum
            distance to one of the circles.
        """
        point = np.array([x, y])
        return np.min(
            np.abs(np.linalg.norm(self._centers - point, axis=1) - self._radii)
        )

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
        for circle in self.circles:
            ax = circle.plot(ax)
        return ax


class Bullseye(Rings):
    """
    Class representing a bullseye shape comprising two concentric circles.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.circles import Bullseye

        _ = Bullseye(DataLoader.load_dataset('panda')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.

    See Also
    --------
    Rings : The Bullseye is a special case where we only have 2 rings.
    """

    def __init__(self, dataset: Dataset) -> None:
        super().__init__(dataset=dataset, num_rings=2)
