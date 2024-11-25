"""Factory class for generating shape objects."""

from itertools import zip_longest
from numbers import Number
from typing import ClassVar

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from ..data.dataset import Dataset
from ..plotting.style import plot_with_custom_style
from .bases.shape import Shape
from .circles import Bullseye, Circle, Rings
from .lines import (
    Diamond,
    HighLines,
    HorizontalLines,
    Rectangle,
    SlantDownLines,
    SlantUpLines,
    Star,
    VerticalLines,
    WideLines,
    XLines,
)
from .points import (
    Club,
    DotsGrid,
    DownParabola,
    Heart,
    LeftParabola,
    RightParabola,
    Scatter,
    Spade,
    UpParabola,
)


class ShapeFactory:
    """
    Factory for generating shape objects based on data.

    .. plot::
       :caption:
            Target shapes currently available.

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.factory import ShapeFactory

        dataset = DataLoader.load_dataset('panda')
        _ = ShapeFactory(dataset).plot_available_shapes()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    _SHAPE_MAPPING: ClassVar[dict[str, type[Shape]]] = {
        'bullseye': Bullseye,
        'circle': Circle,
        'high_lines': HighLines,
        'h_lines': HorizontalLines,
        'slant_down': SlantDownLines,
        'slant_up': SlantUpLines,
        'v_lines': VerticalLines,
        'wide_lines': WideLines,
        'x': XLines,
        'dots': DotsGrid,
        'down_parab': DownParabola,
        'heart': Heart,
        'left_parab': LeftParabola,
        'scatter': Scatter,
        'right_parab': RightParabola,
        'up_parab': UpParabola,
        'diamond': Diamond,
        'rectangle': Rectangle,
        'rings': Rings,
        'star': Star,
        'club': Club,
        'spade': Spade,
    }

    AVAILABLE_SHAPES: list[str] = sorted(_SHAPE_MAPPING.keys())
    """list[str]: The list of available shapes, which can be visualized with
    :meth:`.plot_available_shapes`."""

    def __init__(self, dataset: Dataset) -> None:
        self._dataset: Dataset = dataset

    def generate_shape(self, shape: str, **kwargs: Number) -> Shape:
        """
        Generate the shape object based on the dataset.

        Parameters
        ----------
        shape : str
            The desired shape. See :attr:`.AVAILABLE_SHAPES`.
        **kwargs
            Additional keyword arguments to pass down when creating
            the shape.

        Returns
        -------
        Shape
            An shape object of the requested type.
        """
        try:
            return self._SHAPE_MAPPING[shape](self._dataset, **kwargs)
        except KeyError as err:
            raise ValueError(f'No such shape as {shape}.') from err

    @plot_with_custom_style
    def plot_available_shapes(self) -> Axes:
        """
        Plot the available target shapes.

        Returns
        -------
        matplotlib.axes.Axes
            The :class:`~matplotlib.axes.Axes` object containing the plot.

        See Also
        --------
        AVAILABLE_SHAPES
            The list of available shapes.
        """
        num_cols = 5
        num_plots = len(self.AVAILABLE_SHAPES)
        num_rows = int(np.ceil(num_plots / num_cols))

        fig, axs = plt.subplots(
            num_rows,
            num_cols,
            layout='constrained',
            figsize=(10, 2 * num_rows),
        )
        fig.get_layout_engine().set(w_pad=0.2, h_pad=0.2)

        for shape, ax in zip_longest(self.AVAILABLE_SHAPES, axs.flatten()):
            if shape:
                ax.tick_params(
                    axis='both',
                    which='both',
                    bottom=False,
                    left=False,
                    right=False,
                    labelbottom=False,
                    labelleft=False,
                )
                shape_obj = self.generate_shape(shape)
                ax = shape_obj.plot(ax=ax).set(
                    xlabel='', ylabel='', title=str(shape_obj)
                )
            else:
                ax.remove()
        return axs
