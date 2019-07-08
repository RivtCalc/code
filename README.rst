**rivet**
===========

**r-i-v-e-t** is the language component of **on-c-e** (OpenN Calculation
Environment - see see http://on-c-e.github.io), a framework for producing
engineering calculation documents. The motivation for writing **r-i-v-e-t** is
to improve construction productivity by developing better methods for producing
design documents that are easy to read and resuse.

A **r-i-v-e-t** file is a Python file or files containing design calculations
that use the *rivet* package. Design files have names of the form
*ddcc_designfilename.py* where *dd* and *cc* are two digit numbers identifying
the division and calculation number respectively.

Design calculations and supporting files are contained in a project folder
structure as follows::

    Project Name (chosen by user)
        |- designs
            |- figures
            |- scripts
            |- tables
        |- calcs
            |- txt
            |- html
            |- pdf
            |- temp

Output is saved in the respective calcs folder. The *rivet* package outputs
formatted calculations in utf8 text, html, and PDF if specified (and LaTeX is
installed). Output is also sent to the terminal (standard out) for interactive
development. Options for output in interactive development depend on the editor
or IDE used (e.g. VS Code, Pyzo, Komodo etc.). The design file can also be
processed to calculations from command line, within the design folder, as
follows:

.. code:: python

            python ddcc_designfilename.py


The program and further documentation are here: http://r-i-v-e-t.github.io and
here http://on-c-e.github.i