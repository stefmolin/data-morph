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

import math
import os
import sys

import numpy as np
import pytweening
import tqdm

from .data.stats import get_values
from .plotting import plot, stitch_gif_animation

# TODO: class that does the morphing


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


def average_location(
    pairs,
):  # TODO: is this used anywhere? maybe to morph arbitrary shapes? will need a shape class for this
    """Calculates the average of all the x-coordinates and y-coordinates of the
    pairs given. In other words, if ``pairs`` is a list of ``[(x_i, y_i)]``
    points, then this calculates ``[(mean(x_i), mean(y_i))]``.
    """
    return np.mean(pairs, axis=1)


def perturb(
    df,
    target,
    shake=0.3,
    allowed_dist=2,
    temp=0,
    x_bounds=[
        0,
        100,
    ],  # TODO: derive these bounds based on the data? or just normalize the data to be within these to start?
    y_bounds=[0, 100],
):
    """This is the function which does one round of perturbation

    Args:
        df: is the current dataset
        initial: is the original dataset
        target: is the target shape
        shake: the maximum amount of movement in each iteration
    """
    # TODO: better variable names
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

        old_dist = target.distance(i_xm, i_ym)
        new_dist = target.distance(xm, ym)

        # check if the new distance is closer than the old distance
        # or, if it is less than our allowed distance
        # or, if we are do_bad, that means we are accepting it no matter what
        # if one of these conditions are met, jump out of the loop
        close_enough = new_dist < old_dist or new_dist < allowed_dist or do_bad
        within_bounds = (
            ym > y_bounds[0]
            and ym < y_bounds[1]
            and xm > x_bounds[0]
            and xm < x_bounds[1]
        )
        if close_enough and within_bounds:
            break

    # set the new data point, and return the set
    df.loc[row, 'x'] = xm
    df.loc[row, 'y'] = ym
    return df


def is_kernel():  # TODO: is this necessary?
    """Detects if running in an IPython session"""
    if 'IPython' not in sys.modules:
        # IPython hasn't been imported, definitely not
        return False
    from IPython import get_ipython

    # check for `kernel` attribute on the IPython instance
    return getattr(get_ipython(), 'kernel', None) is not None


def run_pattern(
    start_shape_name,
    start_shape_data,
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
    keep_frames=False,
    seed=None,
    forward_only_animation=False,
):
    """The main function, transforms one dataset into a target shape by
    perturbing it.

    Args:
        df: the initial dataset
        target: the shape we are aiming for
        iters: how many iterations to run the algorithm for
        num_frames: how many frames to save to disk (for animations)
        decimals: how many decimal points to keep fixed
    """
    # TODO: be more consistent about passing around target_shape and target as string or object
    df = start_shape_data  # TODO: rename this everywhere
    r_good = df.copy()

    if seed is not None:
        np.random.seed(seed)

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
    for i in looper(iters, leave=True, ascii=True, desc=f'{target} pattern'):
        t = (max_temp - min_temp) * pytweening.easeInOutQuad(
            ((iters - i) / iters)
        ) + min_temp

        test_good = perturb(r_good.copy(), target=target, temp=t)

        # here we are checking that after the perturbation, that the statistics are still within the allowable bounds
        if is_error_still_ok(df, test_good, decimals):
            r_good = test_good

        # save this chart to the file
        for _ in range(write_frames.count(i)):
            plot(
                r_good,
                save_to=os.path.join(
                    output_dir,
                    f'{start_shape_name}-to-{target}-image-{frame_count:05d}.png',
                ),
                dpi=150,
            )
            if write_data:
                r_good.to_csv(
                    os.path.join(
                        output_dir,
                        f'{start_shape_name}-to-{target}-data-{frame_count:05d}.csv',
                    )
                )

            frame_count += 1

    stitch_gif_animation(
        output_dir,
        start_shape_name,
        target_shape=target,
        keep_frames=keep_frames,
        forward_only_animation=forward_only_animation,
    )
    return r_good
