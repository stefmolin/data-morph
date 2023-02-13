"""Tests for data_morph.morpher module."""

import pytest
from numpy.testing import assert_equal
from pandas.testing import assert_frame_equal

from data_morph.data.loader import DataLoader
from data_morph.morpher import DataMorpher
from data_morph.shapes.factory import ShapeFactory


@pytest.mark.parametrize(
    ['write_data', 'write_images'], [[True, True], [True, False], [False, True]]
)
def test_morpher_input_validation_output_dir(write_data, write_images):
    """Test input validation on output_dir."""
    with pytest.raises(ValueError, match='output_dir cannot be None if'):
        _ = DataMorpher(
            decimals=2,
            in_notebook=False,
            write_data=write_data,
            write_images=write_images,
            output_dir=None,
        )


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


@pytest.mark.parametrize('freeze_for', [-1, 0.5, 200])
def test_morpher_input_validation_freeze_for(freeze_for):
    """Test input validation on freeze_for."""
    with pytest.raises(ValueError, match='freeze_for must be a non-negative integer'):
        morpher = DataMorpher(decimals=2, in_notebook=False, output_dir='')
        _ = morpher._select_frames(
            iterations=100, ramp_in=True, ramp_out=True, freeze_for=freeze_for
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


def test_morpher_no_writing():
    """Test DataMorpher without writing any files to disk."""
    loader = DataLoader(bounds=[10, 90])
    start_shape_name, start_shape_data = loader.load_dataset('dino')

    shape_factory = ShapeFactory(start_shape_data)
    morpher = DataMorpher(
        decimals=2,
        write_images=False,
        write_data=False,
        seed=21,
        keep_frames=False,
        num_frames=100,
        in_notebook=False,
    )

    morphed_data = morpher.morph(
        start_shape_name,
        start_shape_data,
        shape_factory.generate_shape('circle'),
        iterations=1000,
        ramp_in=False,
        ramp_out=False,
        freeze_for=0,
    )

    with pytest.raises(AssertionError):
        assert_frame_equal(morphed_data, start_shape_data)
    assert morpher._is_close_enough(start_shape_data, morphed_data)
