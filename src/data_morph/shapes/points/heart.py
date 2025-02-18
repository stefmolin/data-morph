"""Heart shape."""

import numpy as np

from ...data.dataset import Dataset
from ..bases.point_collection import PointCollection


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
        _, xmax = dataset.data_bounds.x_bounds
        x_shift, y_shift = dataset.data_bounds.center

        t = np.linspace(-3, 3, num=80)

        x = 16 * np.sin(t) ** 3
        y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)

        # scale by the half the widest width of the heart
        scale_factor = (xmax - x_shift) / 16

        super().__init__(
            *np.stack([x * scale_factor + x_shift, y * scale_factor + y_shift], axis=1)
        )
