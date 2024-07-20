"""Test the stats module."""

import numpy as np
from numpy.testing import assert_allclose, assert_equal

from data_morph.data.loader import DataLoader
from data_morph.data.stats import (
    get_values,
    shifted_mean,
    shifted_var,
    shifted_corrcoef,
)


def test_stats():
    """Test that summary statistics tuple is correct."""

    data = DataLoader.load_dataset('dino').df

    stats = get_values(data['x'], data['y'])

    assert stats.x_mean == data.x.mean()
    assert stats.y_mean == data.y.mean()
    assert stats.x_stdev == data.x.std()
    assert stats.y_stdev == data.y.std()
    np.allclose(stats.correlation, data.corr().x.y)


def test_new_mean():
    data = DataLoader.load_dataset('dino').df

    # make sure if we don't do anything to the data that we retrieve the same results
    x = data['x'].to_numpy()

    assert_equal(np.mean(x), shifted_mean(np.mean(x), x[0], x[0], len(x)))

    # we want to test both very large and very small displacements
    for scale in [0.1, 10]:
        x_old = data['x'].to_numpy()
        y_old = data['y'].to_numpy()

        # scaling the data
        x_old /= np.max(np.abs(x_old))
        y_old /= np.max(np.abs(y_old))

        x_new = np.copy(x_old)
        y_new = np.copy(y_old)

        rng = np.random.default_rng(42)

        for _ in range(100_000):
            row = rng.integers(0, len(x_old))
            jitter_x, jitter_y = rng.normal(loc=0, scale=scale, size=2)

            x_new[row] += jitter_x
            y_new[row] += jitter_y

            meanx = np.mean(x_new)
            new_meanx = shifted_mean(np.mean(x_old), x_old[row], x_new[row], len(x_old))

            meany = np.mean(y_new)
            new_meany = shifted_mean(np.mean(y_old), y_old[row], y_new[row], len(y_old))

            assert_allclose(meanx, new_meanx)
            assert_allclose(meany, new_meany)

            x_old = np.copy(x_new)
            y_old = np.copy(y_new)


def test_new_var():
    data = DataLoader.load_dataset('dino').df

    # make sure if we don't do anything to the data that we retrieve the same results
    x = data['x'].to_numpy()

    assert_equal(np.var(x, ddof=0), shifted_var(np.mean(x), np.var(x), x[0], 0, len(x)))

    # we want to test both very large and very small displacements
    for scale in [0.1, 10]:
        x_old = data['x'].to_numpy()
        y_old = data['y'].to_numpy()

        # scaling the data
        x_old /= np.max(np.abs(x_old))
        y_old /= np.max(np.abs(y_old))

        x_new = np.copy(x_old)
        y_new = np.copy(y_old)

        rng = np.random.default_rng(42)

        for _ in range(100_000):
            row = rng.integers(0, len(x_old))
            jitter_x, jitter_y = rng.normal(loc=0, scale=scale, size=2)

            x_new[row] += jitter_x
            y_new[row] += jitter_y

            varx = np.var(x_new)
            new_varx = shifted_var(
                np.mean(x_old), np.var(x_old), x_old[row], jitter_x, len(x_old)
            )

            vary = np.var(y_new)
            new_vary = shifted_var(
                np.mean(y_old), np.var(y_old), y_old[row], jitter_y, len(y_old)
            )

            assert_allclose(varx, new_varx)
            assert_allclose(vary, new_vary)

            x_old = np.copy(x_new)
            y_old = np.copy(y_new)


def test_new_corrcoef():
    data = DataLoader.load_dataset('dino').df

    # make sure if we don't do anything to the data that we retrieve the same results
    x = data['x'].to_numpy()
    y = data['y'].to_numpy()
    corrcoef = np.corrcoef(x, y)[0, 1]
    row = 0
    new_corrcoef = shifted_corrcoef(
        x_old=x[row],
        y_old=y[row],
        x_new=x[row],
        y_new=y[row],
        meanx_old=np.mean(x),
        meany_old=np.mean(y),
        xy_old=np.mean(x * y),
        varx_old=np.var(x),
        vary_old=np.var(y),
        size=len(x),
    )

    corrcoef_by_hand = np.cov(x, y, ddof=0) / np.sqrt(np.var(x) * np.var(y))

    assert_allclose(corrcoef, corrcoef_by_hand[0, 1])
    assert_allclose(corrcoef_by_hand[0, 1], new_corrcoef)

    # we want to test both very large and very small displacements
    for scale in [0.1, 10]:
        x_old = data['x'].to_numpy()
        y_old = data['y'].to_numpy()

        # scaling the data
        x_old /= np.max(np.abs(x_old))
        y_old /= np.max(np.abs(y_old))

        x_new = np.copy(x_old)
        y_new = np.copy(y_old)

        rng = np.random.default_rng(42)

        for _ in range(100_000):
            row = rng.integers(0, len(x_old))
            jitter_x, jitter_y = rng.normal(loc=0, scale=scale, size=2)

            x_new[row] += jitter_x
            y_new[row] += jitter_y

            # corrcoef = np.corrcoef(x_new, y_new)[0, 1]
            corrcoef = (
                np.cov(x_new, y_new, ddof=0) / np.sqrt(np.var(x_new) * np.var(y_new))
            )[0, 1]
            new_corrcoef = shifted_corrcoef(
                x_old=x_old[row],
                y_old=y_old[row],
                x_new=x_new[row],
                y_new=y_new[row],
                meanx_old=np.mean(x_old),
                meany_old=np.mean(y_old),
                xy_old=np.mean(x_old * y_old),
                varx_old=np.var(x_old),
                vary_old=np.var(y_old),
                size=len(x_old),
            )

            assert_allclose(corrcoef, new_corrcoef)

            x_old = np.copy(x_new)
            y_old = np.copy(y_new)
