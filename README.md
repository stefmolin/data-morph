# same-stats-different-graphs

The code used for generating the animations and data sets in
[the paper](https://www.autodeskresearch.com/publications/samestats).  The main
purpose of this code is to provide a reference for performing these simulations,
and ultimately has the goal of being a usable Python package for generating test
data sets.

## Installation

Currently this project is not available in any package repository like PyPI or
Anaconda, so you will have to install from source:

    $ git clone https://github.com/jmatejka/same-stats-different-graphs
    $ cd same-stats-different-graphs
    $ python setup.py install

This should download all dependencies, but just in case it's difficult to get
the dependencies installed from PyPI, the packages needed for installation are:

* `setuptools`
* `pandas`
* `seaborn`
* `matplotlib`
* `numpy`
* `scipy`
* `pytweening`
* `tqdm`
* `docopt`

No specific tests have been performed yet, but this code should work fine with
both Python 2 and Python 3.

## Usage

Currently the easiest way to use this package is from the command line tool set
up by running `python setup.py install`, or by running the module directly with
`python -m samestats`:

    $ python -m samestats run -h
    Usage:
        samestats run <shape_start> <shape_end> [<iters>][<decimals>][<frames>]

## Future plans

Right now we are working on getting the code cleaned up, documented, some
features added, and tests written.  Just the basics for getting a package ready
for prime time. Once the code is in a pretty good state, we want to get it
uploaded to PyPI and Anaconda, if possible, and the documentation uploaded to
[readthedocs.io](https://readthedocs.io).

We may also look into providing an easy-to-use API for generating these types of
data sets from your own data, with the goal of making it easy to generate good
test data for use in unit tests.

Another goal is to provide an API for "anonymizing" data sets. If the desired
statistical properties can be preserved while adding noise to the underlying
values, this could be a useful technique for protecting the privacy of study
participants or users when publishing a dataset online.
