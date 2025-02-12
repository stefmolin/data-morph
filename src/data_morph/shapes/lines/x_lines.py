"""X lines shape."""

from ...data.dataset import Dataset
from ..bases.line_collection import LineCollection


class XLines(LineCollection):
    """
    Class for the X shape consisting of two crossing, perpendicular lines.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.lines import XLines

        _ = XLines(DataLoader.load_dataset('panda')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    name = 'x'

    def __init__(self, dataset: Dataset) -> None:
        (xmin, xmax), (ymin, ymax) = dataset.morph_bounds

        super().__init__([[xmin, ymin], [xmax, ymax]], [[xmin, ymax], [xmax, ymin]])
