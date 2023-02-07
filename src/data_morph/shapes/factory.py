"""Factory class for generating shape objects."""

from . import circles, curves, patterns, polygons
from .bases.shape import Shape


class ShapeFactory:
    """Factory for generating shapes."""

    AVAILABLE_SHAPES = {
        'circle': circles.Circle,
        'bullseye': circles.Bullseye,
        'dots': circles.Dots,
        'x': patterns.XLines,
        'h_lines': patterns.HorizontalLines,
        'v_lines': patterns.VerticalLines,
        'wide_lines': patterns.WideLines,
        'high_lines': patterns.HighLines,
        'slant_up': patterns.SlantUpLines,
        'slant_down': patterns.SlantDownLines,
        'star': polygons.Star,
        'down_parab': curves.DownParab,
    }

    def __init__(self, data) -> None:
        self.data = data

    def generate_shape(self, shape) -> Shape:
        """
        Generate the shape object based on the dataset.

        Parameters
        ----------
        shape : str
            The desired shape. See :attr:`AVAILABLE_SHAPES`.

        Returns
        -------
        Shape
        """
        try:
            return self.AVAILABLE_SHAPES[shape](self.data)
        except KeyError:
            raise ValueError(f'No such shape as {shape}.')
