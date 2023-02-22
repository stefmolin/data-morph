"""Test the __main__ module."""

import unittest.mock as mock

import pandas as pd
import pytest

from data_morph import __main__


def test_main_bad_shape():
    """Test that invalid target shapes raise a ValueError."""
    with pytest.raises(ValueError, match='No valid target shapes were provided.'):
        __main__.main(['dino', '--target-shape=does-not-exist'])


@pytest.mark.bad_input_to_argparse
@pytest.mark.parametrize(
    ['decimals', 'reason'],
    [
        (-1, 'invalid choice'),
        (0.5, 'invalid int value'),
        (10, 'invalid choice'),
        ('s', 'invalid int value'),
    ],
)
def test_main_bad_input_decimals(decimals, reason, capsys):
    """Test that invalid input for decimals is handled correctly."""
    with pytest.raises(SystemExit):
        __main__.main(['dino', f'--decimals={decimals}'])
    assert f'error: argument --decimals: {reason}:' in capsys.readouterr().err


@pytest.mark.bad_input_to_argparse
@pytest.mark.parametrize('value', [True, False, 0.1, 's'])
@pytest.mark.parametrize('field', ['iterations', 'freeze', 'seed'])
def test_main_bad_input_integers(field, value, capsys):
    """Test that invalid input for integers is handled correctly."""
    with pytest.raises(SystemExit):
        __main__.main(['dino', f'--{field}={value}'])
    assert f'error: argument --{field}: invalid int value:' in capsys.readouterr().err


@pytest.mark.bad_input_to_argparse
@pytest.mark.parametrize('value', [1, 0, 's', -1, 0.5, True, False])
@pytest.mark.parametrize(
    'field', ['ramp-in', 'ramp-out', 'forward-only', 'keep-frames']
)
def test_main_bad_input_boolean(field, value, capsys):
    """Test that invalid input for Boolean switches are handled correctly."""
    with pytest.raises(SystemExit):
        __main__.main(['dino', f'--{field}={value}'])
    assert (
        f'error: argument --{field}: ignored explicit argument'
        in capsys.readouterr().err
    )


@pytest.mark.parametrize('flag', [True, False])
def test_main_one_shape(flag, mocker, tmp_path):
    """Check that the proper values are passed to morph a single shape."""
    init_args = {
        'decimals': 3 if flag else None,
        'seed': 1,
        'output_dir': tmp_path,
        'write_data': flag,
        'keep_frames': flag,
        'ramp_in': flag,
        'ramp_out': flag,
        'forward_only_animation': flag,
        'freeze': 3 if flag else None,
        'num_frames': 100,
        'in_notebook': False,
    }
    morph_args = {
        'start_shape_name': 'dino',
        'target_shape': 'circle',
        'iterations': 1000,
    }

    @mock.create_autospec
    def morph_value_check(morpher, **kwargs):
        """Replace the morph() method; first arg is the DataMorpher object."""
        # check how the DataMorpher object was created
        for arg, value in init_args.items():
            assert getattr(morpher, arg) == value

        # check the values passed to morph()
        for arg, value in morph_args.items():
            if arg == 'target_shape':
                assert str(kwargs[arg]) == value
            elif arg == 'start_shape_data':
                assert isinstance(value, pd.DataFrame)
            else:
                assert kwargs[arg] == value

    mocker.patch.object(__main__.DataMorpher, 'morph', morph_value_check)
    argv = [
        morph_args['start_shape_name'],
        f'--target-shape={morph_args["target_shape"]}',
        f'--iterations={morph_args["iterations"]}',
        f'--decimals={init_args["decimals"]}' if init_args['decimals'] else '',
        f'--freeze={init_args["freeze"]}' if init_args['freeze'] else '',
        f'--seed={init_args["seed"]}',
        f'--output-dir={init_args["output_dir"]}',
        '--write-data' if init_args['write_data'] else '',
        '--keep-frames' if init_args['keep_frames'] else '',
        '--ramp-in' if init_args['ramp_in'] else '',
        '--ramp-out' if init_args['ramp_out'] else '',
        '--forward-only' if init_args['forward_only_animation'] else '',
    ]
    __main__.main([arg for arg in argv if arg])
    morph_value_check.assert_called_once()


@pytest.mark.parametrize(
    ['target_shape', 'patched_options'],
    [
        (['star', 'bullseye'], None),
        (None, ['dots', 'x']),
    ],
    ids=['two shapes', 'all shapes'],
)
def test_main_multiple_shapes(
    target_shape, patched_options, monkeypatch, mocker, capsys
):
    """Check that multiple morphing is working."""
    start_shape_name = 'dino'

    if patched_options:
        monkeypatch.setattr(
            __main__.ShapeFactory,
            'AVAILABLE_SHAPES',
            {
                shape: cls
                for shape, cls in __main__.ShapeFactory.AVAILABLE_SHAPES.items()
                if shape in patched_options
            },
        )

    shapes = (
        target_shape if target_shape else __main__.ShapeFactory.AVAILABLE_SHAPES.keys()
    )

    shapes_completed = []

    @mock.create_autospec
    def mock_morph(_, **kwargs):
        """Mock the DataMorpher.morph() method to check input and track progress."""
        assert kwargs['start_shape_name'] == start_shape_name
        shapes_completed.append(str(kwargs['target_shape']))

    mocker.patch.object(__main__.DataMorpher, 'morph', mock_morph)
    __main__.main(
        [start_shape_name, *(['--target-shape', *target_shape] if target_shape else [])]
    )
    assert mock_morph.call_count == len(shapes)
    assert set(shapes_completed).difference(shapes) == set()
    assert (
        ''.join(
            [f'Morphing shape {i + 1} of {len(shapes)}\n' for i in range(len(shapes))]
        )
        == capsys.readouterr().err
    )
