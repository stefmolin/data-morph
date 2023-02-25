"""Shapes that are composed of curves."""

import numpy as np

from ..data.dataset import Dataset
from .bases.lines import Lines


class DownParab(Lines):
    """Class for the down parabola shape."""

    def __init__(self, dataset: Dataset) -> None:
        q1, q3 = dataset.df.y.quantile([0.25, 0.75])

        # TODO: figure out how to use the data to derive these
        curve = [[x, -(((x - 50) / 4) ** 2) + 90] for x in np.arange(0, 100, 3)]

        super().__init__(*[curve[i : i + 2] for i in range(0, len(curve) - 1, 1)])

    def __str__(self) -> str:
        return 'down_parab'


# class UpParab(Lines): # TODO
#     """Class for the up parabola shape."""

#     def __init__(self, dataset) -> None:
#         # TODO
#         pass

#     def __str__(self) -> str:
#         return 'up_parab'
