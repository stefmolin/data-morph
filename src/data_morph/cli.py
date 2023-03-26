"""Run Data Morph CLI from start shape to end shape preserving summary statistics."""

import argparse
import sys
from pathlib import Path
from typing import Sequence, Union

from . import __version__
from .data.loader import DataLoader
from .morpher import DataMorpher
from .shapes.factory import ShapeFactory

ARG_DEFAULTS = {
    'output_dir': Path.cwd() / 'morphed_data',
    'decimals': 2,
    'min_shake': 0.3,
    'iterations': 100_000,
    'freeze': 0,
}


def main(argv: Union[Sequence[str], None] = None) -> None:
    """
    Run data morph as a script.

    Parameters
    ----------
    argv : Union[Sequence[str], None], optional
        Makes it possible to pass in options without running on
        the command line.
    """

    parser = argparse.ArgumentParser(
        prog='Data Morph',
        description=(
            'Morph an input dataset of 2D points into select shapes, while '
            'preserving the summary statistics to a given number of decimal '
            'points through simulated annealing. '
            'For example, morph the panda shape into a star:\n\t'
            'python -m data_morph --target-shape star -- panda'
        ),
        epilog=(
            'Source code available at https://github.com/stefmolin/data-morph.'
            ' Documentation is at TODO.'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        '--version', action='version', version=f'%(prog)s {__version__}'
    )

    shape_config_group = parser.add_argument_group(
        'shape config', description='Specification of start and end shapes.'
    )
    shape_config_group.add_argument(
        '--start-shape',
        required=True,
        nargs='+',
        help=(
            'The starting shape(s). A valid starting shape could be any of '
            f'{DataLoader.AVAILABLE_DATASETS} or a path to a CSV file, '
            "in which case it should have two columns 'x' and 'y'. "
            'See the documentation for visualizations of the built-in datasets.'
        ),
    )
    shape_config_group.add_argument(
        '--target-shape',
        required=True,
        nargs='+',
        help=(
            'The shape(s) to convert to. If multiple shapes are provided, the starting shape '
            'will be converted to each target shape separately. Valid target shapes are '
            f"""'{"', '".join(ShapeFactory.AVAILABLE_SHAPES)}'. Use 'all' to convert to """
            'all target shapes in a single run.'
            ' See the documentation for visualizations of the available target shapes.'
        ),
    )

    morph_config_group = parser.add_argument_group(
        'morph config', description='Configuration for the morphing process.'
    )
    morph_config_group.add_argument(
        '--decimals',
        default=ARG_DEFAULTS['decimals'],
        type=int,
        choices=range(0, 6),
        help=(
            'The number of decimal places to preserve equality. '
            f'Defaults to {ARG_DEFAULTS["decimals"]}.'
        ),
    )
    morph_config_group.add_argument(
        '--iterations',
        default=ARG_DEFAULTS['iterations'],
        type=int,
        help=(
            'The number of iterations to run. '
            f'Defaults to {ARG_DEFAULTS["iterations"]:,d}. '
            'Datasets with more observations may require more iterations.'
        ),
    )
    morph_config_group.add_argument(
        '--scale',
        default=None,
        type=float,
        help=(
            'Scale the data on both x and y by dividing by a scale factor. '
            'For example, `--scale 10` divides all x and y values by 10. '
            'Datasets with large values will morph faster after scaling down.'
        ),
    )
    morph_config_group.add_argument(
        '--seed',
        default=None,
        type=int,
        help='Provide a seed for reproducible results.',
    )
    morph_config_group.add_argument(
        '--shake',
        default=ARG_DEFAULTS['min_shake'],
        type=float,
        help=(
            'The standard deviation for the random movement applied in each '
            'direction, which will be sampled from a normal distribution with '
            'a mean of zero. Note that morphing initially sets the shake to 1, '
            'and then decreases the shake value over time toward the minimum value '
            f'defined here, which defaults to {ARG_DEFAULTS["min_shake"]}. Datasets '
            'with large values may benefit from scaling (see --scale) '
            'or increasing this towards 1, along with increasing the number of '
            'iterations (see --iterations).'
        ),
    )

    file_group = parser.add_argument_group(
        'file config',
        description='Customize where files are written to and which types of files are kept.',
    )
    file_group.add_argument(
        '--keep-frames',
        default=False,
        action='store_true',
        help=(
            'Whether to keep individual frame images in the output directory.'
            " If you don't pass this, the frames will be deleted after the GIF file"
            ' is created.'
        ),
    )
    file_group.add_argument(
        '--output-dir',
        default=ARG_DEFAULTS['output_dir'],
        help=f'Path to a directory for writing output files. Defaults to {ARG_DEFAULTS["output_dir"]}.',
    )
    file_group.add_argument(
        '--write-data',
        default=False,
        action='store_true',
        help='Whether to write CSV files to the output directory with the data for each frame.',
    )

    frame_group = parser.add_argument_group(
        'animation config', description='Customize aspects of the animation.'
    )
    frame_group.add_argument(
        '--forward-only',
        default=False,
        action='store_true',
        help=(
            'By default, this module will create an animation that plays '
            'first forward (applying the transformation) and then unwinds, '
            'playing backward to undo the transformation. Pass this argument '
            'to only play the animation in the forward direction before looping.'
        ),
    )
    frame_group.add_argument(
        '--freeze',
        default=ARG_DEFAULTS['freeze'],
        type=int,
        help=(
            'Number of frames to freeze at the first and final frame of the transition '
            'in the animation. This only affects the frames selected, not the algorithm. '
            f'Defaults to {ARG_DEFAULTS["freeze"]}.'
        ),
    )
    frame_group.add_argument(
        '--ramp-in',
        default=False,
        action='store_true',
        help=(
            'Whether to slowly start the transition from input to target in the '
            'animation. This only affects the frames selected, not the algorithm.'
        ),
    )
    frame_group.add_argument(
        '--ramp-out',
        default=False,
        action='store_true',
        help=(
            'Whether to slow down the transition from input to target towards the end '
            'of the animation. This only affects the frames selected, not the algorithm.'
        ),
    )

    args = parser.parse_args(argv)

    target_shapes = (
        ShapeFactory.AVAILABLE_SHAPES
        if args.target_shape == 'all' or 'all' in args.target_shape
        else set(args.target_shape).intersection(ShapeFactory.AVAILABLE_SHAPES)
    )
    if not target_shapes:
        raise ValueError(
            'No valid target shapes were provided. Valid options are '
            f"""'{"', '".join(ShapeFactory.AVAILABLE_SHAPES)}'."""
        )

    for start_shape in args.start_shape:
        dataset = DataLoader.load_dataset(start_shape, scale=args.scale)
        print(f"Processing starter shape '{dataset.name}'", file=sys.stderr)

        shape_factory = ShapeFactory(dataset)
        morpher = DataMorpher(
            decimals=args.decimals,
            output_dir=args.output_dir,
            write_data=args.write_data,
            seed=args.seed,
            keep_frames=args.keep_frames,
            forward_only_animation=args.forward_only,
            num_frames=100,
            in_notebook=False,
        )

        total_shapes = len(target_shapes)
        for i, target_shape in enumerate(target_shapes, start=1):
            if total_shapes > 1:
                print(f'Morphing shape {i} of {total_shapes}', file=sys.stderr)
            _ = morpher.morph(
                start_shape=dataset,
                target_shape=shape_factory.generate_shape(target_shape),
                iterations=args.iterations,
                min_shake=args.shake,
                ramp_in=args.ramp_in,
                ramp_out=args.ramp_out,
                freeze_for=args.freeze,
            )
