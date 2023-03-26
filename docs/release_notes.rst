Release Notes
=============

0.1.0 (March 26, 2023)
----------------------

This is the first release of Data Morph, which is a spinoff of
`jmatejka/same-stats-different-graphs <https://github.com/jmatejka/same-stats-different-graphs>`_.
Data Morph extends the original premise from
`the Autodesk Research paper <https://www.autodeskresearch.com/publications/samestats>`_ to be more general.
The core improvements include:

* Created a modular package, moving away from functional programming to object-oriented programming.
* Introduction of :class:`.Shape` classes both for resuability of the code and to decouple the shapes from
  the original "dinosaurus" dataset and its hardcoded values. Morphing is now possible from any input dataset
  to the target shapes. See the :class:`.ShapeFactory` documentation for visuals.
* Creation of :class:`.Dataset` to hold the data along with bounds needed for morphing and plotting and the name.
* Morph and plot bounding logic for automatic calculation of values needed for simulated annealing and plot limits.
* Fun new starter datasets: cat, dog, music, panda, and sheep. See the :class:`.DataLoader` documentation for visuals.
* Easier application of plotting theme.
* Documentation with Sphinx.
* Testing suite with pytest.
* Replaced center shape with scatter and included a new rectangle shape.
