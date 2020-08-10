**r-i-v-e-t**
==============

**r-i-v-e-t** is a writing tool for engineering calculation reports that
may be used either as a Python library or as a command line program.  It is  
designed to work with **on-c-e** (**O**\ pe\ **N** **C**\ alculation **E**\ cosystem). 

From the command line:

.. code:: python

    python rivt ddcc_ rivtfilename.py  (or batch_of_files.txt)

As a library:

.. code:: python

    from rivt_lib import *

Like **on-c-e** its focus is on improving the resuse, review, reach and reliability of
engineering calculation reports. Code and documentation are here: https://github.com/r-i-v-e-t .  
For an overview of **on-c-e** see https://github.com/on-c-e .

A **r-i-v-e-t** file is a Python text file containing engineering design and analysis
calculations written in ASCII or UTF-8. Any text processor (i.e. Notepad) can be used to create 
and edit a design file but an IDE or code editor significantly improves efficiency, allows for interactive design development
and is strongly recommended.  **r-i-v-e-t** documentation  is written around the code editor Microsoft VS Code. 
The *rivt* program has a single primary function, *__r("rivt-string")*,  which takes a single string as argument. 
The first  character of each string is one of **r, i, v, e, t**,  which controls the rivt syntax and 
operations within that context. The characters signify the following::

    r -> run Python code
    i -> insert text, tables and figures
    v -> assign values to variables
    e -> evaluate equations
    t -> generate and manipulate tables and plots
    
**r-i-v-e-t** evaluates rivt files (designs) and outputs calculation files (calcs) in UTF-8, HTML 
or PDF formats. Design files have names of the form *ddcc_rivtfilename.py* where dd and cc are 
two digit numbers identifying the division and calculation number respectively. Division 
numbers apply to **r-i-v-e-t**  reports, which are organized compilations of calcs.
Calc output files retain the design file name with a modified file-type suffix (txt, html, pdf), 
depending on the output type selected.

**r-i-v-e-t** files are used within the context of a project. The user initially sets 
up a **r-i-v-e-t** project by creating a project folder structure using the following 
naming conventions::

  User_project_name 
      |- calcs
        |- scripts
        |- sketches
        |- tables
      |- reports
        |- html
          |- figures
          |- append
        |- temp
        
Design (input) files and utf8-calc (output) files are read from and written to the *calcs* folder. Supporting 
design files are stored in the *calcs* sub-folders. All supporting files are  ASCII or UTF-8 text files, 
as are the rivt design and utf8-calc files. A zip of the *calc* folder and sub-folders may be uploaded to a shared online 
database.

**pdf-** calcs and reports are written to the *reports* folder. **html-** calcs and reports are 
written to the *html* folder. Images (png and jpg) and PDF reference documents, used in 
**pdf-** and **html-** calcs and reports, are stored in the *figures* and *append* folders respectively.
