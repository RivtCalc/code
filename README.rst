**rivet**
===========

**r-i-v-e-t** is the language component of **on-c-e** (OpenN Calculation
Environment), a framework for producing engineering calculation documents.
**r-i-v-e-t** is intended to improve construction productivity by producing
design documents that are easier to review and resuse. For an overview of
**on-c-e** see http://on-c-e.github.io.

A **r-i-v-e-t** file is a Python file or files that contain
design calculations using the *rivet* package. Design files
have names of the form *ddcc_designfilename.py* where dd and cc are two digit
numbers identifying the division and calculation number respectively.

Calcs and supporting files for a project are contained in a project folder
structure with names as follows:

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

The *rivet* package processes and outputs formatted calculations in utf8 text,
html, and PDF if specified (and LaTeX is installed). Output is saved in the
respective calcs folder. Output is also sent to std out (terminal) for
interactive development. The options for output in interactive development
depend on the editor or IDE used (e.g. VS Code, Pyzo, Komodo etc.). The design
file can be processed from command line (in the design folder) as follows.

.. code:: python

            python ddcc_designfilename.py


Program and documentation are here: http://r-i-v-e-t.github.io.  

**oncepy**
==========

Unzip and copy the **oncepy** package (folder) to the python/lib/site-packages
directory. From a terminal window in the model or directory type:

.. code:: python

    python -m oncepy ddmm.model.txt (-e or -b)

The -e or -b options echo the calc to a shell (-e) or a Windows
browser (-b). The -b option is needed when the shell lacks complete UTF-8
encoding.

If the program is started from a directory other than the model or
project directory, the full path needs to be prepended
to the model name.


**onceutf.py**

*onceutfnnn.py* can be run as a module or script. Copy it and a model file into
the same directory and start from a console window in that directory:

.. code:: python

    python onceutfnnn.py ddmm.model.txt (-e or -b)

where 'nnn' is the version number (i.e. 044). Alternatively copy
onceutfnnn.py to Python/Lib/site-packages and run from any directory:

.. code:: python

    python -m onceutfnnn ddmm.model.txt (-e or -b)

Rename onceutfnnn.py to onceutf.py for simpler invocation and compatibility
with *on-c-e* toolbars and macros for Komodo Edit.

**Windows**

Open a command shell window in a folder in Windows 7 or 8 by
navigating to the folder using Explorer, hold the shift key,right click,
click on 'open command window here' in the context menu.


**General**

Change the browser encoding settings if needed as follows:
::

 Browser type:
    Chrome: type chrome:settings/fonts in url bar to change settings
    Firefox: options - content - advanced - UTF-8
    Internet Explorer: right click - encoding - UTF-8

A relatively complete UTF-8 font set is needed for symbolic math
representation in an IDE.  *DejaVu Mono* fonts are recommended.

**Program links**:

**oncepy** program: http://on-c-e.org/programs/

User manual and **onceutf.py** : http://on-c-e.us

Roadmap at Trello: https://on-c-e.info

DejaVu fonts: http://dejavu-fonts.org/wiki/Main_Page

Source code and documentation: http://on-c-e.github.io/

Package author: Rod Holland once.pyproject@gmail.com
