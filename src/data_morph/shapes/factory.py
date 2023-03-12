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

    AVAILABLE_SHAPES: dict = {
        'circle': circles.Circle,
        'bullseye': circles.Bullseye,
        'dots': circles.Dots,
        'scatter': circles.Scatter,
        'x': patterns.XLines,
        'h_lines': patterns.HorizontalLines,
        'v_lines': patterns.VerticalLines,
        'wide_lines': patterns.WideLines,
        'high_lines': patterns.HighLines,
        'slant_up': patterns.SlantUpLines,
        'slant_down': patterns.SlantDownLines,
        'star': polygons.Star,
        'down_parab': curves.DownParabola,
        'up_parab': curves.UpParabola,
    }
    """dict[str, Shape]: A mapping of shape names to classes."""

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
            return self.AVAILABLE_SHAPES[shape](self._dataset)
        except KeyError:
            raise ValueError(f'No such shape as {shape}.')
