"""Test the stats module."""

import pytest

from data_morph.data.loader import DataLoader
from data_morph.data.stats import get_summary_statistics


@pytest.mark.parametrize('with_median', [True, False])
def test_stats(with_median):
    """Test that summary statistics tuple is correct."""

    data = DataLoader.load_dataset('dino').data

    stats = get_summary_statistics(data, with_median)

    assert stats.x_mean == data.x.mean()
    assert stats.y_mean == data.y.mean()
    assert stats.x_stdev == data.x.std()
    assert stats.y_stdev == data.y.std()
    assert stats.correlation == data.corr().x.y

    if with_median:
        assert stats.x_median == data.x.median()
        assert stats.y_median == data.y.median()
    else:
        assert stats.x_median is stats.y_median is None
