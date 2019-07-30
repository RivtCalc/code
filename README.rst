**rivet package**
==================

The *rivet* package implements the **r-i-v-e-t** calculation language as a
component for **on-c-e** (**O**\pe\**N** **C**\alculation **E**\nvironment),
which produces engineering calculation documents. It is written in Python and
designed to improve document reuse and review.  The program and documentation
are here: https://github.com/r-i-v-e-t .  For an overview of **on-c-e** see
https://github.com/on-c-e .

A **r-i-v-e-t** calculation is an ASCII text file containing engineering design
calculations in the **r-i-v-e-t** and Python language format. Design files have
names of the form *ddcc_design_filename.py* where dd and cc are two digit
numbers identifying the division and calculation number respectively. Division
numbers apply to **r-i-v-e-t**  reports which are organized compilations of
calculations.

Design input files and their required supporting files must be stored in the
proper subfolders of the *designs* folder. Output files are written to the
*calcs* directory in html, pdf and text (utf) format. To protect against data
loss the user must create the project folder structure and use the following
naming conventions.  The program will display an error and stop if it does not
find the correct folder structure and naming. ::

  Project_Name (chosen by user)
      |- calcs
          |- pdf
          |- temp
          |- txt
      |- designs
          |- figures
          |- scripts
          |- tables
      |- reports
          |- attachments
          |- html
          |- temp

The *rivet* package processes and outputs formatted calculations and reports.
In the common case where designs are written and edited in interactive mode,
calculations are produced by importing the *rivet_lib* library into the design
file. Calculations can also be produced by processing an entire design file from
the command line by invoking the rivet package as follows:

.. code:: python

    python rivet ddcc_ design_filename.py
