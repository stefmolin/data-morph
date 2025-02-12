"""High lines shape."""

from ...data.dataset import Dataset
from ..bases.line_collection import LineCollection


class HighLines(LineCollection):
    """
    Class for the high lines shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.lines import HighLines

        _ = HighLines(DataLoader.load_dataset('panda')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    name = 'high_lines'

    def __init__(self, dataset: Dataset) -> None:
        x_bounds, y_bounds = dataset.data_bounds

        offset = y_bounds.range / 5
        lower = y_bounds[0] + offset
        upper = y_bounds[1] - offset

        super().__init__(
            [[x_bounds[0], lower], [x_bounds[1], lower]],
            [[x_bounds[0], upper], [x_bounds[1], upper]],
        )
