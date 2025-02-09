"""Test the stats module."""

import numpy as np

from data_morph.data.loader import DataLoader
from data_morph.data.stats import get_values


def test_stats():
    """Test that summary statistics tuple is correct."""

    data = DataLoader.load_dataset('dino').df

    stats = get_values(data['x'], data['y'])

    assert stats.x_mean == data.x.mean()
    assert stats.y_mean == data.y.mean()
    assert stats.x_stdev == data.x.std()
    assert stats.y_stdev == data.y.std()
    np.allclose(stats.correlation, data.corr().x.y)
