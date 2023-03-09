"""Shapes that are composed of curves."""

import numpy as np

from ..data.dataset import Dataset
from .bases.point_collection import PointCollection


class DownParab(PointCollection):
    """
    Class for the down parabola shape.

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
            [x, - (((x - (xmax - x_range / 2)) / 4) ** 2) + ymax]
            for x in np.linspace(xmin, xmax, int(x_range / 3))
        ]
        super().__init__(*pts)

    def __str__(self) -> str:
        return 'down_parab'


# class UpParab(Lines): # TODO
#     """Class for the up parabola shape."""

#     def __init__(self, dataset) -> None:
#         # TODO
#         pass

#     def __str__(self) -> str:
#         return 'up_parab'
