"""Pytest config."""

import pandas as pd
import pytest


@pytest.fixture(scope='session')
def sample_data():
    """Fixture for the sample data."""
    return pd.DataFrame({'x': [10, 20, 30], 'y': [50, 50, 80]})
