#!/usr/bin/env python
"""
Call this script with the names of files that have changed to get the
datasets and shapes to test with the CLI.

Examples
--------

$ python bin/ci.py src/data_morph/shapes/circles.py
bullseye circle rings

$ python bin/ci.py src/data_morph/shapes/bases/line_collection.py
high_lines h_lines slant_down slant_up v_lines wide_lines x diamond rectangle star

$ python bin/ci.py src/data_morph/shapes/points/heart.py
heart spade

$ python bin/ci.py src/data_morph/data/starter_shapes/superdatascience.csv
SDS
"""

import sys
from pathlib import Path

from data_morph.data.loader import DataLoader
from data_morph.shapes.factory import ShapeFactory

new_paths = sys.argv[1:]

args = set()

# Figure out argument of datasets based on .csv filename
for dataset, filename in DataLoader._DATASETS.items():
    for new_file in new_paths:
        if filename in new_file:
            args.add(dataset)

# Figure out argument of shapes based on .py filename
new_files = [Path(x).name for x in new_paths]
for shape, shape_cls in ShapeFactory._SHAPE_MAPPING.items():
    # Find the class and all parent classes and get their module name
    # We get the module name because it ends in the Python file without .py extension
    mro = [
        x.__module__ for x in shape_cls.__mro__ if x.__module__.startswith('data_morph')
    ]

    if shape == 'spade':
        mro.append('heart')

    all_modules = [f'{x}.py' for x in mro]

    for new_file in new_files:
        for module in all_modules:
            if module.endswith(new_file):
                args.add(shape)
                break

print(' '.join(args))
