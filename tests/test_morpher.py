"""Tests for data_morph.morpher module."""

import pytest
from numpy.testing import assert_equal

from data_morph.morpher import DataMorpher


@pytest.mark.parametrize('decimals', [5.5, -1, 0.5, 6])
def test_morpher_input_validation_decimals(decimals):
    """Test input validation on decimals."""
    with pytest.raises(ValueError, match='decimals must be a non-negative integer'):
        _ = DataMorpher(decimals=decimals, in_notebook=False, output_dir='')


@pytest.mark.parametrize('num_frames', [-1, 0, 0.5, 200])
def test_morpher_input_validation_num_frames(num_frames):
    """Test input validation on num_frames."""
    with pytest.raises(ValueError, match='num_frames must be a positive integer'):
        _ = DataMorpher(
            decimals=2, in_notebook=False, output_dir='', num_frames=num_frames
        )


@pytest.mark.parametrize(
    ['ramp_in', 'ramp_out', 'expected_frames'],
    [
        (True, True, [0, 1, 2, 5, 8, 12, 15, 18, 19]),
        (True, False, [0, 0, 1, 3, 5, 7, 10, 13, 17]),
        (False, True, [0, 3, 7, 10, 13, 15, 17, 19, 20]),
        (False, False, [0, 2, 4, 7, 9, 11, 13, 16, 18]),
    ],
)
def test_morpher_frames(ramp_in, ramp_out, expected_frames):
    """Confirm that frames are correct."""
    freeze_for = 2
    iterations = 20

    morpher = DataMorpher(decimals=2, in_notebook=False, output_dir='', num_frames=10)
    frames = morpher._select_frames(
        iterations=iterations, ramp_in=ramp_in, ramp_out=ramp_out, freeze_for=freeze_for
    )

    assert_equal(frames[:freeze_for], [0] * freeze_for)
    assert_equal(frames[-freeze_for:], [iterations] * freeze_for)
    assert_equal(frames[freeze_for:-freeze_for], expected_frames)
