"""Rectangle shape."""

from ...data.dataset import Dataset
from ..bases.line_collection import LineCollection


class Rectangle(LineCollection):
    """
    Class for the rectangle shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.plotting.diagnostics import plot_shape_on_dataset
        from data_morph.shapes.lines import Rectangle

        dataset = DataLoader.load_dataset('panda')
        shape = Rectangle(dataset)
        plot_shape_on_dataset(dataset, shape, show_bounds=False, alpha=0.25)

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        xmin, xmax = dataset.data.x.quantile([0.1, 0.9])
        ymin, ymax = dataset.data.y.quantile([0.1, 0.9])

        super().__init__(
            [[xmin, ymin], [xmin, ymax]],
            [[xmin, ymin], [xmax, ymin]],
            [[xmax, ymin], [xmax, ymax]],
            [[xmin, ymax], [xmax, ymax]],
        )
