CLI Reference
=============

.. argparse::
    :ref: data_morph.cli._generate_parser_for_docs
    :prog: Data Morph
    :noepilog:

----

Examples
--------

1. morph the panda shape into a star::

    $ data-morph --start-shape panda --target-shape star

2. morph the panda shape into all available target shapes::

    $ data-morph --start-shape panda --target-shape all

3. morph the cat, dog, and panda shapes into the circle and slant_down shapes::

    $ data-morph --start-shape cat dog panda --target-shape circle slant_down

4. morph the dog shape into upward-slanting lines over 50,000 iterations with seed 1::

    $ data-morph --start-shape dog --target-shape slant_up --iterations 50000 --seed 1

5. morph the cat shape into a circle, preserving summary statistics to 3 decimal places::

    $ data-morph --start-shape cat --target-shape circle --decimals 3

6. morph the music shape into a bullseye, specifying the output directory::

    $ data-morph --start-shape music --target-shape bullseye --output-dir path/to/dir

7. morph the sheep shape into vertical lines, slowly ramping in and out for the animation::

    $ data-morph --start-shape sheep --target-shape v_lines --ramp-in --ramp-out
