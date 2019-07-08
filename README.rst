**rivet**
===========

This package provides a language for **on-c-e** (OpeN Calculation Environment -
see http://on-c-e.github.io.), an open source, cross platform framework
intended to improve construction productivity by establishing a few standard
engineering design document formats that are easy to read, reuse and extend.

A calculation file in **r-i-v-e-t** is a Python file or files containing design
calculations that use the *rivet* package. Design file names have the form
*ddcc_designfilename.py*, where dd and cc are two digit numbers identifying the
division and calculation number respectively.

Calcs and supporting files for a project are contained in a project folder
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

Design input files and their required supporting files are stored in the
design folder and it's respective subfolders. 

The *rivet* package processes and outputs formatted calculations in UTF-8 text,
HTML, and PDF when specified (and LaTeX is installed). Output is saved in the
respective calcs folder. Output is also sent to the terminal (std out) for
interactive calculation development. Interactive output depends on the editor
or IDE used (e.g. VS Code, Pyzo, Komodo etc.). VS Code or Pyzo are recommended.
The design file can be processed from command line (in the design folder) as
follows.

.. code:: python

            python ddcc_designfilename.py


Program and documentation are here: http://r-i-v-e-t.github.io and here
http://on-c-e.github.io.