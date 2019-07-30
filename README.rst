**rivet**
===========

**r-i-v-e-t** is an example of the calculation language component for **on-c-e**
(OpeN  Calculation Environment), which produces engineering calculation
documents. It is written in Python 3 and is designed to improve document reuse
and review. For an overview of **on-c-e** see http://on-c-e.github.io.

A **r-i-v-e-t** calculation is a Python engineering design file files that
contain design calculations in the **r-i-v-e-t** format and import the rivet_lib
library. Design files for a project have names of the form
*ddcc_designfilename.py* where dd and cc are two digit numbers identifying the
division and calculation number respectively.  Division numbers apply to
**r-i-v-e-t**  reports which are organized compilations of calculations.

Design input files and their required supporting files must be stored in the
proper subfolders of the *designs* folder. Output files are written to the
*calcs* directory in html, pdf and text (utf) format. To protect against data
loss the user must set up the project folder structure using the following
names.  The program will display an error and stop if it does not find the
proper folder structure and names. ::

  Project_Name (by user)
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

The *rivet* package processes and outputs formatted calculations.  In the common
case where calculations are written and edited in interactive  mode,  the
program is invoked by importing the *rivet_lib* library.  Calculations can also
be produced by processing an entire design file from the commmand line by invoking the
rivet package as follows:

.. code:: python

    python rivet ddcc_ userdescrip.py

The program and documentation are here: http://r-i-v-e-t.github.io.
