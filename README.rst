**rivet package**
==================

The *rivet* package implements the **r-i-v-e-t** calculation language as a
component of **on-c-e** (**O**\ pe\ **N** **C**\ alculation **E**\ nvironment),
which produces formatted engineering calculation documents. It is written in
Python and designed to improve document reuse and review.  The program and
documentation are here: https://github.com/r-i-v-e-t .  For an overview of
**on-c-e** see https://github.com/on-c-e .

A **r-i-v-e-t** design is an ASCII text file containing engineering calculations
in the **r-i-v-e-t** and Python language format. Design files have names of the
form *ddcc_design_filename.py* where dd and cc are two digit numbers identifying
the division and calculation number respectively. Division numbers apply to
**r-i-v-e-t**  reports which are organized compilations of calculations.

Designs and their required supporting files must be stored in their respective
*designs* subfolder. Output calc files are written to the *calcs* directory in
html and text (utf) format. PDF calcs, if specified, are written to the report
folder and may be assembled into collated reports. To protect against data loss
the user must initially set up a project by creating the project folder
structure using the following naming conventions::

  Project_Name (chosen by user)
      |- calcs
          |- txt
      |- designs
          |- figures
          |- scripts
          |- tables
      |- reports
          |- attachments
          |- temp

The program will display an error and stop if the design file is not located
within the correct folder structure.

In the common case where designs are developed and edited in interactive mode,
calculations are produced by importing the *rivet.rivet_lib* library into the
design file. Calculations can also be produced by processing the design file (or
file set) from the command line by invoking the rivet package as follows:

.. code:: python

    python rivet ddcc_ design_filename.py  (list_of_files.txt)
