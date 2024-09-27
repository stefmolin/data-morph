"""Shapes that are composed of points."""

import itertools
from numbers import Number

import numpy as np

from ..data.dataset import Dataset
from .bases.point_collection import PointCollection


class DotsGrid(PointCollection):
    """
    Class representing a 3x3 grid of dots.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.points import DotsGrid

        _ = DotsGrid(DataLoader.load_dataset('panda')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        xlow, xhigh = dataset.df.x.quantile([0.05, 0.95]).tolist()
        ylow, yhigh = dataset.df.y.quantile([0.05, 0.95]).tolist()

        xmid = (xhigh + xlow) / 2
        ymid = (yhigh + ylow) / 2

        super().__init__(
            *list(itertools.product([xlow, xmid, xhigh], [ylow, ymid, yhigh]))
        )

    def __str__(self) -> str:
        return 'dots'


class DownParabola(PointCollection):
    """
    Class for the down parabola shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.points import DownParabola

        _ = DownParabola(DataLoader.load_dataset('panda')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        x_bounds = dataset.data_bounds.x_bounds
        xmin, xmax = x_bounds
        xmid = xmax - x_bounds.range / 2

        x_offset = x_bounds.range / 10
        xmin += x_offset
        xmax -= x_offset

        ymin, ymax = dataset.data_bounds.y_bounds

        poly = np.polynomial.Polynomial.fit([xmin, xmid, xmax], [ymin, ymax, ymin], 2)

        super().__init__(*np.stack(poly.linspace(), axis=1))

    def __str__(self) -> str:
        return 'down_parab'


class Heart(PointCollection):
    """
    Class for the heart shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.points import Heart

        _ = Heart(DataLoader.load_dataset('panda')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.

    Notes
    -----
    The formula for the heart shape is inspired by
    `Heart Curve <https://mathworld.wolfram.com/HeartCurve.html>`_:

        Weisstein, Eric W. "Heart Curve." From `MathWorld <https://mathworld.wolfram.com/>`_
        --A Wolfram Web Resource. https://mathworld.wolfram.com/HeartCurve.html
    """

    def __init__(self, dataset: Dataset) -> None:
        x_bounds = dataset.data_bounds.x_bounds
        y_bounds = dataset.data_bounds.y_bounds

        x_shift = sum(x_bounds) / 2
        y_shift = sum(y_bounds) / 2

        t = np.linspace(-3, 3, num=80)

        x = 16 * np.sin(t) ** 3
        y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)

        # scale by the half the widest width of the heart
        scale_factor = (x_bounds[1] - x_shift) / 16

        super().__init__(
            *np.stack([x * scale_factor + x_shift, y * scale_factor + y_shift], axis=1)
        )


class LeftParabola(PointCollection):
    """
    Class for the left parabola shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.points import LeftParabola

        _ = LeftParabola(DataLoader.load_dataset('panda')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        y_bounds = dataset.data_bounds.y_bounds
        ymin, ymax = y_bounds
        ymid = ymax - y_bounds.range / 2

        y_offset = y_bounds.range / 10
        ymin += y_offset
        ymax -= y_offset

        xmin, xmax = dataset.data_bounds.x_bounds

        poly = np.polynomial.Polynomial.fit([ymin, ymid, ymax], [xmin, xmax, xmin], 2)

        super().__init__(*np.stack(poly.linspace()[::-1], axis=1))

    def __str__(self) -> str:
        return 'left_parab'


class RightParabola(PointCollection):
    """
    Class for the right parabola shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.points import RightParabola

        _ = RightParabola(DataLoader.load_dataset('panda')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        y_bounds = dataset.data_bounds.y_bounds
        ymin, ymax = y_bounds
        ymid = ymax - y_bounds.range / 2

        y_offset = y_bounds.range / 10
        ymin += y_offset
        ymax -= y_offset

        xmin, xmax = dataset.data_bounds.x_bounds

        poly = np.polynomial.Polynomial.fit([ymin, ymid, ymax], [xmax, xmin, xmax], 2)

        super().__init__(*np.stack(poly.linspace()[::-1], axis=1))

    def __str__(self) -> str:
        return 'right_parab'


class UpParabola(PointCollection):
    """
    Class for the up parabola shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.points import UpParabola

        _ = UpParabola(DataLoader.load_dataset('panda')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        x_bounds = dataset.data_bounds.x_bounds
        xmin, xmax = x_bounds
        xmid = xmax - x_bounds.range / 2

        x_offset = x_bounds.range / 10
        xmin += x_offset
        xmax -= x_offset

        ymin, ymax = dataset.data_bounds.y_bounds

        poly = np.polynomial.Polynomial.fit([xmin, xmid, xmax], [ymax, ymin, ymax], 2)

        super().__init__(*np.stack(poly.linspace(), axis=1))

    def __str__(self) -> str:
        return 'up_parab'


class Scatter(PointCollection):
    """
    Class for the scatter shape: a cloud of randomly-scattered points.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.points import Scatter

        _ = Scatter(DataLoader.load_dataset('panda')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        rng = np.random.default_rng(1)
        center = (dataset.df.x.mean(), dataset.df.y.mean())
        points = [center]
        max_radius = max(dataset.df.x.std(), dataset.df.y.std())
        for radius in np.linspace(max_radius // 5, max_radius, num=5):
            for angle in np.linspace(0, 360, num=50, endpoint=False):
                points.append(
                    (
                        center[0]
                        + np.cos(angle) * radius
                        + rng.standard_normal() * max_radius,
                        center[1]
                        + np.sin(angle) * radius
                        + rng.standard_normal() * max_radius,
                    )
                )
        super().__init__(*points)

        self._alpha = 0.4

    def distance(self, x: Number, y: Number) -> int:
        """
        No-op that allows returns 0 so that all perturbations are accepted.

        Parameters
        ----------
        x, y : int or float
            Coordinates of a point in 2D space.

        Returns
        -------
        int
            Always returns 0 to allow for scattering of the points.
        """
        return 0


class Spade(PointCollection):
    """
    Class for the spade shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.points import Spade

        _ = Spade(DataLoader.load_dataset('panda')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        x_bounds = dataset.data_bounds.x_bounds
        y_bounds = dataset.data_bounds.y_bounds

        x_shift = sum(x_bounds) / 2
        y_shift = sum(y_bounds) / 2

        # graph upside-down heart
        heart_points = Heart(dataset).points
        heart_points[:, 1] = -heart_points[:, 1] + 2 * y_shift

        # line base
        line_x = np.linspace(-6, 6, num=12)
        line_y = np.repeat(-16, 12)

        # left wing
        left_x = np.linspace(-6, 0, num=12)
        left_y = 0.278 * np.power(left_x + 6.0, 2) - 16

        # right wing
        right_x = np.linspace(0, 6, num=12)
        right_y = 0.278 * np.power(right_x - 6.0, 2) - 16

        # shift and scale the base and wing
        base_x = np.concatenate((line_x, left_x, right_x), axis=0)
        base_y = np.concatenate((line_y, left_y, right_y), axis=0)

        # scale by the half the widest width of the spade
        scale_factor = (x_bounds[1] - x_shift) / 16
        base_x = base_x * scale_factor + x_shift
        base_y = base_y * scale_factor + y_shift

        # combine the base and the upside-down heart
        x = np.concatenate((heart_points[:, 0], base_x), axis=0)
        y = np.concatenate((heart_points[:, 1], base_y), axis=0)

        super().__init__(*np.stack([x, y], axis=1))
