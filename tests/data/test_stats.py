"""Test the stats module."""

from data_morph.data.loader import DataLoader
from data_morph.data.stats import get_summary_statistics


def test_stats():
    """Test that summary statistics tuple is correct."""

    data = DataLoader.load_dataset('dino').data

    stats = get_summary_statistics(data)

    assert stats.x_mean == data.x.mean()
    assert stats.y_mean == data.y.mean()
    assert stats.x_stdev == data.x.std()
    assert stats.y_stdev == data.y.std()
    assert stats.correlation == data.corr().x.y
