Data Morph
==========

Morph an input dataset of 2D points into select shapes, while preserving the summary
statistics to a given number of decimal points through simulated annealing.

.. image:: docs/_static/panda_to_star.gif
   :alt: Morphing the panda dataset into the star shape.
   :align: center

Installation
------------
The ``data_morph`` package can be installed with ``pip``:

.. code:: console

   $ pip install data_morph

Usage
-----

Once installed, Data Morph can be used on the command line or as an importable Python package.
Below are some examples; be sure to check out the documentation for more information.


Command Line Usage
~~~~~~~~~~~~~~~~~~

Run ``data-morph`` on the command line:

.. code:: console

   $ data-morph --target-shape star -- panda

This produces the animation in the newly-created ``morphed_data`` directory
within your current working directory (shown above).

----

See all available CLI options by passing in ``--help``:

.. code:: console

   $ data-morph --help

Python Usage
~~~~~~~~~~~~

The ``DataMorpher`` class performs the morphing from a ``Dataset`` to a ``Shape``.
Any ``pandas.DataFrame`` with numeric columns ``x`` and ``y`` can be a ``Dataset``.
Use the ``DataLoader`` to create the ``Dataset`` from a file or use a built-in dataset:

.. code:: python

   from data_morph.data.loader import DataLoader

   dataset = DataLoader.load_dataset('panda')

For morphing purposes, all target shapes are placed/sized based on aspects of the ``Dataset`` class.
All shapes are accessible via the ``ShapeFactory`` class:

.. code:: python

   from data_morph.shapes.factory import ShapeFactory

   shape_factory = ShapeFactory(dataset)
   target_shape = shape_factory.generate_shape('star')

With the ``Dataset`` and ``Shape`` created, here is a minimal example of morphing:

.. code:: python

   from data_morph.morpher import DataMorpher

   morpher = DataMorpher(
       decimals=2,
       in_notebook=False,  # whether you are running in a Jupyter Notebook
       output_dir='data_morph/output',
   )

   result = morpher.morph(start_shape=dataset, target_shape=target_shape)

Note that the ``result`` variable in the above code block is a ``pandas.DataFrame`` of the data
after completing the specified iterations of the simulated annealing process. The ``DataMorpher.morph()``
method is also saving plots to visualize the output periodically and make an animation; these end up in
``data_morph/output``, which we set as ``DataMorpher.output_dir``.


----

In this example, we morphed the built-in panda ``Dataset`` into the star ``Shape``. Be sure to try
out the other built-in options:

* The ``DataLoader.AVAILABLE_DATASETS`` attribute contains a list of available datasets, which
  are also visualized in the ``DataLoader`` documentation.

* The ``ShapeFactory.AVAILABLE_SHAPES`` attribute contains a list of available shapes, which
  are also visualized in the ``ShapeFactory`` documentation.

Acknowledgements
----------------
This code has been altered by Stefanie Molin ([@stefmolin](https://github.com/stefmolin/data-morph/edit/main/README.rst)) to work for other input datasets
by parameterizing the target shapes with information from the input shape.
The original code works for a specific dataset called the "dinosaurus" and was created
for the paper *Same Stats, Different Graphs: Generating Datasets with Varied Appearance and
Identical Statistics through Simulated Annealing* by Justin Matejka and George Fitzmaurice
(ACM CHI 2017).

The paper, video, and associated code and datasets can be found on the
Autodesk Research website `here <https://www.autodeskresearch.com/publications/samestats>`_.
The version of this code placed on GitHub at
`jmatejka/same-stats-different-graphs <https://github.com/jmatejka/same-stats-different-graphs>`_,
served as the starting point for the ``data_morph`` code base, which is on GitHub at
`stefmolin/data-morph <https://github.com/stefmolin/data-morph>`_.
