"""Factory class for generating shape objects."""

from ..data.dataset import Dataset
from . import circles, curves, patterns, polygons
from .bases.shape import Shape


class ShapeFactory:
    """
    Factory for generating shapes.

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    _SHAPE_MAPPING: dict = {
        'bullseye': circles.Bullseye,
        'circle': circles.Circle,
        'scatter': circles.Scatter,
        'down_parab': curves.DownParabola,
        'up_parab': curves.UpParabola,
        'dots': patterns.DotsGrid,
        'high_lines': patterns.HighLines,
        'h_lines': patterns.HorizontalLines,
        'slant_down': patterns.SlantDownLines,
        'slant_up': patterns.SlantUpLines,
        'v_lines': patterns.VerticalLines,
        'wide_lines': patterns.WideLines,
        'x': patterns.XLines,
        'star': polygons.Star,
    }

    AVAILABLE_SHAPES: list[str] = sorted(list(_SHAPE_MAPPING.keys()))
    """list[str]: The list of available shapes, which can be visualized with
    :meth:`.plot_available_shapes`."""

    def __init__(self, dataset: Dataset) -> None:
        self._dataset: Dataset = dataset

    def generate_shape(self, shape: str) -> Shape:
        """
        Generate the shape object based on the dataset.

        Parameters
        ----------
        shape : str
            The desired shape. See :attr:`.AVAILABLE_SHAPES`.

        Returns
        -------
        Shape
            An shape object of the requested type.
        """
        try:
            return self._SHAPE_MAPPING[shape](self._dataset)
        except KeyError:
            raise ValueError(f'No such shape as {shape}.')
