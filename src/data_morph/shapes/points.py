"""Shapes that are composed of points."""

import numpy as np

from ..data.dataset import Dataset
from .bases.point_collection import PointCollection


class DownParabola(PointCollection):
    """
    Class for the down parabola shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the dino dataset
            (without normalization).

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.points import DownParabola

        _ = DownParabola(DataLoader.load_dataset('dino')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        x_bounds = dataset.morph_bounds.x_bounds
        x_range = x_bounds.range

        xmin, xmax = x_bounds
        ymax = dataset.data_bounds.y_bounds[1]

        pts = [
            [x, -(((x - (xmax - x_range / 2)) / 4) ** 2) + ymax]
            for x in np.linspace(xmin, xmax, int(x_range / 3))
        ]
        super().__init__(*pts)

    def __str__(self) -> str:
        return 'down_parab'


class UpParabola(PointCollection):
    """
    Class for the up parabola shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the dino dataset
            (without normalization).

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.points import UpParabola

        _ = UpParabola(DataLoader.load_dataset('dino')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset) -> None:
        x_bounds = dataset.morph_bounds.x_bounds
        x_range = x_bounds.range

        xmin, xmax = x_bounds
        ymin = dataset.data_bounds.y_bounds[0]

        pts = [
            [x, (((x - (xmax - x_range / 2)) / 4) ** 2) + ymin]
            for x in np.linspace(xmin, xmax, int(x_range / 3))
        ]
        super().__init__(*pts)

    def __str__(self) -> str:
        return 'up_parab'
