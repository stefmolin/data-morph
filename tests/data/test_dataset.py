"""Test the dataset module."""

import pandas as pd
import pytest
from numpy.testing import assert_equal
from pandas.testing import assert_frame_equal

from data_morph.bounds.bounding_box import BoundingBox
from data_morph.data.dataset import Dataset
from data_morph.data.loader import DataLoader


@pytest.mark.dataset
class TestDataset:
    """Test the Dataset class."""

    @pytest.mark.parametrize('scale', [10, 0.5, None])
    def test_scale_data(self, scale, starter_shapes_dir):
        """Confirm that data scaling is working by checking min and max."""

        original_data = pd.read_csv(starter_shapes_dir / 'dino.csv')
        original_min = original_data.min()
        original_max = original_data.max()

        dataset = DataLoader.load_dataset('dino', scale=scale)

        if scale:
            assert_equal(dataset.data.min().to_numpy(), original_min / scale)
            assert_equal(dataset.data.max().to_numpy(), original_max / scale)
        else:
            assert_frame_equal(dataset.data, original_data)

    @pytest.mark.input_validation
    @pytest.mark.parametrize(
        'scale',
        [[3], (), '', '12', True, False, 0],
        ids=str,
    )
    def test_scale_data_invalid_scale(self, scale):
        """Confirm that scaling doesn't happen unless scale is valid."""
        if scale is not False and scale == 0:
            exc = ValueError
            msg = 'scale must be non-zero'
        else:
            exc = TypeError
            msg = 'scale must be a numeric value'

        with pytest.raises(exc, match=msg):
            _ = DataLoader.load_dataset('dino', scale=scale)

    @pytest.mark.input_validation
    def test_validate_data_missing_columns(self, starter_shapes_dir):
        """Confirm that creation of a Dataset validates the DataFrame columns."""

        data = pd.read_csv(starter_shapes_dir / 'dino.csv').rename(columns={'x': 'a'})

        with pytest.raises(ValueError, match='Columns "x" and "y" are required.'):
            _ = Dataset('dino', data)

    def test_validate_data_fix_column_casing(self, starter_shapes_dir):
        """Confirm that creating a Dataset with correct names but in wrong casing works."""

        data = pd.read_csv(starter_shapes_dir / 'dino.csv').rename(columns={'x': 'X'})
        dataset = Dataset('dino', data)
        assert not dataset.data[list(dataset._REQUIRED_COLUMNS)].empty

    @pytest.mark.bounds
    @pytest.mark.parametrize(
        ('scale', 'data_bounds', 'morph_bounds', 'plot_bounds'),
        [
            (
                10,
                [[2.23077, 9.82051], [0.29487, 9.94872]],
                [[1.4717959999999999, 10.579484], [-0.670515, 10.914105]],
                [[-0.7320549999999985, 12.783335], [-1.6359, 11.879489999999999]],
            ),
            (
                0.5,
                [[44.6154, 196.4102], [5.8974, 198.9744]],
                [[29.43592, 211.58968000000002], [-13.4103, 218.2821]],
                [
                    [-14.641100000000009, 255.66670000000005],
                    [-32.718, 237.58980000000003],
                ],
            ),
            (
                None,
                [[22.3077, 98.2051], [2.9487, 99.4872]],
                [[14.71796, 105.79484000000001], [-6.70515, 109.14105]],
                [
                    [-7.320550000000004, 127.83335000000002],
                    [-16.359, 118.79490000000001],
                ],
            ),
        ],
    )
    def test_derive_bounds(self, scale, data_bounds, morph_bounds, plot_bounds):
        """Test that the _derive_*_bounds() methods are working."""
        dataset = DataLoader.load_dataset('dino', scale=scale)

        assert dataset.data_bounds == BoundingBox(*data_bounds)
        assert dataset.morph_bounds == BoundingBox(*morph_bounds)
        assert dataset.plot_bounds == BoundingBox(*plot_bounds)

    @pytest.mark.parametrize('scale', [10, None])
    def test_repr(self, scale):
        """Check that the __repr__() method is working."""

        dataset = DataLoader.load_dataset('dino', scale=scale)
        assert repr(dataset) == (f'<Dataset name=dino scaled={scale is not None}>')
