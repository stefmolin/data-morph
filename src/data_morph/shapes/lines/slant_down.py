"""Slant down lines shape."""

from ...data.dataset import Dataset
from ..bases.line_collection import LineCollection


class SlantDownLines(LineCollection):
    """
    Class for the slant down lines shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.lines import SlantDownLines

        _ = SlantDownLines(DataLoader.load_dataset('panda')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    name = 'slant_down'

    def __init__(self, dataset: Dataset) -> None:
        x_bounds, y_bounds = dataset.morph_bounds

        xmin, xmax = x_bounds
        xmid = xmin + x_bounds.range / 2
        x_offset = (xmid - xmin) / 2

        ymin, ymax = y_bounds
        ymid = ymin + y_bounds.range / 2
        y_offset = (ymid - ymin) / 2

        super().__init__(
            [[xmin, ymid], [xmid, ymin]],
            [[xmin, ymid + y_offset], [xmid + x_offset, ymin]],
            [[xmin, ymax], [xmax, ymin]],
            [[xmin + x_offset, ymax], [xmax, ymin + y_offset]],
            [[xmid, ymax], [xmax, ymid]],
        )
