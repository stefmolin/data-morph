"""Test shape classes."""

import pandas as pd
import pytest

from data_morph.shapes.bases.shape import Shape
from data_morph.shapes.factory import ShapeFactory


@pytest.fixture
def sample_data():
    """Fixture for the sample data."""
    return pd.DataFrame({'x': [10, 20, 30], 'y': [50, 50, 80]})


def test_shape_factory(sample_data):
    """Test the ShapeFactory class."""

    shape_factory = ShapeFactory(sample_data)

    for shape_name, shape_type in shape_factory.AVAILABLE_SHAPES.items():
        shape = shape_factory.generate_shape(shape_name)
        assert isinstance(shape, shape_type)
        assert shape_name == str(shape)

    with pytest.raises(ValueError, match='No such shape'):
        _ = shape_factory.generate_shape('does not exist')


def test_shape_abc():
    """Test that Shape class can't be instantiated directly."""
    with pytest.raises(TypeError):
        _ = Shape()

    class NewShape(Shape):
        def distance(self):
            return super().distance(0, 0)

    with pytest.raises(NotImplementedError):
        NewShape().distance()


def test_circle(sample_data):
    """Test the Circle class."""
    circle = ShapeFactory(sample_data).generate_shape('circle')
    assert circle.distance(20, 50) == 20.0


def test_bullseye(sample_data):
    """Test the Bullseye class."""
    bullseye = ShapeFactory(sample_data).generate_shape('bullseye')
    assert bullseye.distance(20, 50) == 8.0


def test_dots(sample_data):
    """Test the Dots class."""
    dots = ShapeFactory(sample_data).generate_shape('dots')
    assert dots.distance(20, 50) == 0.0
