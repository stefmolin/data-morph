"""Shapes that are circular in nature."""

from numbers import Number

import matplotlib.pyplot as plt
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
            This shape is generated using the dino dataset
            (without normalization).

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.circles import Circle

        _ = Circle(DataLoader.load_dataset('dino')).plot()

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
        return abs(self._euclidean_distance((self.cx, self.cy), (x, y)) - self.r)

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
            _, ax = plt.subplots()
        _ = ax.add_patch(plt.Circle((self.cx, self.cy), self.r, ec='k', fill=False))
        _ = ax.autoscale()
        return ax


class Bullseye(Shape):
    """
    Class representing a bullseye shape comprising two concentric circles.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the dino dataset
            (without normalization).

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.circles import Bullseye

        _ = Bullseye(DataLoader.load_dataset('dino')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        stdev = dataset.df.std().mean()
        self.circles: list[Circle] = [Circle(dataset, r) for r in [stdev, stdev * 2]]
        """list[Circle]: The inner and outer :class:`Circle` objects."""

    def __repr__(self) -> str:
        return self._recursive_repr('circles')

    def distance(self, x: Number, y: Number) -> float:
        """
        Calculate the minimum absolute distance between this bullseye's inner and outer
        circles' edges and a point (x, y).

        Parameters
        ----------
        x, y : numbers.Number
            Coordinates of a point in 2D space.

        Returns
        -------
        float
            The minimum absolute distance between this bullseye's inner and outer
            circles' edges and the point (x, y).

        See Also
        --------
        Circle.distance :
            A bullseye consists of two circles, so we use the minimum
            distance to one of the circles.
        """
        return min(circle.distance(x, y) for circle in self.circles)

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


class Scatter(Circle):  # numpydoc ignore: PR02
    """
    Class for the scatter shape: a circular cloud of scattered points.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the dino dataset
            (without normalization).

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.circles import Scatter

        _ = Scatter(DataLoader.load_dataset('dino')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def distance(self, x: Number, y: Number) -> float:
        """
        Calculate the distance between this circular cloud of scattered points and a point (x, y).

        Parameters
        ----------
        x, y : numbers.Number
            Coordinates of a point in 2D space.

        Returns
        -------
        float
            The distance between this circular cloud of scattered points and the point (x, y).
        """
        return max(self._euclidean_distance((self.cx, self.cy), (x, y)) - self.r, 0)

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
            _, ax = plt.subplots()
        _ = ax.add_patch(
            plt.Circle(
                (self.cx, self.cy),
                self.r,
                ec='k',
                fill=False,
                hatch='.',
                linestyle=':',
            )
        )
        _ = ax.autoscale()
        return ax
