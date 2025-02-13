Shape Creation
==============

This tutorial walks you through the process of creating a new shape
for use as a target in the morphing process.

.. contents:: Steps
    :depth: 2
    :local:
    :backlinks: none

----

Create a class for the shape
----------------------------

All Data Morph shapes are defined as classes inside the :mod:`.shapes` subpackage.
In order to register a new target shape for the CLI, you will need to fork and clone
`the Data Morph repository <https://github.com/stefmolin/data-morph>`_, and then add
a class defining your shape.

Select the appropriate base class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Data Morph uses a hierarchy of shapes that all descend from an abstract
base class (:class:`.Shape`), which defines the basics of how a shape
needs to behave (*i.e.*, it must have a ``distance()`` method and a
``plot()`` method).

.. figure:: ../_static/tutorials/shapes_uml.svg
   :alt: UML diagram showing the hierarchy of the shape classes.
   :align: center

Any new shape must inherit from :class:`.Shape` or one of its
child classes:

* If your shape is composed of lines, inherit from :class:`.LineCollection`
  (*e.g.*, :class:`.Star`).
* If your shape is composed of points, inherit from :class:`.PointCollection`
  (*e.g.*, :class:`.Heart`).
* If your shape isn't composed of lines or points you can inherit directly from
  :class:`.Shape` (*e.g.*, :class:`.Circle`). Note that in this case you must
  define both the ``distance()`` and ``plot()`` methods (this is done for your
  if you inherit from :class:`.LineCollection` or :class:`.PointCollection`).

Define the scale and placement of the shape based on the dataset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each shape will be initialized with a :class:`.Dataset` instance. Use the dataset
to determine where in the *xy*-plane the shape should be placed and also to scale it
to the data. If you take a look at the existing shapes, you will see that they use
various bits of information from the dataset, such as the automatically-calculated
bounds (*e.g.*, :attr:`.Dataset.data_bounds`, which form the bounding box of the
starting data, and :attr:`.Dataset.morph_bounds`, which define the limits of where
the algorithm can move the points) or percentiles using the data itself (see
:attr:`.Dataset.data`). For example, the :class:`.XLines` shape inherits from
:class:`.LineCollection` and uses the morph bounds (:attr:`.Dataset.morph_bounds`)
to calculate its position and scale:

.. code:: python

    class XLines(LineCollection):

        name = 'x'

        def __init__(self, dataset: Dataset) -> None:
            (xmin, xmax), (ymin, ymax) = dataset.morph_bounds

            super().__init__([[xmin, ymin], [xmax, ymax]], [[xmin, ymax], [xmax, ymin]])


Since we inherit from :class:`.LineCollection` here, we don't need to define
the ``distance()`` and ``plot()`` methods (unless we want to override them).
We do set the ``name`` attribute here since the default will result in
a value of ``xlines`` and ``x`` makes more sense for use in the documentation
(see :class:`.ShapeFactory`).

Register the shape
------------------

For the ``data-morph`` CLI to find your shape, you need to register it with the
:class:`.ShapeFactory`:

1. Add your shape class to the appropriate module inside the ``src/data_morph/shapes/``
   directory. Note that these correspond to the type of shape (*e.g.*, use
   ``src/data_morph/shapes/points/<your_shape>.py`` for a new shape inheriting from
   :class:`.PointCollection`).
2. Add your shape to ``__all__`` in that module's ``__init__.py`` (*e.g.*, use
   ``src/data_morph/shapes/points/__init__.py`` for a new shape inheriting from
   :class:`.PointCollection`).
3. Add an entry to the ``ShapeFactory._SHAPE_CLASSES`` tuple in
   ``src/data_morph/shapes/factory.py``, preserving alphabetical order.

Test out the shape
------------------

Defining how your shape should be generated from the input dataset will require
a few iterations. Be sure to test out your shape on different datasets:

.. code:: console

   $ data-morph --start-shape panda music soccer --target-shape <your shape>

Some shapes will work better on certain datasets, and that's fine. However,
if your shape only works well on one of the built-in datasets (see the
:class:`.DataLoader`), then you need to keep tweaking your implementation.

(Optional) Contribute the shape
-------------------------------

If you think that your shape would be a good addition to Data Morph, `create an issue
<https://github.com/stefmolin/data-morph/issues>`_ in the Data Morph repository proposing
its inclusion. Be sure to consult the `contributing guidelines
<https://github.com/stefmolin/data-morph/blob/main/CONTRIBUTING.md>`_ before doing so.

If and only if you are given the go ahead:

1. Prepare a docstring for your shape following what the other shapes have.
   Be sure to change the plotting code in the docstring to use your shape.
2. Add test cases for your shape to the ``tests/shapes/`` directory.
3. Submit your pull request.
