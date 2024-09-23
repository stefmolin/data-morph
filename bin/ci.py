#!/usr/bin/env python
from data_morph.shapes.factory import ShapeFactory
from data_morph.data.loader import DataLoader
import sys
from inspect import getmro
from os.path import basename

new_paths = sys.argv[1:]

args = []

# Figure out argument of datasets based on .csv filename
for dataset, filename in DataLoader._DATASETS.items():
    for new_file in new_paths:
        if filename in new_file:
            args.append(dataset)

# Figure out argument of shapes based on .py filename
new_files = [basename(x).split('/')[-1] for x in new_paths]
for shape, c in ShapeFactory._SHAPE_MAPPING.items():
    for new_file in new_files:
        # Find the class and all parent classes and get their module name
        # We get the module name because it ends in the python file without .py extension
        # To make it easy to compare, we just add the extension onto the end
        parents = [x.__module__ for x in getmro(c)]
        all_modules = parents + [c.__module__]
        all_modules = [f"{x}.py" for x in all_modules]

        for module in all_modules:
            if module.endswith(new_file):
                args.append(shape)
                break

print(" ".join(args))
