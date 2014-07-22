"""
**onceutf.py**
==============
The program formats structural calculations using a simple, natural
markup language as input.  It is a single, long module that takes a
**on-c-e** model as input and returns a formatted UTF-8 calc. It runs
on local (Anaconda, Enthought, Pythonxy),
web (Wakari, PythonAnywhere), and
mobile (QPython-Android, Pythonista - iOS)
Python scientific platforms.

The module is a subset of the package **oncepy** and combines
several modules into a single file to simplify installation
and experimentation, particulary on web and mobile platforms.
incorporates the Unum and tabulate packages as classes since
they are typically not part of Python scientific distributions.
It includes **oncepy** capabilities except for
projects, PDF calcs and external units. It

Participation and feedback are very welcome.
Currently the program can run calculation models as
illustrated in the examples. Some classes and methods are
not implemented yet (see Trello roadmap). The current beta
development cycle will complete model and project operations,
add input error checking, unit tests
and package the program for pypi and other distributions.

onceutf.py, example models and the user manual can be downloaded from:

    **onceutf: ** https://on-c-e.us

    Progress is tracked at Trello: http://on-c-e.info

    Source code and documentation for are at github: http://on-c-e.github.io/

    email contact: r holland once.pyproject@gmail.com

Running the Program
===================
Copy **onceutf_nnn.py** and the model file into the same directory,
change to the directory and type, from a terminal window:

.. code:: python

    python onceutfnnn.py xxyy.model.txt (-e or -b)

        if onceutfnnn.py and model are in the same folder


    python -m onceutfnnn xxyy.model.txt (-e or -b)

        if onceutfnnn.py is copied to Python/Lib/site-packages


where 'nnn' is the version number (i.e. 040) and *xxyy.model.txt*
is the file name where xx is the chapter number and yy is the model
number.  The command lower form has the advantage of being available to
every model folder and the Komodo Edit tool buttons.


The program will write the calc file calxxyy.model.txt and the
-e or -b options will echo the calc to a console or terminal (-e) or
a Windows browser (-b). The -b option is needed on Windows because
of UTF-8 encoding limitations in the console/terminal.

To open a terminal window in a folder in Windows 7 or 8 ,
navigate to the folder using Explorer, hold the shift key,right click,
click on 'open command window here' in the context menu.

Change the browser encoding settings if needed:
-----------------------------------------------
Chrome  - type chrome:settings/fonts  in url bar -
scroll to the bottom of the dialog box and make the change

Firefox - options - content - advanced - UTF-8

Internet Explorer - right click - encoding - UTF-8

For further details refer to the  user manual and programs here:

    **oncepy**
    http://structurelabs.knackhq.com/oncedb#programs/

A relatively complete UTF-8 font set is needed for proper math
representation in an IDE.  **DejaVu Mono** fonts are recommended and
can be downloaded here:

    http://dejavu-fonts.org/wiki/Main_Page
"""
