"""Test the __main__ module."""

import pytest

from data_morph import __main__, __version__
from data_morph.data.dataset import Dataset


def test_main_version(capsys):
    """Confirm that --version works."""
    with pytest.raises(SystemExit):
        __main__.main(['--version'])
    assert f'Data Morph {__version__}' == capsys.readouterr().out.strip()


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
@pytest.mark.parametrize(
    ['value', 'reason'],
    [
        ('--', 'expected one argument'),
        ('s', 'invalid float value'),
    ],
)
@pytest.mark.parametrize('field', ['shake', 'scale'])
def test_main_bad_input_floats(field, value, reason, capsys):
    """Test that invalid input for floats is handled correctly."""
    with pytest.raises(SystemExit):
        __main__.main([f'--{field}', value, 'dino'])
    assert f'error: argument --{field}: {reason}' in capsys.readouterr().err


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


@pytest.mark.parametrize(
    ['start_shape', 'scale'],
    [['dino', 10], ['dino', 0.5], ['dino', None]],
)
def test_main_dataloader(start_shape, scale, mocker):
    """Check that the DataLoader is being used correctly."""

    bound_args = ['--scale', str(scale)] if scale else []

    load = mocker.patch.object(__main__.DataLoader, 'load_dataset', autospec=True)
    _ = mocker.patch.object(__main__.DataMorpher, 'morph')
    argv = [
        start_shape,
        '--target-shape=circle',
        *bound_args,
    ]
    __main__.main([arg for arg in argv if arg])
    load.assert_called_once_with(start_shape, scale=scale)


@pytest.mark.parametrize('flag', [True, False])
def test_main_one_shape(flag, mocker, tmp_path):
    """Check that the proper values are passed to morph a single shape."""
    init_args = {
        'decimals': 3 if flag else None,
        'seed': 1,
        'output_dir': str(tmp_path),
        'write_data': flag,
        'keep_frames': flag,
        'forward_only_animation': flag,
        'num_frames': 100,
        'in_notebook': False,
    }
    morph_args = {
        'start_shape_name': 'dino',
        'target_shape': 'circle',
        'min_shake': 0.5 if flag else None,
        'iterations': 1000,
        'freeze': 3 if flag else None,
        'ramp_in': flag,
        'ramp_out': flag,
    }

    morpher_init = mocker.patch.object(__main__.DataMorpher, '__init__', autospec=True)
    morpher_init.return_value = None
    morph_mock = mocker.patch.object(__main__.DataMorpher, 'morph', autospec=True)

    argv = [
        morph_args['start_shape_name'],
        f'--target-shape={morph_args["target_shape"]}',
        f'--iterations={morph_args["iterations"]}',
        f'--decimals={init_args["decimals"]}' if init_args['decimals'] else '',
        f'--seed={init_args["seed"]}',
        f'--output-dir={init_args["output_dir"]}',
        '--write-data' if init_args['write_data'] else '',
        '--keep-frames' if init_args['keep_frames'] else '',
        '--forward-only' if init_args['forward_only_animation'] else '',
        f'--shake={morph_args["min_shake"]}' if morph_args['min_shake'] else '',
        f'--freeze={morph_args["freeze"]}' if morph_args['freeze'] else '',
        '--ramp-in' if morph_args['ramp_in'] else '',
        '--ramp-out' if morph_args['ramp_out'] else '',
    ]
    __main__.main([arg for arg in argv if arg])

    morpher_init.assert_called_once()
    for arg, value in init_args.items():
        if arg == 'decimals' and value is None:
            value = __main__.ARG_DEFAULTS[arg]
        assert morpher_init.call_args.kwargs[arg] == value

    morph_mock.assert_called_once()
    for arg, value in morph_mock.call_args.kwargs.items():
        if arg == 'target_shape':
            assert str(value) == morph_args['target_shape']
        elif arg == 'start_shape':
            assert isinstance(value, Dataset)
            assert value.name == morph_args['start_shape_name']
        elif arg in ['freeze_for', 'min_shake']:
            arg = 'freeze' if arg == 'freeze_for' else arg
            assert value == (morph_args[arg] or __main__.ARG_DEFAULTS[arg])
        else:
            assert value == morph_args[arg]


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
            patched_options,
        )

    shapes = target_shape or patched_options

    morph_noop = mocker.patch.object(__main__.DataMorpher, 'morph', autospec=True)
    __main__.main(
        [start_shape_name, *(['--target-shape', *target_shape] if target_shape else [])]
    )
    assert morph_noop.call_count == len(shapes)
    assert (
        ''.join(
            [f'Morphing shape {i + 1} of {len(shapes)}\n' for i in range(len(shapes))]
        )
        == capsys.readouterr().err
    )
    patterns_run = [
        str(kwargs['target_shape']) for _, kwargs in morph_noop.call_args_list
    ]
    assert set(shapes).difference(patterns_run) == set()
