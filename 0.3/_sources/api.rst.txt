API
===

.. automodule:: data_morph

.. rubric:: Modules

.. autosummary::
   :toctree: api
   :recursive:

   data_morph.bounds
   data_morph.data
   data_morph.morpher
   data_morph.plotting
   data_morph.progress
   data_morph.shapes

----

.. rubric:: Examples

.. include:: quickstart.rst
   :start-after: .. PYTHON USAGE START
   :end-before: .. PYTHON USAGE END

This produces the following animation in the directory specified as ``output_dir`` above:

.. figure:: _static/panda_to_star.gif
   :alt: Morphing the panda dataset into the star shape.
   :align: center

   Morphing the panda :class:`.Dataset` into the star :class:`.Shape`.

----

.. include:: quickstart.rst
   :start-after: .. VIZ LISTINGS

.. note::
   There is also a :ref:`CLI option <quickstart:command line usage>` for morphing.

.. rubric:: Citations

.. include:: citation.rst
