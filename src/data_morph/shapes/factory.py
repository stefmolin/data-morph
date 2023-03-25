"""Factory class for generating shape objects."""

from ..data.dataset import Dataset
from . import circles, lines, points, polygons
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
        'bullseye': circles.Bullseye,
        'circle': circles.Circle,
        'high_lines': lines.HighLines,
        'h_lines': lines.HorizontalLines,
        'slant_down': lines.SlantDownLines,
        'slant_up': lines.SlantUpLines,
        'v_lines': lines.VerticalLines,
        'wide_lines': lines.WideLines,
        'x': lines.XLines,
        'dots': points.DotsGrid,
        'down_parab': points.DownParabola,
        'scatter': points.Scatter,
        'up_parab': points.UpParabola,
        'rectangle': polygons.Rectangle,
        'star': polygons.Star,
    }

    def __init__(self, dataset: Dataset) -> None:
        self.dataset: Dataset = dataset

    def generate_shape(self, shape: str) -> Shape:
        """
        Generate the shape object based on the dataset.

        Parameters
        ----------
        shape : str
            The desired shape. See :attr:`AVAILABLE_SHAPES`.

        Returns
        -------
        Shape
            An shape object of the requested type.
        """
        try:
            return self.AVAILABLE_SHAPES[shape](self.dataset)
        except KeyError:
            raise ValueError(f'No such shape as {shape}.')
