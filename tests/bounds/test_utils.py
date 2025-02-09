"""Test the _utils module."""

import pytest

from data_morph.bounds._utils import _validate_2d


@pytest.mark.bounds
@pytest.mark.input_validation
@pytest.mark.parametrize(
    ('data', 'msg'),
    [
        (True, 'must be an iterable of 2 numeric values'),
        ({1, 2}, 'must be an iterable of 2 numeric values'),
        ('12', 'must be an iterable of 2 numeric values'),
        ([0, False], 'must be an iterable of 2 numeric values'),
        ([1, 2], False),
    ],
    ids=['True', '{1, 2}', '12', '[0, False]', '[1, 2]'],
)
def test_validate_2d(data, msg):
    """Test that 2D numeric value check is working."""
    if msg:
        with pytest.raises(ValueError, match=msg):
            _ = _validate_2d(data, 'test')
    else:
        assert data == _validate_2d(data, 'test')
