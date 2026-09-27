"""
Data Morph.

Morph an input dataset of 2D points into select shapes, while preserving the summary
statistics to a given number of decimal points through simulated annealing. It is intended
to be used as a teaching tool to illustrate the importance of data visualization (see
`Data Morph in the classroom <https://stefaniemolin.com/data-morph/stable/index.html#classroom-ideas>`_
for ideas).

.. figure:: _static/panda-to-star-median.gif
   :alt: Morphing the panda dataset into the star shape with marginal plots.
   :align: center

   Morphing the panda :class:`.Dataset` into the star :class:`.Shape` with marginal
   plots, preserving the median in addition to the mean and standard deviation.

Notes
-----
This code has been altered by Stefanie Molin to work for other input datasets
by parameterizing the target shapes with information from the input shape.
The original code works for a specific dataset called the "Datasaurus" and was created
for the paper *Same Stats, Different Graphs: Generating Datasets with Varied Appearance and
Identical Statistics through Simulated Annealing* by Justin Matejka and George Fitzmaurice
(ACM CHI 2017).

The paper and video can be found on the `Autodesk Research website
<https://www.research.autodesk.com/publications/same-stats-different-graphs-generating-datasets-with-varied-appearance-and-identical-statistics-through-simulated-annealing/>`_.
The version of the code placed on GitHub at
`jmatejka/same-stats-different-graphs <https://github.com/jmatejka/same-stats-different-graphs>`_,
served as the starting point for the Data Morph codebase, which is on GitHub at
`stefmolin/data-morph <https://github.com/stefmolin/data-morph>`_.

Read more about the creation of Data Morph in `this article
<https://stefaniemolin.com/articles/data-science/introducing-data-morph/>`_
and `this slide deck <https://stefaniemolin.com/data-morph-talk/#/>`_.
"""

from importlib.metadata import version

__version__ = version('data-morph-ai')
MAIN_DIR = __name__

__all__ = ['MAIN_DIR', '__version__']
