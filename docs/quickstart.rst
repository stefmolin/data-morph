Quick Start Guide
=================

Installation
------------
The ``data_morph`` package can be installed with ``pip``:

.. code:: console

   $ pip install data_morph

..
   You can also install with ``conda`` (coming soon):

   .. code:: console

      $ conda install data_morph -c conda-forge

Command Line Usage
------------------

Run ``data-morph`` on the command line:

.. code:: console

   $ data-morph --target-shape star -- panda

This produces the following animation in a the newly-created ``morphed_data`` directory
within your current working directory:

.. image:: _static/panda_to_star.gif
   :alt: Morphing the panda :class:`.Dataset` into the star :class:`.Shape`.
   :align: center

----

See all available CLI options by passing in ``--help``:

.. code:: console

   $ data-morph --help

Python Usage
------------

The :class:`.DataMorpher` class performs the morphing from a :class:`.Dataset` to a :class:`.Shape`.
Any :class:`~pandas.DataFrame` with numeric columns ``x`` and ``y`` can be a :class:`.Dataset`.
Use the :class:`.DataLoader` to create the :class:`.Dataset` from a file or use a built-in dataset:

.. code:: python

   from data_morph.data.loader import DataLoader

   dataset = DataLoader.load_dataset('panda')

For morphing purposes, all target shapes are placed/sized based on aspects of the :class:`.Dataset`.
All shapes are accessible via the :class:`.ShapeFactory`:

.. code:: python

   from data_morph.shapes.factory import ShapeFactory

   shape_factory = ShapeFactory(dataset)
   target_shape = shape_factory.generate_shape('star')

With the :class:`.Dataset` and :class:`.Shape` created, here is a minimal example of morphing:

.. code:: python

   from data_morph.morpher import DataMorpher

   morpher = DataMorpher(
       decimals=2,
       in_notebook=False,  # indicate whether you are running this in a Jupyter Notebook
       output_dir='data_morph/output',
   )

   result = morpher.morph(start_shape=dataset, target_shape=target_shape)

.. note::

   The ``result`` variable in the above code block is a :class:`~pandas.DataFrame` of the data
   after completing the specified iterations of the simulated annealing process. The :meth:`.DataMorpher.morph`
   method is also saving plots to visualize the output periodically and make an animation; these end up in
   ``data_morph/output``, which we set as :attr:`.DataMorpher.output_dir`.

----

In this example, we morphed the built-in panda :class:`.Dataset` into the star :class:`.Shape`. Be sure to try
out the other options:

* The :attr:`.DataLoader.AVAILABLE_DATASETS` attribute contains a list of available datasets, which
  are also visualized in the :class:`.DataLoader` documentation.

* The :attr:`.ShapeFactory.AVAILABLE_SHAPES` attribute contains a list of available shapes, which
  are also visualized in the :class:`.ShapeFactory` documentation.
