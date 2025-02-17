"""Test the data_morph.morpher module."""

import re
from functools import partial

import pandas as pd
import pytest
from numpy.testing import assert_equal
from pandas.testing import assert_frame_equal

from data_morph.data.loader import DataLoader
from data_morph.morpher import DataMorpher
from data_morph.shapes.factory import ShapeFactory


@pytest.mark.morpher
class TestDataMorpher:
    """Test the DataMorpher class."""

    @pytest.fixture(scope='class')
    def morph_partial(self):
        """Fixture providing a partial morph() method with start and target specified."""
        morpher = DataMorpher(decimals=2, in_notebook=False, output_dir='')
        dataset = DataLoader.load_dataset('dino')
        return partial(
            morpher.morph,
            start_shape=dataset,
            target_shape=ShapeFactory(dataset).generate_shape('circle'),
        )

    @pytest.mark.input_validation
    @pytest.mark.parametrize(
        ('write_data', 'write_images'), [(True, True), (True, False), (False, True)]
    )
    def test_input_validation_output_dir(self, write_data, write_images):
        """Test input validation on output_dir."""
        with pytest.raises(ValueError, match='output_dir cannot be None if'):
            _ = DataMorpher(
                decimals=2,
                in_notebook=False,
                write_data=write_data,
                write_images=write_images,
                output_dir=None,
            )

    @pytest.mark.input_validation
    @pytest.mark.parametrize('decimals', [5.5, -1, 0.5, 6, True, 's'])
    def test_input_validation_decimals(self, decimals):
        """Test input validation on decimals."""
        with pytest.raises(ValueError, match='decimals must be a non-negative integer'):
            _ = DataMorpher(decimals=decimals, in_notebook=False, output_dir='')

    @pytest.mark.input_validation
    @pytest.mark.parametrize('num_frames', [-1, 0, 0.5, 200, True, 's'])
    def test_input_validation_num_frames(self, num_frames):
        """Test input validation on num_frames."""
        with pytest.raises(ValueError, match='num_frames must be a positive integer'):
            _ = DataMorpher(
                decimals=2, in_notebook=False, output_dir='', num_frames=num_frames
            )

    @pytest.mark.input_validation
    @pytest.mark.parametrize('freeze_for', [-1, 0.5, 200, True, 's'])
    def test_input_validation_freeze_for(self, freeze_for):
        """Test input validation on freeze_for."""
        morpher = DataMorpher(decimals=2, in_notebook=False, output_dir='')

        with pytest.raises(
            ValueError, match='freeze_for must be a non-negative integer'
        ):
            _ = morpher._select_frames(
                iterations=100, ease_in=True, ease_out=True, freeze_for=freeze_for
            )

    @pytest.mark.input_validation
    @pytest.mark.parametrize('iterations', [-1, 0.5, 's'])
    def test_input_validation_iterations(self, iterations):
        """Test input validation on iterations."""
        morpher = DataMorpher(decimals=2, in_notebook=False, output_dir='')

        with pytest.raises(ValueError, match='iterations must be a positive integer'):
            _ = morpher._select_frames(
                iterations=iterations, ease_in=True, ease_out=True, freeze_for=0
            )

    @pytest.mark.parametrize(
        ('ease_in', 'ease_out', 'expected_frames'),
        [
            (True, True, [0, 1, 2, 5, 8, 12, 15, 18, 19]),
            (True, False, [0, 0, 1, 3, 5, 7, 10, 13, 17]),
            (False, True, [0, 3, 7, 10, 13, 15, 17, 19, 20]),
            (False, False, [0, 2, 4, 7, 9, 11, 13, 16, 18]),
        ],
    )
    def test_frames(self, ease_in, ease_out, expected_frames):
        """Confirm that frames produced by the _select_frames() method are correct."""
        freeze_for = 2
        iterations = 20

        morpher = DataMorpher(
            decimals=2, in_notebook=False, output_dir='', num_frames=10
        )
        frames = morpher._select_frames(
            iterations=iterations,
            ease_in=ease_in,
            ease_out=ease_out,
            freeze_for=freeze_for,
        )

        assert_equal(frames[:freeze_for], [0] * freeze_for)
        assert_equal(frames[-freeze_for:], [iterations] * freeze_for)
        assert_equal(frames[freeze_for:-freeze_for], expected_frames)

    @pytest.mark.input_validation
    @pytest.mark.parametrize('name', ['min_shake', 'max_shake', 'min_temp', 'max_temp'])
    @pytest.mark.parametrize('value', [-1, 1.5, 's', False])
    def test_morph_input_validation(self, morph_partial, name, value):
        """Test input validation for the morph() method."""
        with pytest.raises(ValueError, match=f'{name} must be a number >= 0 and <= 1'):
            _ = morph_partial(**{name: value})

    @pytest.mark.input_validation
    @pytest.mark.parametrize('name', ['shake', 'temp'])
    @pytest.mark.parametrize(
        ('min_value', 'max_value'),
        [(0, 0), (1, 1), (0.5, 0.5), (0.5, 0.25)],
    )
    def test_morph_input_validation_shake_and_temp_range(
        self, morph_partial, name, min_value, max_value
    ):
        """Test input validation of the temp and shake ranges for the morph() method."""
        with pytest.raises(
            ValueError, match=f'max_{name} must be greater than min_{name}'
        ):
            _ = morph_partial(**{f'min_{name}': min_value, f'max_{name}': max_value})

    @pytest.mark.input_validation
    @pytest.mark.parametrize('value', [-1, 's', False])
    def test_morph_input_validation_allowed_dist(self, morph_partial, value):
        """Test input validation for allowed_dist in the morph() method."""
        with pytest.raises(
            ValueError, match='allowed_dist must be a non-negative numeric value'
        ):
            _ = morph_partial(allowed_dist=value)

    def test_no_writing(self, capsys):
        """Test running the morph() method without writing any files to disk."""
        dataset = DataLoader.load_dataset('dino')

        shape_factory = ShapeFactory(dataset)
        morpher = DataMorpher(
            decimals=2,
            write_images=False,
            write_data=False,
            seed=21,
            keep_frames=False,
            num_frames=100,
            in_notebook=False,
        )

        target_shape = 'circle'
        iterations = 1000

        morphed_data = morpher.morph(
            start_shape=dataset,
            target_shape=shape_factory.generate_shape(target_shape),
            iterations=iterations,
            ease_in=False,
            ease_out=False,
            freeze_for=0,
        )

        with pytest.raises(AssertionError):
            assert_frame_equal(morphed_data, dataset.data)
        assert morpher._is_close_enough(dataset.data, morphed_data)

        out, _ = capsys.readouterr()
        assert f'{dataset.name} to {target_shape}' in out
        assert f' {iterations}/{iterations} ' in out

    def test_saving_data(self, tmp_path):
        """Test that writing files to disk in the morph() method is working."""
        num_frames = 5
        iterations = 10
        start_shape = 'dino'
        target_shape = 'circle'

        dataset = DataLoader.load_dataset(start_shape)
        base_file_name = f'{dataset.name}-to-{target_shape}'

        shape_factory = ShapeFactory(dataset)
        morpher = DataMorpher(
            decimals=2,
            write_images=True,
            write_data=True,
            output_dir=tmp_path,
            seed=21,
            keep_frames=True,
            num_frames=num_frames,
            in_notebook=False,
        )

        morphed_data = morpher.morph(
            start_shape=dataset,
            target_shape=shape_factory.generate_shape(target_shape),
            iterations=iterations,
            ease_in=False,
            ease_out=False,
            freeze_for=0,
        )

        frame_number_format = f'{{:0{len(str(iterations))}d}}'.format

        # we don't save the data for the first frame since it is in the input data
        assert not (
            tmp_path / f'{base_file_name}-data-{frame_number_format(0)}.csv'
        ).is_file()

        # make sure we have the correct number of files
        for kind in ['png', 'csv']:
            assert len(list(tmp_path.glob(f'{base_file_name}*.{kind}'))) == num_frames

        # at the final frame, we have the output data
        assert_frame_equal(
            pd.read_csv(
                tmp_path
                / f'{base_file_name}-data-{frame_number_format(iterations)}.csv'
            ),
            morphed_data,
        )

        # other frames shouldn't have the same data
        with pytest.raises(AssertionError):
            assert_frame_equal(
                pd.read_csv(
                    tmp_path / f'{base_file_name}-data-{frame_number_format(8)}.csv'
                ),
                morphed_data,
            )

        # confirm the animation was created
        assert (tmp_path / f'{dataset.name}_to_{target_shape}.gif').is_file()

    @pytest.mark.parametrize('write_images', [True, False])
    @pytest.mark.parametrize('start_frame', [0, 1, 20])
    def test_record_frames(self, write_images, start_frame, tmp_path):
        """Confirm that _record_frames() is working."""
        dataset = DataLoader.load_dataset('dino')
        morpher = DataMorpher(
            decimals=2,
            write_images=write_images,
            write_data=False,
            output_dir=tmp_path,
            seed=21,
            keep_frames=True,
            num_frames=20,
            in_notebook=False,
        )

        frame_number = f'{start_frame:03d}'

        base_path = 'test-freeze'
        morpher._record_frames(
            dataset.data,
            dataset.plot_bounds,
            base_path,
            frame_number,
        )

        images = list(tmp_path.glob(f'{base_path}*.png'))

        assert len(images) == int(write_images)
        if write_images:
            assert re.search(r'\d{3}', images[0].stem).group(0) == frame_number
