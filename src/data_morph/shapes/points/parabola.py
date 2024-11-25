"""Parabola shapes."""

import numpy as np

from ...data.dataset import Dataset
from ..bases.point_collection import PointCollection


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
