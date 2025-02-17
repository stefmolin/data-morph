Release Notes
=============

0.3.0 (February 17, 2025)
-------------------------

What's New
^^^^^^^^^^

CLI
~~~
* Added ``--workers`` option to the CLI for running multiple morphs in parallel.
* Renamed ``--ramp-in`` and ``--ramp-out`` as ``--ease-in`` and ``--ease-out``.
* Added ``--ease`` option to the CLI, which is shorthand for ``--ease-in --ease-out``.

Documentation
~~~~~~~~~~~~~
* Added :doc:`tutorials/index` page to the documentation.
* Added :doc:`tutorials/shape-creation` tutorial.
* Added section to the documentation with ideas of how to use :ref:`classroom ideas`.
* Updated contribution instructions in :doc:`tutorials/custom-datasets` tutorial.
* Included reference to `article on the creation of Data Morph
  <https://stefaniemolin.com/articles/data-science/introducing-data-morph/>`_
  in the documentation header.
* Included reference to `Data Morph: A Cautionary Tale of Summary Statistics
  <https://stefaniemolin.com/data-morph-talk/>`_
  (conference talk) in the documentation header.
* Added `contributing guidelines <https://github.com/stefmolin/data-morph/blob/main/CONTRIBUTING.md>`_
  and `code of conduct <https://github.com/stefmolin/data-morph/blob/main/CODE_OF_CONDUCT.md>`_.
* Configured canonical URL.

Morphing
~~~~~~~~
* Reworked GIF creation logic to write only one PNG for distinct frames in the
  animation and use frequency counts to determine frame duration for speed
  improvements and less I/O.
* Added three new datasets: soccer, pi, and gorilla. See the :class:`.DataLoader` for visuals.
* Added four new shapes: :class:`.Club`, :class:`.FigureEight`, :class:`.Spade`,
  and :class:`.Spiral`.
* Refactored some shape logic to use more ``numpy`` for speed improvements.
* Added ``center`` property to :class:`.Interval` and :class:`.BoundingBox` to simplify shape calculations.
* Made it possible to unpack the bounds from the :class:`.BoundingBox`.
* Switched from ``tqdm`` to progress bars powered by ``rich``.
* Renamed the ``ramp_in`` and ``ramp_out`` arguments to :meth:`.DataMorpher.morph`
  as ``ease_in`` and ``ease_out``.
* Added :meth:`.Shape.get_name` method and :attr:`.Shape.name` attribute to replace
  ``__str__()`` shape naming logic, which removed some redundancies in
  :class:`.ShapeFactory`.
* Refactored the shape code into separate modules per shape.
* Renamed ``get_values()`` as :func:`.get_summary_statistics`.
* Improved variable names in several spots for more readable code.

Plotting
~~~~~~~~
* Added ``show_bounds`` parameter to :meth:`.Dataset.plot` to visualize the automatically-calculated bounds.
* Added ``title`` parameter to :meth:`.Dataset.plot` with default showing the name and number of points.
* Switched from using Matplotlib's ``tight_layout()`` to constrained layout.
* Added :func:`.style_context` context manager for plotting in a Data Morph style.
* Added test suite for :mod:`.plotting.style` module.
* Changed plot layouts for :meth:`.DataLoader.plot` and :meth:`.ShapeFactory.plot_available_shapes`.
* Adjusted grid of datasets in the documentation to use tighter plot bounds.

Tooling
~~~~~~~
* Added new GitHub Actions workflow to run Data Morph on new/altered datasets, shapes,
  or core logic.
* Switched to trusted publishing on PyPI via GitHub Actions.
* Added PR and issue templates.
* Added ``pytest-xdist`` to dev dependencies and reworked the test suite to make it faster.
* Switched from ``black`` to ``ruff`` formatting in pre-commit setup and included additional rulesets.
* Added ``pyproject-fmt`` pre-commit hook.
* Refactored shape tests.

Bug Fixes
^^^^^^^^^
* Addressed compatibility issues with ``numpy>=2.0.0``.
* Assorted performance and code quality improvements after running additional
  ``ruff`` rules.
* Fixed some incorrect return types.

Dependency Updates
^^^^^^^^^^^^^^^^^^
* Replaced ``tqdm`` dependency with ``rich``.
* Replaced ``pytweening`` dependency with functions in :mod:`.plotting.animation`.
* Replaced ``sphinxarg.ext`` Sphinx extension with ``sphinx_argparse_cli``.
* Changed the minimum Sphinx version to 7.2.6.
* Changed the minimum ``pydata-sphinx-theme`` version to 0.15.3.
* Updated pre-commit hooks to the latest versions.
* Factored out ``scipy`` dependency.
* Updated GitHub Actions workflows for Node 16 deprecation.
* Enabled Dependabot on GitHub Actions and switched to use commit hashes for versioning.
* Updated Python testing matrix to include Python 3.9 through 3.13.

0.2.0 (September 24, 2023)
--------------------------

What's New
^^^^^^^^^^
* Created 5 new target shapes: :class:`.Diamond`, :class:`.Heart`,
  :class:`.LeftParabola`, :class:`.RightParabola`, :class:`.Rings`.
* Created 3 new datasets: bunny, Python logo (TM), SuperDataScience logo.
  Logos are used with permission.
* Made it possible to install via ``conda``.
* Configured versioned documentation hosted in GitHub Pages.
* Generated a :doc:`CLI reference <cli>` page in the documentation.
* Provided a :doc:`custom dataset creation tutorial <tutorials/custom-datasets>` to the documentation.
* Included logo and badges in README.
* Included an example using easing for the animation to the documentation.
* Included reference to `article on the creation of Data Morph
  <https://stefaniemolin.com/articles/data-science/introducing-data-morph/>`_
  in the documentation.
* Configured codecov reporting on test coverage with actions to validate the
  config both periodically and upon change.
* Incorporated metavar indicators for some CLI options.
* Added a test of the frame freezing functionality in the :class:`.DataMorpher`.
* Added a test for the :meth:`.ShapeFactory.plot_available_shapes` method used in the documentation.
* Added a test for the :meth:`.PointCollection.plot` method used in the documentation.

Bug Fixes
^^^^^^^^^
* Fixed links to Autodesk assets after change to their website.
* Corrected missing type references in the documentation.
* Addressed a bug in the :class:`.DataMorpher` that caused frame recording to miss first frame (initial dataset).
* Fixed a bug in the :class:`.DataMorpher` that wasn't properly decreasing
  the temperature in the simulated annealing process.
* Reduced point size for datasets displayed in the documentation so points
  appear with some separation and stay true to their subjects.
* Fixed bug in logic for padding statistics in plots that would use incorrect spacing in some cases.

Dependency Updates
^^^^^^^^^^^^^^^^^^
* Changed the minimum Sphinx version to 7.2.1.
* Changed the minimum ``pytweening`` version to 1.0.5.
* Switched from ``isort`` and ``flake8`` to ``ruff`` in pre-commit setup.
* Updated pre-commit hooks to the latest versions and to use the new upstream ``numpydoc`` validation hook.


0.1.0 (April 1, 2023)
---------------------

This is the first release of Data Morph, which is a spinoff of
`jmatejka/same-stats-different-graphs <https://github.com/jmatejka/same-stats-different-graphs>`_.
Data Morph extends the original premise from
`the Autodesk Research paper <https://www.autodeskresearch.com/publications/samestats>`_ to be more general.
The core improvements include:

* Created a modular package, moving away from functional programming to object-oriented programming.
* Introduction of :class:`.Shape` classes both for resuability of the code and to decouple the shapes from
  the original "datasaurus" dataset and its hardcoded values. Morphing is now possible from any input dataset
  to the target shapes. See the :class:`.ShapeFactory` documentation for visuals.
* Creation of :class:`.Dataset` to hold the data along with bounds needed for morphing and plotting and the name.
* Morph and plot bounding logic for automatic calculation of values needed for simulated annealing and plot limits.
* Fun new starter datasets: cat, dog, music, panda, and sheep. See the :class:`.DataLoader` documentation for visuals.
* Easier application of plotting theme.
* Documentation with Sphinx.
* Testing suite with pytest.
* Replaced center shape with :class:`.Scatter` and included a new :class:`.Rectangle` shape.
