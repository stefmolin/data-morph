"""Test the __main__ module."""

import pytest

from data_morph import __main__


def test_main_bad_shape():
    """Test that invalid target shapes raise a ValueError."""
    with pytest.raises(ValueError, match='No valid target shapes were provided.'):
        __main__.main(['dino', '--target-shape=does-not-exist'])


@pytest.mark.bad_input_to_argparse
@pytest.mark.parametrize(
    ['decimals', 'reason'],
    [(-1, 'invalid choice'), (0.5, 'invalid int value'), 
    (10, 'invalid choice'), ('s', 'invalid int value')]
)
def test_main_bad_input_decimals(decimals, reason, capsys):
    """Test that invalid input for decimals is handled correctly."""
    with pytest.raises(SystemExit):
        __main__.main(['dino', f'--decimals={decimals}'])
    assert f'error: argument --decimals: {reason}:' in capsys.readouterr().err


def test_main_one_shape(tmp_path, capsys):
    """Check stdout and stderr when running one shape."""
    iterations = 2
    __main__.main(
        [
            'dino',  # start_shape
            '--target-shape=circle',
            f'--iterations={iterations}',
            '--seed=1',
            f'--output-dir={tmp_path}',
        ]
    )

    _, err = capsys.readouterr()
    assert 'circle pattern: 100%' in err
    assert f' {iterations}/{iterations} ' in err


@pytest.mark.parametrize(
    ['target_shape', 'patched_options'],
    [
        (['star', 'bullseye'], None),
        (None, ['dots', 'x']),
    ],
    ids=['two shapes', 'all shapes'],
)
def test_main_multiple_shapes(
    target_shape, patched_options, monkeypatch, tmp_path, capsys
):
    """Check stdout and stderr when running multiple shapes."""
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
    iterations = 2
    args = [
        'dino',  # start_shape
        *(['--target-shape', *target_shape] if target_shape else []),
        f'--iterations={iterations}',
        '--seed=1',
        f'--output-dir={tmp_path}',
    ]
    __main__.main(args)

    out, err = capsys.readouterr()
    assert f' {iterations}/{iterations} ' in err

    shapes = (
        target_shape if target_shape else __main__.ShapeFactory.AVAILABLE_SHAPES.keys()
    )
    for i, shape in enumerate(shapes, start=1):
        assert f'{shape} pattern: 100%' in err
        assert f'Morphing shape {i} of {len(shapes)}\n' in out
