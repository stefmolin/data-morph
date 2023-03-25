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

   $ data_morph --help
