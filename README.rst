**oncepy**
===========

The package *oncepy* and the portable module *onceutf.py* take a
*on-c-e* ASCII model *ddmm.model.txt* as input and return formatted
structural engineering calculations (calcs) in UTF-8. *oncepy* can
also return a PDF-LaTeX formatted calculation and can collect
calcs into project sets.

The programs write the calc file *calddmm.model.txt* where *ddmm* is
the model number,  *dd* is the division number, and *mm* is the model
designation.
::

 platforms:
    Anaconda, Enthought, Pythonxy or a minimum installation (see manual)
    on Windows, Linux, OSX

    onceutf.py: Wakari, PythonAnywhere web platforms
    onceutf.py: QPython, Pythonista on Android and iOS

**oncepy**

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
