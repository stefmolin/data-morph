"""Wide lines shape."""

from ...data.dataset import Dataset
from ..bases.line_collection import LineCollection


class WideLines(LineCollection):
    """
    Class for the wide lines shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.plotting.diagnostics import plot_shape_on_dataset
        from data_morph.shapes.lines import WideLines

        dataset = DataLoader.load_dataset('panda')
        shape = WideLines(dataset)
        plot_shape_on_dataset(dataset, shape, show_bounds=False, alpha=0.25)

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    name = 'wide_lines'

    def __init__(self, dataset: Dataset) -> None:
        x_bounds, y_bounds = dataset.data_bounds

        offset = x_bounds.range / 5
        lower = x_bounds[0] + offset
        upper = x_bounds[1] - offset

        super().__init__(
            [[lower, y_bounds[0]], [lower, y_bounds[1]]],
            [[upper, y_bounds[0]], [upper, y_bounds[1]]],
        )
