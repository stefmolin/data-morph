Release Notes
=============

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
