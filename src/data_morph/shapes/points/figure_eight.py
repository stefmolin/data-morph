"""Figure eight shape."""

import numpy as np

from ...data.dataset import Dataset
from ..bases.point_collection import PointCollection


class FigureEight(PointCollection):
    """
    Class for the figure eight shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.points import FigureEight

        _ = FigureEight(DataLoader.load_dataset('panda')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes. For datasets
        with larger *y* ranges than *x* ranges, the figure eight will be
        vertical; otherwise, it will be horizontal.

    Notes
    -----
    This shape uses the formula for the `Lemniscate of Bernoulli
    <https://en.wikipedia.org/wiki/Lemniscate_of_Bernoulli>`_.
    """

    name = 'figure_eight'

    def __init__(self, dataset: Dataset) -> None:
        x_shift, y_shift = dataset.data_bounds.center
        x_range, y_range = dataset.data_bounds.range

        t = np.linspace(-3.1, 3.1, num=80)

        focal_distance = max(x_range, y_range) * 0.3
        half_width = focal_distance * np.sqrt(2)

        x = (half_width * np.cos(t)) / (1 + np.square(np.sin(t)))
        y = x * np.sin(t)

        super().__init__(
            *np.stack([x, y] if x_range >= y_range else [y, x], axis=1)
            + np.array([x_shift, y_shift])
        )
