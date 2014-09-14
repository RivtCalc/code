""" oncepy package

The package *oncepy* and the portable module *onceutf.py* take a
*on-c-e* ASCII model *ddmm.model.txt* as input and return formatted
structural engineering calculations (calcs) in UTF-8. *oncepy* can
also return a PDF-LaTeX formatted calculation and can collect
calcs into project sets.

The programs write the calc file *calddmm.model.txt* where *ddmm* is
the model number,  *dd* is the division number, and *mm* is the model
designation.
::

 oncepy and onceutf.py platforms:
    Anaconda, Enthought, Pythonxy on
    Windows, Linux, OSX

 onceutf.py platforms:
    web: Wakari, PythonAnywhere in browser
    mobile: QPython on Android, Pythonista on iOS

**Example oncepy**

Unzip and copy the **oncepy** package (folder) to the python/lib/site-packages
directory. From a terminal window type:

.. code:: python

    python -m oncepy ddmm.model.txt (-e or -b)

The -e or -b options echo the calc to a shell (-e) or a Windows
browser (-b). The -b option is needed in the Windows shell because
the shell lacks needed UTF-8 encoding.

**Example onceutf.py**

*onceutfnnn.py* can be run in two ways. Simply copy it and a model file into
the same directory and start from a console window in that directory:

.. code:: python

    python onceutfnnn.py ddmm.model.txt (-e or -b)

where 'nnn' is the version number (i.e. 044). Alternatively copy
onceutfnnn.py to Python/Lib/site-packages and run from any directory:

.. code:: python

    python -m onceutfnnn ddmm.model.txt (-e or -b)

Rename onceutfnnn.py to onceutf.py for a simpler invocation and compatibility
with *on-c-e* toolbars and macros for Komodo Edit.

**General**

Open a command shell window in a folder in Windows 7 or 8 by
navigating to the folder using Explorer, hold the shift key,right click,
click on 'open command window here' in the context menu.

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

"""
from __future__ import division
from __future__ import print_function
import locale
import os
import sys
import oncepy
from oncepy.cproj import ProjStart
from oncepy.cstart import ModStart
from oncepy.cdict import ModDicts
from oncepy.ctext import CalcUTF
from oncepy.crst import CalcRST
from oncepy.cpdf import CalcPDF
from oncepy.ccheck import ModCheck
import oncepy.oconfig as oCfg
from sympy.core.cache import *

__version__ = "0.4.5"
__author__ = 'rholland'
locale.setlocale(locale.LC_ALL, '')

#------------------------------------------------------------------------------
def _gencalc(fi4):
    """ program execution sequence
    ::

     arguments:
        fi4 (list): list of auxiliary files

    """
    ew = ModCheck()

    # generate calc file
    modinit = ModStart()
    calcf, pyf, sumf = modinit.gen_filenames()      # generate filenames
    dicts = ModDicts()                              # generate dicts
    dicts.build_dicts()
    fidict = dicts.get_fidict()
    mdict = dicts.get_mdict()
    modinit.out_term()                              # echo output if -e or -b

    oCfg.caltype = 0                                # check for PDF calc flag
    with open(oCfg.sysargv[1], 'r') as f5:
        readlines2 = f5.readlines()
    for i2 in readlines2:
        # check for #- format tag
        if len(i2.strip()) > 0:
            if i2.split('|')[0].strip() == '#- format':
                oCfg.caltype = i2.split('|')[2].strip()

    if float(oCfg.caltype) != 0:
        try:                                        # find PDF style file
            f2 = open('once.sty')
            f2.close()
            oCfg.stylefile = 'model folder'
            oCfg.stylepath = os.getcwd()
        except IOError:
            try:
                os.chdir(os.pardir)
                f3 = open('once.sty')
                f3.close()
                oCfg.stylefile = 'project folder'
                oCfg.stylepath = os.getcwd()
                os.chdir(oCfg.mpath)
            except IOError:
                os.chdir(oncepy.__path__[0])
                f4 = open('once.sty')
                f4.close()
                oCfg.stylefile = 'built-in'
                oCfg.stylepath = os.getcwd()
                os.chdir(oCfg.mpath)

    modinit.file_summary()                          # write file table
    modinit.var_table(mdict)                        # write variable table
    newmod = CalcUTF(mdict, fidict, calcf, pyf, sumf)
    newmod.gen_utf()                                # generate UTF calc
    if float(oCfg.caltype) != 0:                    # PDF calc margin
        try:
            pdfmargin = float(oCfg.caltype.strip())
        except TypeError:
            pdfmargin = 1.0

        p1 = oCfg.stylepath + "/once.sty"
        with open(p1,'r') as f2:
            newlines = []
            for line1 in f2.readlines():
                if line1[:9] == "\geometry":
                    line1 = ("\geometry{hmargin={1.0in,0.75in}"
                             ",vmargin={0.9in," + str(pdfmargin) + "in}}\n")
                newlines.append(line1)
        with open(p1, 'w') as f3:
            for line1 in newlines:
                f3.write(line1)
        # remove auxiliary files

        for i4 in fi4:                           # remove any auxiliary files
            try:
                os.remove(i4)
            except OSError:
                pass

        rstout1 = CalcRST(mdict, fidict)         # generate rst file
        rstout1.gen_rst()
        ew.errwrite("< rst file written >", 0)

        pdfout1 = CalcPDF(oCfg.mfile)            # generate PDF calc
        pdfout1.gen_tex()
        pdfout1.gen_pdf()
        ew.errwrite("< pdf file written >", 0)

#------------------------------------------------------------------------------
if __name__ == '__main__':                      # start program
    #print(sys.argv)
    oCfg.sysargv = sys.argv

    startmod = ModStart
    startproj = ProjStart

    _cleanflag = 1
    if len(oCfg.sysargv) < 2:                    # check command line input
        startmod.cmdline(__version__)
    elif oCfg.sysargv[1] == '-h':
        startmod.cmdline(__version__)
    if len(oCfg.sysargv) > 2 and '-noclean' in oCfg.sysargv:
        _cleanflag = 0                          # set clean aux files flag

    _ew = ModCheck()                            # start execution log
    _ew.logstart()


    oCfg.mfile = oCfg.sysargv[1]                  # set paths
    oCfg.mpath = os.getcwd()
    os.chdir(oCfg.mpath)
    sys.path.append(oCfg.mpath)
    #print(oCfg.mfile)
    clear_cache()                               # clear sympy cache

    with open(oCfg.sysargv[1], 'r') as _f1:      # check for project tag [p]
        _readlines1 = _f1.readlines()
    for _i1 in _readlines1:
        if len(_i1.strip()) > 0:
            #print(i1)
            if _i1.split()[0].strip()[0:3] == '[p]':
                oCfg.pfile = oCfg.sysargv[1]
                oCfg.ppath = os.getcwd()
                print("project operations are not supported yet")
                break
                #_startproj()

    rstfile = oCfg.mfile.replace('.txt', '.rst') # list of auxiliary files
    texfile = oCfg.mfile.replace('.txt', '.tex')
    auxfile = oCfg.mfile.replace('.txt', '.aux')
    outfile = oCfg.mfile.replace('.txt', '.out')
    logfile = oCfg.mfile.replace('.txt', '.log')
    texmak1 = oCfg.mfile.replace('.txt', '.fls')
    texmak2 = oCfg.mfile.replace('.txt', '.fdb_latexmk')
    fi5 = [rstfile, texfile, auxfile, outfile, logfile,
               texmak1, texmak2]

    _gencalc(fi5)                               # generate calcs

    _ew.errwrite("< calc completed >", 1)
    _ew.logclose()                              # close log

    if _cleanflag:                              # remove auxiliary files
        for i5 in fi5:
            try:
                os.remove(i5)
            except OSError:
                pass
                                                # end of program
