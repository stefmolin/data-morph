"""Test shape classes."""

import pandas as pd
import pytest

from data_morph.shapes.factory import ShapeFactory


def test_shape_factory():
    """Test the ShapeFactory class."""
    data = pd.DataFrame({'x': [10, 20, 30], 'y': [50, 50, 80]})

    shape_factory = ShapeFactory(data)

    for shape_name, shape_type in shape_factory.AVAILABLE_SHAPES.items():
        shape = shape_factory.generate_shape(shape_name)
        assert isinstance(shape, shape_type)

    with pytest.raises(ValueError, match='No such shape'):
        _ = shape_factory.generate_shape('does not exist')
