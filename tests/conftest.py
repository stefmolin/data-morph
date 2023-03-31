"""Global pytest config for data_morph tests."""

from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture(scope='session')
def sample_data():
    """Fixture for the sample data."""
    return pd.DataFrame({'x': [10, 20, 30], 'y': [50, 50, 80]})


@pytest.fixture(scope='session')
def starter_shapes_dir(request):
    """Fixture for the starter shapes directory."""
    return (
        Path(request.config.rootdir) / 'src' / 'data_morph' / 'data' / 'starter_shapes'
    )
