"""Diamond shape."""

from ...data.dataset import Dataset
from ..bases.line_collection import LineCollection


class Diamond(LineCollection):
    """
    Class for the diamond shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        import matplotlib.pyplot as plt
        from data_morph.data.loader import DataLoader
        from data_morph.shapes.polygons import Diamond

        _ = Diamond(DataLoader.load_dataset('panda')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        xmin, xmax = dataset.df.x.quantile([0.05, 0.95])
        ymin, ymax = dataset.df.y.quantile([0.05, 0.95])

        xmid = (xmax + xmin) / 2
        ymid = (ymax + ymin) / 2

        super().__init__(
            [[xmin, ymid], [xmid, ymax]],
            [[xmid, ymax], [xmax, ymid]],
            [[xmax, ymid], [xmid, ymin]],
            [[xmid, ymin], [xmin, ymid]],
        )
