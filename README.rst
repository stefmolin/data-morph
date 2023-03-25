Data Morph
==========

Morph an input dataset of 2D points into select shapes, while preserving the summary
statistics to a given number of decimal points through simulated annealing.

.. include:: docs/quickstart.rst
   :start-after: .. INSTALLATION

Notes
-----
This code has been altered by Stefanie Molin to work for other input datasets
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
