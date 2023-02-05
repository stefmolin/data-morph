"""Run data morph from start shape to end shape preserving summary statistics."""

import argparse
import os

from .data_morph import run_pattern
from .load_data import load_dataset
from .shapes import ShapeFactory


def main():
    ALL_TARGETS = ShapeFactory.AVAILABLE_SHAPES.keys()

    parser = argparse.ArgumentParser(
        prog='Data Morph',
        description=(
            'Morph an input dataset of 2D points into select shapes, while '
            'preserving the summary statistics to a given number of decimal '
            'points through simulated annealing.'
        ),
        epilog = 'For example, python -m data_morph dino circle'
    )
    parser.add_argument(
        'start_shape',
        help=(
            'The starting shape. This could be something in the data folder or '
            'a path to a CSV file, in which case it should have two columns "x" and "y".'
        )
    )
    parser.add_argument(
        '--target-shape', nargs='*', default='all',
        help=(
            'The shape(s) to convert to. If multiple shapes are provided, the starting shape '
            'will be converted to each target shape separately. Valid target shapes are '
            f'{", ".join(ALL_TARGETS)}. Omit to convert to all target shapes in a single run.'
        )
    )
    parser.add_argument(
        '--iterations', default=100000, type=int, help='The number of iterations to run.'
    )
    parser.add_argument(
        '--decimals', default=2, type=int, help='The number of decimal places to preserve equality.'
    )
    parser.add_argument(
        '--output-dir', default=os.path.join(os.getcwd(), 'morphed_data'), 
        help='Path to a directory for writing output files.'
    )
    parser.add_argument(
        '--keep-frames', default=False, action='store_true',
        help='Whether to keep individual frame images in the output directory.'
    )
    parser.add_argument(
        '--write-data', default=False, action='store_true',
        help='Whether to write CSV files to the output directory with the data for each frame.'
    )
    parser.add_argument(
        '--seed', default=None, type=int,
        help='Provide a seed for reproducible results.'
    )

    args = parser.parse_args()

    target_shapes = (
        ALL_TARGETS
        if args.target_shape == 'all'
        else set(args.target_shape).intersection(ALL_TARGETS)
    )
    if not target_shapes:
        raise ValueError(
            'No valid target shapes were provided. Valid options are '
            f'{", ".join(ALL_TARGETS)}.'
        )

    start_shape_name, start_shape_data = load_dataset(args.start_shape)
    shape_factory = ShapeFactory(start_shape_data)

    for target_shape in target_shapes:
        run_pattern(
            start_shape_name, start_shape_data,
            shape_factory.generate_shape(target_shape),
            iters=args.iterations, decimals=args.decimals,
            output_dir=args.output_dir, keep_frames=args.keep_frames, 
            write_data=args.write_data, seed=args.seed,
            num_frames=100, # TODO: should this be variable?
        )


if __name__ == '__main__':
    main()
