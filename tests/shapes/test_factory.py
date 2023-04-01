"""Test the factory module."""

import pytest


@pytest.mark.shapes
class TestShapeFactory:
    """Test the ShapeFactory class."""

    def test_generate_shape(self, shape_factory):
        """Test the generate_shape() method on a valid shape."""
        for shape_name, shape_type in shape_factory._SHAPE_MAPPING.items():
            shape = shape_factory.generate_shape(shape_name)
            assert isinstance(shape, shape_type)
            assert shape_name == str(shape)

    def test_generate_shape_error(self, shape_factory):
        """Test the generate_shape() method on a non-existent shape."""
        with pytest.raises(ValueError, match='No such shape'):
            _ = shape_factory.generate_shape('does not exist')
