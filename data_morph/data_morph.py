"""
Morph an input dataset of 2D points into select shapes, while preserving the summary
statistics to a given number of decimal points through simulated annealing.

.. note::
    This code has been altered by Stefanie Molin to work for other input datasets
    by parameterizing the target shapes with information from the input shape.
    The original code works for a specific dataset called the "dinosaurus" and was created
    for the paper "Same Stats, Different Graphs: Generating Datasets with Varied Appearance and
    Identical Statistics through Simulated Annealing" by Justin Matejka and George Fitzmaurice
    (ACM CHI 2017).

    The paper, video, and associated code and datasets can be found on the
    Autodesk Research website `here <https://www.autodeskresearch.com/publications/samestats>`_.
"""

import argparse
from functools import wraps
import itertools
from importlib.resources import files, as_file
import math
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytweening
import seaborn as sns
import tqdm


# TODO: make a constants file or something for this stuff
MAIN_DIR = 'data_morph'
DATA_DIR = 'data'
DATASETS = {
    'dino': 'dino.csv',
}
LINE_SHAPES = [
    'x', 'h_lines', 'v_lines', 'wide_lines', 'high_lines', 'slant_up',
    'slant_down', 'center', 'star', 'down_parab'
]
ALL_TARGETS = LINE_SHAPES + ['circle', 'bullseye', 'dots']
INITIAL_DATASETS = ['dino']


def plot_with_custom_style(plotting_function):
    @wraps(plotting_function)
    def plot_in_style(*args, **kwargs):
        style = files(MAIN_DIR).joinpath('plot_style.mplstyle')
        with as_file(style) as style_path:
            with plt.style.context(style_path):
                output = plotting_function(*args, **kwargs)
        return output
    return plot_in_style

def load_dataset(dataset):
    """Loads the example data sets used in the paper.

    Args:
        name (str): One of 'dino', 'rando', 'slant', or 'big_slant'

    Returns:
        pd.DataFrame: A ``DataFrame`` with ``x`` and ``y`` columns
    """
    try:
        return pd.read_csv(files(MAIN_DIR).joinpath(f'{DATA_DIR}/{DATASETS[dataset]}'))
    except KeyError:
        try:
            # TODO: for custom datasets we need to scale it to be within the 
            # bounds of the target datasets or find a map to map the logic to
            # target dataset values dynamically
            return pd.read_csv(dataset)
        except FileNotFoundError:
            raise ValueError(
                f'Unknown dataset "{dataset}". '
                'Provide a valid path to a CSV dataset or use one of '
                f'the included datasets: {", ".join(DATASETS.keys())}.'
            )


def get_values(df):
    """Calculates the summary statistics for the given set of points

    Args:
        df (pd.DataFrame): A ``DataFrame`` with ``x`` and ``y`` columns

    Returns:
        list: ``[x-mean, y-mean, x-stdev, y-stdev, correlation]``
    """
    xm = df.x.mean()
    ym = df.y.mean()
    xsd = df.x.std()
    ysd = df.y.std()
    pc = df.corr().x.y

    return [xm, ym, xsd, ysd, pc]


def is_error_still_ok(df1, df2, decimals=2):
    """Checks to see if the statistics are still within the acceptable bounds

    Args:
        df1 (pd.DataFrame): The original data set
        df2 (pd.DataFrame): The test data set
        decimals (int):     The number of decimals of precision to check

    Returns:
        bool: ``True`` if the maximum error is acceptable, ``False`` otherwise
    """
    r1 = get_values(df1)
    r2 = get_values(df2)

    # check each of the error values to check if they are the same to the
    # correct number of decimals
    r1 = [math.floor(r * 10**decimals) for r in r1]
    r2 = [math.floor(r * 10**decimals) for r in r2]

    # we are good if r1 and r2 have the same numbers
    er = np.subtract(r1, r2)
    er = [abs(n) for n in er]

    return np.max(er) == 0


def line_magnitude(x1, y1, x2, y2):
    """Calculates the distance between ``(x1, y1)`` and ``(x2, y2)``

    Args:
        x1 (float): The x coordinate of the first point
        y1 (float): The y coordinate of the first point
        x2 (float): The x coordinate of the second point
        y2 (float): The y coordinate of the second point
    """
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def distance_point_line(px, py, x1, y1, x2, y2):
    """Calculates the minimum distance between a point and a line, used to
    determine if the points are getting closer to the target. Implementation
    based on `this VBA code`_

    .. this VBA code: http://local.wasp.uwa.edu.au/~pbourke/geometry/pointline/source.vba
    """
    line_mag = line_magnitude(x1, y1, x2, y2)

    if line_mag < 0.00000001:
        # Arbitrarily large value
        return 9999

    u1 = (((px - x1) * (x2 - x1)) + ((py - y1) * (y2 - y1)))
    u = u1 / (line_mag * line_mag)

    if (u < 0.00001) or (u > 1):
        # closest point does not fall within the line segment, take the shorter
        # distance to an endpoint
        ix = line_magnitude(px, py, x1, y1)
        iy = line_magnitude(px, py, x2, y2)
        if ix > iy:
            distance = iy
        else:
            distance = ix
    else:
        # Intersecting point is on the line, use the formula
        ix = x1 + u * (x2 - x1)
        iy = y1 + u * (y2 - y1)
        distance = line_magnitude(px, py, ix, iy)

    return distance

@plot_with_custom_style
def plot(df, save_to, **save_kwds):
    """Creates a plot which shows both the plot and the statistical summary

    Args:
        df (pd.DataFrame):  The data set to plot
    """
    y_offset = 0
    fig, ax = plt.subplots(figsize=(12, 5), layout='constrained')
    ax.scatter(df.x, df.y, s=50, alpha=0.7, color='black')
    ax.set(xlim=(0, 105), ylim=(y_offset, 105))

    res = get_values(df)
    fs = 30

    labels = ('X Mean', 'Y Mean', 'X SD', 'Y SD', 'Corr.')
    max_label_length = max([len(l) for l in labels])

    # If `max_label_length = 10`, this string will be "{:<10}: {:0.9f}", then we
    # can pull the `.format` method for that string to reduce typing it
    # repeatedly
    formatter = '{{:<{pad}}}: {{:0.9f}}'.format(pad=max_label_length).format
    corr_formatter = '{{:<{pad}}}: {{:+.9f}}'.format(pad=max_label_length).format

    opts = dict(fontsize=fs, alpha=0.3)
    ax.text(110, y_offset + 80, formatter(labels[0], res[0])[:-2], **opts)
    ax.text(110, y_offset + 65, formatter(labels[1], res[1])[:-2], **opts)
    ax.text(110, y_offset + 50, formatter(labels[2], res[2])[:-2], **opts)
    ax.text(110, y_offset + 35, formatter(labels[3], res[3])[:-2], **opts)
    ax.text(110, y_offset + 20, corr_formatter(labels[4], res[4], pad=max_label_length)[:-2], **opts)

    opts['alpha'] = 1
    ax.text(110, y_offset + 80, formatter(labels[0], res[0])[:-7], **opts)
    ax.text(110, y_offset + 65, formatter(labels[1], res[1])[:-7], **opts)
    ax.text(110, y_offset + 50, formatter(labels[2], res[2])[:-7], **opts)
    ax.text(110, y_offset + 35, formatter(labels[3], res[3])[:-7], **opts)
    ax.text(110, y_offset + 20, corr_formatter(labels[4], res[4], pad=max_label_length)[:-7], **opts)

    if not save_to:
        return ax

    dirname = os.path.dirname(save_to)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    fig.savefig(save_to, **save_kwds)
    plt.close(fig)

def dist(p1, p2):
    """Calculates the Euclidean distance between ``p1`` and ``p2`` where these
    are 2-tuples (or lists, numpy arrays, etc).

    Args:
        p1 ((float, float)): The first point
        p2 ((float, float)): The second point
    """
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def average_location(pairs):
    """Calculates the average of all the x-coordinates and y-coordinates of the
    pairs given. In other words, if ``pairs`` is a list of ``[(x_i, y_i)]``
    points, then this calculates ``[(mean(x_i), mean(y_i))]``.
    """
    return np.mean(pairs, axis=1)


def get_points_for_shape(line_shape):
    """These are the hard-coded shapes which we perturb towards. It would useful
    to have a tool for drawing these shapes instead
    """
    lines = []
    if line_shape == 'x':
        l1 = [[20, 0], [100, 100]]
        l2 = [[20, 100], [100, 0]]
        lines = [l1, l2]
    elif line_shape == "h_lines":
        lines = [[[0, y], [100, y]] for y in [10, 30, 50, 70, 90]]
    elif line_shape == 'v_lines':
        lines = [[[x, 0], [x, 100]] for x in [10, 30, 50, 70, 90]]
    elif line_shape == 'wide_lines':
        l1 = [[10, 0], [10, 100]]
        l2 = [[90, 0], [90, 100]]
        lines = [l1, l2]
    elif line_shape == 'high_lines':
        l1 = [[0, 10], [100, 10]]
        l2 = [[0, 90], [100, 90]]
        lines = [l1, l2]
    elif line_shape == 'slant_up':
        l1 = [[0, 0], [100, 100]]
        l2 = [[0, 30], [70, 100]]
        l3 = [[30, 0], [100, 70]]
        l4 = [[50, 0], [100, 50]]
        l5 = [[0, 50], [50, 100]]
        lines = [l1, l2, l3, l4, l5]
    elif line_shape == 'slant_down':
        l1 = [[0, 100], [100, 0]]
        l2 = [[0, 70], [70, 0]]
        l3 = [[30, 100], [100, 30]]
        l4 = [[0, 50], [50, 0]]
        l5 = [[50, 100], [100, 50]]
        lines = [l1, l2, l3, l4, l5]
    elif line_shape == 'center':
        cx = 54.26
        cy = 47.83
        l1 = [[cx, cy], [cx, cy]]
        lines = [l1]
    elif line_shape == 'star':
        star_pts = [10, 40, 40, 40, 50, 10, 60, 40, 90, 40, 65, 60, 75, 90, 50, 70, 25, 90, 35, 60]
        pts = [star_pts[i:i + 2] for i in range(0, len(star_pts), 2)]
        pts = [[p[0] * 0.8 + 20, 100 - p[1]] for p in pts]
        pts.append(pts[0])
        lines = [pts[i:i + 2] for i in range(0, len(pts) - 1, 1)]
    elif line_shape == 'down_parab':
        curve = [[x, -((x - 50) / 4)**2 + 90] for x in np.arange(0, 100, 3)]
        lines = [curve[i:i + 2] for i in range(0, len(curve) - 1, 1)]
    else:
        raise ValueError(line_shape)

    return lines


def perturb(
        df,
        initial,
        target='circle',
        line_error=1.5,
        shake=0.1,
        allowed_dist=3,  # should be 2, just making it bigger for the sp example
        temp=0,
        x_bounds=[0, 100],
        y_bounds=[0, 100]):
    """This is the function which does one round of perturbation

    Args:
        df: is the current dataset
        initial: is the original dataset
        target: is the name of the target shape
        shake: the maximum amount of movement in each iteration
    """
    # take one row at random, and move one of the points a bit
    row = np.random.randint(0, len(df))
    i_xm = df.at[row, 'x']
    i_ym = df.at[row, 'y']

    # this is the simulated annealing step, if "do_bad", then we are willing to
    # accept a new state which is worse than the current one
    do_bad = np.random.random_sample() < temp

    while True:
        xm = i_xm + np.random.randn() * shake
        ym = i_ym + np.random.randn() * shake

        if target == 'circle':
            # info for the circle
            cx = 54.26
            cy = 47.83
            r = 30

            dc1 = dist([df['x'][row], df['y'][row]], [cx, cy])
            dc2 = dist([xm, ym], [cx, cy])

            old_dist = abs(dc1 - r)
            new_dist = abs(dc2 - r)

        elif target == 'bullseye':
            # info for the bullseye
            cx = 54.26
            cy = 47.83
            rs = [18, 37]

            dc1 = dist([df['x'][row], df['y'][row]], [cx, cy])
            dc2 = dist([xm, ym], [cx, cy])

            old_dist = np.min([abs(dc1 - r) for r in rs])
            new_dist = np.min([abs(dc2 - r) for r in rs])

        elif target == 'dots':
            # create a grid of "cluster points" and move if you are getting closer
            # (or are already close enough)
            xs = [25, 50, 75]
            ys = [20, 50, 80]

            old_dist = np.min([
                dist([x, y], [df['x'][row], df['y'][row]])
                for x, y in itertools.product(xs, ys)
            ])
            new_dist = np.min([
                dist([x, y], [xm, ym])
                for x, y in itertools.product(xs, ys)
            ])

        elif target in LINE_SHAPES:
            lines = get_points_for_shape(target)

            # calculate how far the point is from the closest one of these
            old_dist = np.min([
                distance_point_line(i_xm, i_ym, l[0][0], l[0][1], l[1][0], l[1][1])
                for l in lines
            ])
            new_dist = np.min([
                distance_point_line(xm, ym, l[0][0], l[0][1], l[1][0], l[1][1])
                for l in lines
            ])
        else:
            raise ValueError(target)

        # check if the new distance is closer than the old distance
        # or, if it is less than our allowed distance
        # or, if we are do_bad, that means we are accepting it no matter what
        # if one of these conditions are met, jump out of the loop
        close_enough = (new_dist < old_dist or new_dist < allowed_dist or do_bad)
        within_bounds = ym > y_bounds[0] and ym < y_bounds[1] and xm > x_bounds[0] and xm < x_bounds[1]
        if close_enough and within_bounds:
            break

    # set the new data point, and return the set
    df.loc[row, 'x'] = xm
    df.loc[row, 'y'] = ym
    return df


def s_curve(v):
    return pytweening.easeInOutQuad(v)


def is_kernel():
    """Detects if running in an IPython session
    """
    if 'IPython' not in sys.modules:
        # IPython hasn't been imported, definitely not
        return False
    from IPython import get_ipython
    # check for `kernel` attribute on the IPython instance
    return getattr(get_ipython(), 'kernel', None) is not None


def run_pattern(df,
                target,
                iters=100000,
                num_frames=100,
                decimals=2,
                max_temp=0.4,
                min_temp=0,
                ramp_in=False,
                ramp_out=False,
                freeze_for=0,
                output_dir='.',
                write_data=False,
                keep_frames=False):
    """The main function, transforms one dataset into a target shape by
    perturbing it.

    Args:
        df: the initial dataset
        target: the shape we are aiming for
        iters: how many iterations to run the algorithm for
        num_frames: how many frames to save to disk (for animations)
        decimals: how many decimal points to keep fixed
    """
    if target not in ALL_TARGETS:
        raise ValueError(f'"{target}" is not a valid target shape.')

    r_good = df.copy()

    # this is a list of frames that we will end up writing to file
    write_frames = [
        int(round(pytweening.linear(x) * iters))
        for x in np.arange(0, 1, 1 / (num_frames - freeze_for))
    ]

    if ramp_in and not ramp_out:
        write_frames = [
            int(round(pytweening.easeInSine(x) * iters))
            for x in np.arange(0, 1, 1 / (num_frames - freeze_for))
        ]
    elif ramp_out and not ramp_in:
        write_frames = [
            int(round(pytweening.easeOutSine(x) * iters))
            for x in np.arange(0, 1, 1 / (num_frames - freeze_for))
        ]
    elif ramp_out and ramp_in:
        write_frames = [
            int(round(pytweening.easeInOutSine(x) * iters))
            for x in np.arange(0, 1, 1 / (num_frames - freeze_for))
        ]

    extras = [iters] * freeze_for
    write_frames.extend(extras)

    # this gets us the nice progress bars in the notebook, but keeps it from crashing
    looper = tqdm.tnrange if is_kernel() else tqdm.trange

    frame_count = 0
    # this is the main loop, were we run for many iterations to come up with the pattern
    for i in looper(iters, leave=True, ascii=True, desc=target + " pattern"):
        t = (max_temp - min_temp) * s_curve(((iters - i) / iters)) + min_temp

        test_good = perturb(r_good.copy(), initial=df, target=target, temp=t)

        # here we are checking that after the perturbation, that the statistics are still within the allowable bounds
        if is_error_still_ok(df, test_good, decimals):
            r_good = test_good

        # save this chart to the file
        for _ in range(write_frames.count(i)):
            plot(
                r_good,
                save_to=os.path.join(output_dir, f'{target}-image-{frame_count:05d}.png'),
                dpi=150
            )
            if write_data:
                r_good.to_csv(os.path.join(output_dir, f'{target}-data-{frame_count:05d}.csv'))

            frame_count += 1

    # TODO stitch together the animation and pass in keep_frames to determine whether frames should be deleted
    return r_good

def main():
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
        'target_shape', nargs='+',
        help=(
            'The shape(s) to convert to. If multiple shapes are provided, the starting shape '
            'will be converted to each target shape separately. TODO: pass all option'
        )
    )
    parser.add_argument('--iterations', default=100000, type=int, help='The number of iterations to run.')
    parser.add_argument('--decimals', default=2, type=int, help='The number of decimal places to preserve equality.')
    parser.add_argument(
        '--output-dir', default=os.path.join(os.getcwd(), 'morphed_data'), help='Path to a directory for writing output files.'
    )
    parser.add_argument(
        '--keep-frames', default=False, action='store_true',
        help='Whether to keep individual frame images in the output directory.'
    )
    parser.add_argument(
        '--write-data', default=False, action='store_true',
        help='Whether to write CSV files to the output directory with the data for each frame.'
    )

    args = parser.parse_args()

    target_shapes = ALL_TARGETS if args.target_shape == ['all'] else set(args.target_shape).intersection(ALL_TARGETS)
    if not target_shapes:
        raise ValueError('No valid target shapes were provided.') # TODO print options here too

    start_shape = load_dataset(args.start_shape)

    for target_shape in target_shapes:
        run_pattern(
            start_shape, target_shape,
            iters=args.iterations, decimals=args.decimals,
            output_dir=args.output_dir, keep_frames=args.keep_frames, 
            write_data=args.write_data, num_frames=100,
        )


if __name__ == '__main__':
    main()
