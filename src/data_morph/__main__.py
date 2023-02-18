"""Run data morph from start shape to end shape preserving summary statistics."""

import argparse
import os
from typing import Sequence, Union

from .data.loader import DataLoader
from .morpher import DataMorpher
from .shapes.factory import ShapeFactory


def main(argv: Union[Sequence[str], None] = None) -> None:
    """Run data morph as a module."""

    ALL_TARGETS = ShapeFactory.AVAILABLE_SHAPES.keys()

    parser = argparse.ArgumentParser(
        prog='Data Morph',
        description=(
            'Morph an input dataset of 2D points into select shapes, while '
            'preserving the summary statistics to a given number of decimal '
            'points through simulated annealing.'
        ),
        epilog=(
            'For example, morph the panda shape into a star: '
            'python -m data_morph --target-shape star panda'
        ),
    )
    parser.add_argument(
        'start_shape',
        help=(
            f'The starting shape. This could be one of {DataLoader.AVAILABLE_DATASETS} or '
            "a path to a CSV file, in which case it should have two columns 'x' and 'y'."
        ),
    )
    parser.add_argument(
        '--target-shape',
        nargs='*',
        default='all',
        help=(
            'The shape(s) to convert to. If multiple shapes are provided, the starting shape '
            'will be converted to each target shape separately. Valid target shapes are '
            f"""'{"', '".join(ALL_TARGETS)}'. Omit to convert to all target shapes in a single run."""
        ),
    )
    parser.add_argument(
        '--iterations',
        default=100000,
        type=int,
        help='The number of iterations to run. Datasets with more observations will take more iterations.',
    )
    parser.add_argument(
        '--decimals',
        default=2,
        type=int,
        choices=range(0, 6),
        help='The number of decimal places to preserve equality.',
    )
    parser.add_argument(
        '--seed',
        default=None,
        type=int,
        help='Provide a seed for reproducible results.',
    )
    parser.add_argument(
        '--output-dir',
        default=os.path.join(os.getcwd(), 'morphed_data'),
        help='Path to a directory for writing output files.',
    )
    parser.add_argument(
        '--write-data',
        default=False,
        action='store_true',
        help='Whether to write CSV files to the output directory with the data for each frame.',
    )
    parser.add_argument(
        '--ramp-in',
        default=False,
        action='store_true',
        help=(
            'Whether to slowly start the transition from input to target in '
            'the animation. This only affects the frames, not the algorithm.'
        ),
    )
    parser.add_argument(
        '--ramp-out',
        default=False,
        action='store_true',
        help=(
            'Whether to slow down the transition from input to target towards '
            'the end of the animation. This only affects the frames, not the algorithm.'
        ),
    )
    parser.add_argument(
        '--freeze',
        default=0,
        type=int,
        help=(
            'Number of frames to freeze at the first and final frame of the transition '
            'in the animation. This only affects the frames, not the algorithm.'
        ),
    )
    parser.add_argument(
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
    parser.add_argument(
        '--keep-frames',
        default=False,
        action='store_true',
        help='Whether to keep individual frame images in the output directory.',
    )

    args = parser.parse_args(argv)

    target_shapes = (
        ALL_TARGETS
        if args.target_shape == 'all'
        else set(args.target_shape).intersection(ALL_TARGETS)
    )
    if not target_shapes:
        raise ValueError(
            'No valid target shapes were provided. Valid options are '
            f"""'{"', '".join(ALL_TARGETS)}'."""
        )

    # TODO: maybe the bounds should be configurable on the command line too?
    # TODO: these bounds need to be tied into the visualization logic
    # and passed into the annealing process, but both should have them wider
    # than the data since we need flexibility to transform the data
    loader = DataLoader(bounds=[10, 90])
    start_shape_name, start_shape_data = loader.load_dataset(args.start_shape)

    shape_factory = ShapeFactory(start_shape_data)
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
            print(f'Morphing shape {i} of {total_shapes}')
        _ = morpher.morph(
            start_shape_name,
            start_shape_data,
            shape_factory.generate_shape(target_shape),
            iterations=args.iterations,
            ramp_in=args.ramp_in,
            ramp_out=args.ramp_out,
            freeze_for=args.freeze,
        )


if __name__ == '__main__':
    main()  # pragma: no cover
