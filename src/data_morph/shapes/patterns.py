"""Shapes that are patterns of lines."""

import numpy as np

from ..data.dataset import Dataset
from .bases.lines import Lines


class HighLines(Lines):
    """
    Class for the high lines shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the dino dataset
            (without normalization).

        import matplotlib.pyplot as plt
        from data_morph.data.loader import DataLoader
        from data_morph.shapes.patterns import HighLines

        _ = HighLines(DataLoader.load_dataset('dino')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        x_bounds = dataset.morph_bounds.x_bounds
        y_bounds = dataset.data_bounds.y_bounds

        offset = y_bounds.range / 5
        lower = y_bounds[0] + offset
        upper = y_bounds[1] - offset

        super().__init__(
            [[x_bounds[0], lower], [x_bounds[1], lower]],
            [[x_bounds[0], upper], [x_bounds[1], upper]],
        )

    def __str__(self) -> str:
        return 'high_lines'


class HorizontalLines(Lines):
    """
    Class for the horizontal lines shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the dino dataset
            (without normalization).

        import matplotlib.pyplot as plt
        from data_morph.data.loader import DataLoader
        from data_morph.shapes.patterns import HorizontalLines

        _ = HorizontalLines(DataLoader.load_dataset('dino')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        x_bounds = dataset.morph_bounds.x_bounds
        y_bounds = dataset.data_bounds.y_bounds

        super().__init__(
            *[
                [[x_bounds[0], y], [x_bounds[1], y]]
                for y in np.linspace(y_bounds[0], y_bounds[1], 5)
            ]
        )

    def __str__(self) -> str:
        return 'h_lines'


class SlantDownLines(Lines):
    """
    Class for the slant down lines shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the dino dataset
            (without normalization).

        import matplotlib.pyplot as plt
        from data_morph.data.loader import DataLoader
        from data_morph.shapes.patterns import SlantDownLines

        _ = SlantDownLines(DataLoader.load_dataset('dino')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        x_bounds = dataset.morph_bounds.x_bounds
        y_bounds = dataset.morph_bounds.y_bounds

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

    def __str__(self) -> str:
        return 'slant_down'


class SlantUpLines(Lines):
    """
    Class for the slant up lines shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the dino dataset
            (without normalization).

        import matplotlib.pyplot as plt
        from data_morph.data.loader import DataLoader
        from data_morph.shapes.patterns import SlantUpLines

        _ = SlantUpLines(DataLoader.load_dataset('dino')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        x_bounds = dataset.morph_bounds.x_bounds
        y_bounds = dataset.morph_bounds.y_bounds

        xmin, xmax = x_bounds
        xmid = xmin + x_bounds.range / 2
        x_offset = (xmid - xmin) / 2

        ymin, ymax = y_bounds
        ymid = ymin + y_bounds.range / 2
        y_offset = (ymid - ymin) / 2

        super().__init__(
            [[xmin, ymid], [xmid, ymax]],
            [[xmin, ymin + y_offset], [xmid + x_offset, ymax]],
            [[xmin, ymin], [xmax, ymax]],
            [[xmin + x_offset, ymin], [xmax, ymid + y_offset]],
            [[xmid, ymin], [xmax, ymid]],
        )

    def __str__(self) -> str:
        return 'slant_up'


class VerticalLines(Lines):
    """
    Class for the vertical lines shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the dino dataset
            (without normalization).

        import matplotlib.pyplot as plt
        from data_morph.data.loader import DataLoader
        from data_morph.shapes.patterns import VerticalLines

        _ = VerticalLines(DataLoader.load_dataset('dino')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        x_bounds = dataset.data_bounds.x_bounds
        y_bounds = dataset.morph_bounds.y_bounds

        super().__init__(
            *[
                [[x, y_bounds[0]], [x, y_bounds[1]]]
                for x in np.linspace(x_bounds[0], x_bounds[1], 5)
            ]
        )

    def __str__(self) -> str:
        return 'v_lines'


class WideLines(Lines):
    """
    Class for the wide lines shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the dino dataset
            (without normalization).

        import matplotlib.pyplot as plt
        from data_morph.data.loader import DataLoader
        from data_morph.shapes.patterns import WideLines

        _ = WideLines(DataLoader.load_dataset('dino')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        x_bounds = dataset.data_bounds.x_bounds
        y_bounds = dataset.morph_bounds.y_bounds

        offset = x_bounds.range / 5
        lower = x_bounds[0] + offset
        upper = x_bounds[1] - offset

        super().__init__(
            [[lower, y_bounds[0]], [lower, y_bounds[1]]],
            [[upper, y_bounds[0]], [upper, y_bounds[1]]],
        )

    def __str__(self) -> str:
        return 'wide_lines'


class XLines(Lines):
    """
    Class for the X shape consisting of two crossing, perpendicular lines.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the dino dataset
            (without normalization).

        import matplotlib.pyplot as plt
        from data_morph.data.loader import DataLoader
        from data_morph.shapes.patterns import XLines

        _ = XLines(DataLoader.load_dataset('dino')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        xmin, xmax = dataset.morph_bounds.x_bounds
        ymin, ymax = dataset.morph_bounds.y_bounds

        super().__init__([[xmin, ymin], [xmax, ymax]], [[xmin, ymax], [xmax, ymin]])

    def __str__(self) -> str:
        return 'x'
