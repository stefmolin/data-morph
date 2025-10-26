"""Dots grid shape."""

import itertools

from ...data.dataset import Dataset
from ..bases.point_collection import PointCollection


class DotsGrid(PointCollection):
    """
    Class representing a 3x3 grid of dots.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.plotting.diagnostics import plot_shape_on_dataset
        from data_morph.shapes.points import DotsGrid

        dataset = DataLoader.load_dataset('panda')
        shape = DotsGrid(dataset)
        plot_shape_on_dataset(dataset, shape, show_bounds=False, alpha=0.1)

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    name = 'dots'

    def __init__(self, dataset: Dataset) -> None:
        xlow, xhigh = dataset.data.x.quantile([0.05, 0.95]).tolist()
        ylow, yhigh = dataset.data.y.quantile([0.05, 0.95]).tolist()

        xmid = (xhigh + xlow) / 2
        ymid = (yhigh + ylow) / 2

        super().__init__(
            *list(itertools.product([xlow, xmid, xhigh], [ylow, ymid, yhigh]))
        )
