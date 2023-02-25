"""Polygon shapes made from lines."""

from ..data.dataset import Dataset
from .bases.lines import Lines


class Star(Lines):
    """Class for the star shape."""

    def __init__(self, dataset: Dataset) -> None:
        # q1, q3 = dataset.df.y.quantile([0.25, 0.75])

        # TODO: figure out how to use the data to derive these
        star_pts = [
            10,
            40,
            40,
            40,
            50,
            10,
            60,
            40,
            90,
            40,
            65,
            60,
            75,
            90,
            50,
            70,
            25,
            90,
            35,
            60,
        ]
        pts = [star_pts[i : i + 2] for i in range(0, len(star_pts), 2)]
        pts = [[p[0] * 0.8 + 20, 100 - p[1]] for p in pts]
        pts.append(pts[0])

        super().__init__(*[pts[i : i + 2] for i in range(0, len(pts) - 1, 1)])
