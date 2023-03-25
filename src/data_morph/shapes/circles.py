"""Shapes that are circular in nature."""

from numbers import Number

from ..data.dataset import Dataset
from .bases.shape import Shape


class Circle(Shape):
    """
    Class representing a hollow circle.

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    r : Number, optional
        The radius of the circle.
    """

    def __init__(self, dataset: Dataset, r: Number = None) -> None:
        self.cx: float = dataset.df.x.mean()
        self.cy: float = dataset.df.y.mean()
        self.r: Number = r or dataset.df.std().mean() * 1.5

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} cx={self.cx} cy={self.cy} r={self.r}>'

    def distance(self, x: Number, y: Number) -> float:
        """
        Calculate the absolute distance between this circle's edge and a point (x, y).

        Parameters
        ----------
        x, y : Number
            Coordinates of a point in 2D space.

        Returns
        -------
        float
            The absolute distance between this circle's edge and the point (x, y).
        """
        return abs(self._euclidean_distance((self.cx, self.cy), (x, y)) - self.r)


class Bullseye(Shape):
    """
    Class representing a bullseye shape comprising two concentric circles.

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        stdev = dataset.df.std().mean()
        self.circles: list[Circle] = [Circle(dataset, r) for r in [stdev, stdev * 2]]

    def __repr__(self) -> str:
        return self._recursive_repr('circles')

    def distance(self, x: Number, y: Number) -> float:
        """
        Calculate the minimum absolute distance between this bullseye's inner and outer
        circles' edges and a point (x, y).

        Parameters
        ----------
        x, y : Number
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
