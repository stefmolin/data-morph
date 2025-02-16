"""Test the CLI."""

import itertools
from pathlib import Path

import pytest

from data_morph import __version__, cli
from data_morph.data.dataset import Dataset

pytestmark = pytest.mark.cli


@pytest.fixture(scope='module', params=['dino', 'sheep.csv'])
def start_shape(starter_shapes_dir, request):
    """A fixture for starter shapes both by name and file for testing."""

    def extract_starter_shape(item):
        """Determine the starter shape."""
        return str(starter_shapes_dir / item) if item.endswith('csv') else item

    if isinstance(request.param, str):
        return extract_starter_shape(request.param)
    return [extract_starter_shape(item) for item in request.param]


def test_cli_version(capsys):
    """Confirm that --version works."""
    with pytest.raises(SystemExit):
        cli.main(['--version'])
    assert f'data-morph {__version__}' == capsys.readouterr().out.strip()


def test_cli_bad_shape():
    """Test that invalid target shapes raise a ValueError."""
    with pytest.raises(ValueError, match='No valid target shapes were provided.'):
        cli.main(['--start-shape=dino', '--target-shape=does-not-exist'])


@pytest.mark.input_validation
@pytest.mark.parametrize(
    ('decimals', 'reason'),
    [
        (-1, 'invalid choice'),
        (0.5, 'invalid int value'),
        (10, 'invalid choice'),
        ('s', 'invalid int value'),
    ],
)
def test_cli_bad_input_decimals(decimals, reason, capsys):
    """Test that invalid input for decimals is handled correctly."""
    with pytest.raises(SystemExit):
        cli.main(['--start-shape=dino', f'--decimals={decimals}'])
    assert f'error: argument --decimals: {reason}:' in capsys.readouterr().err


@pytest.mark.input_validation
@pytest.mark.parametrize(
    ('value', 'reason'),
    [
        ('--', 'expected one argument'),
        ('s', 'invalid float value'),
    ],
)
@pytest.mark.parametrize('field', ['shake', 'scale'])
def test_cli_bad_input_floats(field, value, reason, capsys):
    """Test that invalid input for floats is handled correctly."""
    with pytest.raises(SystemExit):
        cli.main([f'--{field}', value, '--start-shape=dino'])
    assert f'error: argument --{field}: {reason}' in capsys.readouterr().err


@pytest.mark.input_validation
@pytest.mark.parametrize('value', [True, False, 0.1, 's'])
@pytest.mark.parametrize('field', ['iterations', 'freeze', 'seed'])
def test_cli_bad_input_integers(field, value, capsys):
    """Test that invalid input for integers is handled correctly."""
    with pytest.raises(SystemExit):
        cli.main(['--start-shape=dino', f'--{field}={value}'])
    assert f'error: argument --{field}: invalid int value:' in capsys.readouterr().err


@pytest.mark.input_validation
@pytest.mark.parametrize('value', [1, 0, 's', -1, 0.5, True, False])
@pytest.mark.parametrize(
    'field', ['ease-in', 'ease-out', 'forward-only', 'keep-frames']
)
def test_cli_bad_input_boolean(field, value, capsys):
    """Test that invalid input for Boolean switches are handled correctly."""
    with pytest.raises(SystemExit):
        cli.main(['--start-shape=dino', f'--{field}={value}'])
    assert (
        f'error: argument --{field}: ignored explicit argument'
        in capsys.readouterr().err
    )


@pytest.mark.parametrize(
    ('start_shape', 'scale'),
    [('dino', 10), ('dino', 0.5), ('dino', None)],
)
def test_cli_dataloader(start_shape, scale, mocker):
    """Check that the DataLoader is being used correctly."""

    bound_args = ['--scale', str(scale)] if scale else []

    load = mocker.patch.object(cli.DataLoader, 'load_dataset', autospec=True)
    _ = mocker.patch.object(cli.DataMorpher, 'morph')
    argv = [
        f'--start-shape={start_shape}',
        '--target-shape=circle',
        *bound_args,
    ]
    cli.main([arg for arg in argv if arg])
    load.assert_called_once_with(start_shape, scale=scale)


@pytest.mark.parametrize('flag', [True, False])
def test_cli_one_shape(start_shape, flag, mocker, tmp_path):
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
        'start_shape_name': start_shape,
        'target_shape': 'circle',
        'min_shake': 0.5 if flag else None,
        'iterations': 1000,
        'freeze': 3 if flag else None,
        'ease_in': flag,
        'ease_out': flag,
        'ease': not flag,
    }

    morpher_init = mocker.patch.object(cli.DataMorpher, '__init__', autospec=True)
    morpher_init.return_value = None
    morph_mock = mocker.patch.object(cli.DataMorpher, 'morph', autospec=True)

    argv = [
        f'--start-shape={morph_args["start_shape_name"]}',
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
        '--ease-in' if morph_args['ease_in'] else '',
        '--ease-out' if morph_args['ease_out'] else '',
        '--ease' if morph_args['ease'] else '',
    ]
    cli.main([arg for arg in argv if arg])

    morpher_init.assert_called_once()
    for arg, value in init_args.items():
        if arg == 'decimals' and value is None:
            value = cli.ARG_DEFAULTS[arg]
        assert morpher_init.call_args.kwargs[arg] == value

    morph_mock.assert_called_once()
    for arg, value in morph_mock.call_args.kwargs.items():
        if arg == 'target_shape':
            assert str(value) == morph_args['target_shape']
        elif arg == 'start_shape':
            assert isinstance(value, Dataset)
            assert value.name == Path(morph_args['start_shape_name']).stem
        elif morph_args['ease'] and arg.startswith('ease_'):
            assert value
        elif arg in ['freeze_for', 'min_shake']:
            arg = 'freeze' if arg == 'freeze_for' else arg
            assert value == (morph_args[arg] or cli.ARG_DEFAULTS[arg])
        else:
            assert value == morph_args[arg]


@pytest.mark.parametrize(
    ('target_shape', 'patched_options'),
    [
        (['star', 'bullseye'], None),
        (['all'], ['dots', 'x']),
    ],
    ids=['two shapes', 'all shapes'],
)
@pytest.mark.parametrize(
    'start_shape',
    [
        ['dino.csv'],
        ['dino', 'sheep.csv'],
    ],
    indirect=True,  # uses the start_shape fixture above to complete the CSV path if necessary
    ids=str,
)
def test_cli_multiple_shapes(
    start_shape, target_shape, patched_options, monkeypatch, tmp_path, capsys
):
    """Check that multiple morphing is working."""

    if patched_options:
        monkeypatch.setattr(
            cli.ShapeFactory,
            'AVAILABLE_SHAPES',
            patched_options,
        )

    shapes = patched_options or target_shape

    iterations = 1
    workers = 2
    cli.main(
        [
            '--start-shape',
            *start_shape,
            '--target-shape',
            *target_shape,
            f'--iterations={iterations}',
            f'--output-dir={tmp_path}',
            f'--workers={workers}',
        ]
    )

    total_morphs = len(shapes) * len(start_shape)

    out = capsys.readouterr().out
    total_iterations = total_morphs * iterations
    assert 'Overall progress' in out
    assert f'100% {total_iterations}/{total_iterations}'

    if workers >= total_morphs:
        for shape in start_shape:
            assert Path(shape).stem in out
    else:
        # only the overall progress should show up in this case
        assert len(out.splitlines()) == 1

    for dataset, shape in itertools.product(start_shape, shapes):
        assert (tmp_path / f'{Path(dataset).stem}_to_{shape}.gif').exists()
