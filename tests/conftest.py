"""Pytest config."""

from pathlib import Path

import pandas as pd
import pytest

from data_morph.data.dataset import Dataset
from data_morph.shapes.factory import ShapeFactory


@pytest.fixture(scope='session')
def sample_data():
    """Fixture for the sample data."""
    return pd.DataFrame({'x': [10, 20, 30], 'y': [50, 50, 80]})


@pytest.fixture(scope='session')
def shape_factory(sample_data):
    """Fixture for a ShapeFactory of sample data."""
    return ShapeFactory(Dataset('sample', sample_data))


@pytest.fixture(scope='session')
def starter_shapes_dir(request):
    """Fixture for the starter shapes directory."""
    return (
        Path(request.config.rootdir) / 'src' / 'data_morph' / 'data' / 'starter_shapes'
    )
