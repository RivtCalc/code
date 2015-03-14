""" oncepy package

The portable module *onceutf.py* and full package *oncepy* take a
*on-c-e* ASCII calc input file *ffdd.inputname.txt* and return UTF-8 formatted
structural engineering calculation. *oncepy* can also return a
PDF-LaTeX formatted calculation and organize calcs into project sets.

The programs write the calc file *ffddcalc.inputname.txt* where *ffdd* is
the calc number,  *ff* is the division folder number, and *dd* is the calc
designation.
::

 platforms:
    oncepy and onceutf.py on Windows, Linux, OSX:
    Anaconda, Enthought, Pythonxy, Pyzo

    onceutf.py web-based: Wakari, PythonAnywhere
    onceutf.py mobile: QPython, DroidEdit on Android, Pythonista on iOS

**oncepy**

Unzip and copy the **oncepy** package (folder) to the python/lib/site-packages
directory. From a terminal window in the model or directory type:

.. code:: python

    python -m oncepy ffdd.calcname.txt [-t, -b, -o] [-nn]

    -t echoes the UTF output to the terminal
    -b opens the PDF ouptut in the browser
    -o opens the PDF output in the .txt os-associated program

    -nn is the UTF output line width from 72 to 90 (default is 80)

If the program is started from a directory other than the model or
project directory, the full path must be prepended
to the calc name.


**General**


On Windows 7 or 8, open a command shell window in a folder by
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

**oncepy** program:     http://on-c-e.org/programs/

**onceutf.py** program: http://on-c-e.us

User manual:            http://on-c-e.info

Roadmap:                https://on-c-e.net

Source code:            http://on-c-e.github.io/

DejaVu fonts:           http://dejavu-fonts.org/wiki/Main_Page

author - Rod Holland:   once.pyproject@gmail.com


"""
from __future__ import division
from __future__ import print_function
import subprocess
import time
import locale
import os
import glob
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

__version__ = "0.5.4"
__author__ = 'rholland'
locale.setlocale(locale.LC_ALL, '')

#------------------------------------------------------------------------------
def _cmdline():
    """command line help"""
    print()
    print("onceutf" + __version__ + ": writes on-c-e UTF calcs")
    print()
    print("Use:")
    print("python onceutf.py ffdd.calcfile.txt (options)")
    print("   when onceutf.py is in calc folder")
    print("         or")
    print("python -m onceutf ffdd.calcfile.txt (-h, -s, -b, -o) (-nn)")
    print("   when onceutfnnnn.py is in Python /Lib/site-packages")
    print()
    print()
    print("options:")
    print("   -h   prints this prompt")
    print("   -nn  set UTF-8 calc width (72 to 90 characters - 80 default)")
    print("   -t   echoes UTF-8 calc to terminal (stdout)")
    print("   -o   opens UTF-8 calc in operating system associated program")
    print("   -b   opens UTF-8 calc in Windows browser")
    print("        trying the following commands in order:")
    print("             start chrome ddff.calcfile.txt ")
    print("             start firefox ddff.calcfile.txt")
    print("             start iexplore file:///%CD%/ddff.calcfile.txt")
    print("        set browser encoding to UTF-8; refer to user manual")
    print()
    print("outputs:")
    print("   _calclog.calcfile.txt")
    print()
    print("if no errors then outputs:")
    print("   ffddcalc.calcfile.txt (UTF-8 calc")
    print("   _equations.py (IPython and database input)")


def _outterm(echoflag, calctyp):
    """-e, -b or -p flag echoes calc to console or browser
    ::

     -b switch needed primarily on Window where UTF-8 is missing

    """
    # onceweb modified
    if echoflag == 't':
        print()
        print("|======================  "
                "echo calc  =====================|")
        print()
        try:
            with open(calcf, 'r') as mod1:
                for i in mod1.readlines():
                    print(i)
        except OSError:
            pass
    elif echoflag == 'b':
        try:
            os.system("start chrome " + calctyp)
        except OSError:
            try:
                os.system("start firefox " + calctyp)
            except OSError:
                try:
                    os.system("start iexplore file:///%CD%/" + calctyp)
                except OSError:
                    pass
    elif echoflag == 'o':
        try:
            subprocess.Popen(calctyp, shell=True)
        except OSError:
            pass

def _gencalc(fi4):
    """ program execution
    ::

     arguments:
        fi4 (list): list of auxiliary files

    """
    ew = ModCheck()

    # generate calc file
    modinit1 = ModStart()
    calcf1, pyf1, sumf1, pdff1 = modinit1.gen_filenames() # generate filenames

    #start calc file early to avoid Komodo dialog prompt
    with open(calcf1,'w') as f1:
        f1.write(time.strftime("%c") + "     onceutf version: " + __version__)

    dicts = ModDicts()                              # generate dicts
    dicts.build_dicts()
    fidict = dicts.get_fidict()
    mdict = dicts.get_mdict()

    oCfg.caltype = 0                                # check for PDF calc flag
    with open(oCfg.sysargv[1], 'r') as f5:
        readlines2 = f5.readlines()
    for i2 in readlines2:
        # check for #- formateq tag
        if len(i2.strip()) > 0:
            if i2.split('|')[0].strip() == '#- formateq':
                oCfg.caltype = i2.split('|')[2].strip()

    if float(oCfg.caltype) != 0:
        try:
            os.system('latex --version')             # check for LaTeX
            try:                                     # find PDF style file
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
        except(OSError):
            oCfg.caltype = 0
            _ew.errwrite("< latex not installed - PDF calc not generated >", 1)

    modinit1.file_summary()                          # write file table
    modinit1.var_table(mdict)                        # write variable table
    newmod = CalcUTF(mdict, fidict, calcf1, pyf1, sumf1)
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

        pdfout1 = CalcPDF(oCfg.mfile, oCfg.mpath)            # generate PDF calc
        pdfout1.gen_tex()
        pdfout1.gen_pdf()
        ew.errwrite("< pdf file written >", 0)

        odict1 = newmod.get_odict()
        return odict1

#------------------------------------------------------------------------------

if __name__ == '__main__':                  # start program
    #print(sys.argv)
    oCfg.sysargv = sys.argv
    _echoflag = ''

    startmod = ModStart
    startproj = ProjStart

    _ew = ModCheck()                        # start execution log
    _ew.logstart()

    if '-h' in sys.argv:
        _cmdline()
        sys.exit(1)

    _cleanflag = 1
    if '-noclean' in sys.argv:
        _cleanflag = 0                       # set clean aux files flag

    try:
        mfile = os.path.basename(sys.argv[1])  # model name
        mpath = os.path.dirname(sys.argv[1])   # model path
        if len(mpath) == 0:
            mpath = os.getcwd()
        os.chdir(mpath)                       # set model directory as pwd
        f2 = open(mfile, 'r')                 # does model exist in cur dir
        f2.close()

        if len(oCfg.sysargv) > 2:             # echo flag
            if '-t' in oCfg.sysargv:
                _echoflag = 't'
            elif '-b' in oCfg.sysargv:
                _echoflag = 'b'
            elif '-o' in oCfg.sysargv:
                _echoflag = 'o'

        print('echoflag', _echoflag)
        for _w1 in oCfg.sysargv:
            try:
                oCfg.calcwidth = int(_w1[1:].strip())
            except:
                pass
        _ew.errwrite('< UTF calc width = ' + str(oCfg.calcwidth) + ' >', 1)

    except IOError:
        _ew.errwrite(sys.argv[1] + ' not found', 1)
        sys.exit(1)

#            projdiv = mfile.strip()[0:2]      # look for model below proj dir
#            mpath = glob.glob(mpath + "/" + projdiv + "*")[0]
#            os.chdir(mpath)
#            f2 = open(mfile,'r')              # does model exist in cur dir
#            f2.close()


    os.chdir(mpath)
    oCfg.mfile = mfile                      # set paths
    oCfg.mpath = mpath
    os.chdir(oCfg.mpath)
    sys.path.append(oCfg.mpath)
    #print(oCfg.mfile)
    clear_cache()                           # clear sympy cache

    with open(oCfg.sysargv[1], 'r') as _f1: # check for project tag [p]
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

    rstfile = oCfg.mfile.replace('.txt', '.rst')  # list of PDF auxiliary files
    texfile = oCfg.mfile.replace('.txt', '.tex')
    auxfile = oCfg.mfile.replace('.txt', '.aux')
    outfile = oCfg.mfile.replace('.txt', '.out')
    logfile = oCfg.mfile.replace('.txt', '.log')
    texmak1 = oCfg.mfile.replace('.txt', '.fls')
    texmak2 = oCfg.mfile.replace('.txt', '.fdb_latexmk')
    fi5 = [rstfile, texfile, auxfile, outfile, logfile,
               texmak1, texmak2]

    _ew.errwrite(" ", 1)
    _ew.errwrite("< begin calc processing >", 1)
    _ew.errwrite(" ", 1)

    os.chdir(mpath)
    sys.path.append(mpath)
    odict2 = _gencalc(fi5)                  # generate calcs

    _vardef =[]                             # gen list of equations for shell
    try:
        for k1 in odict2:                   # exec eq and overwrite symbolics
            if k1[0] != '_' or k1[0:2] == '_a':
                    try:
                        exec(odict2[k1][1].strip())
                        if '=' in odict2[k1][1].strip():
                            _vardef.append(odict2[k1][1].strip())
                    except:
                        pass
                    if k1[0:2] == '_a':
                        try:
                            exec(odict2[k1][3].strip())
                            if '=' in odict2[k1][3].strip():
                                _vardef.append(odict2[k1][3].strip())
                        except:
                            pass
                        try:
                            exec(odict2[k1][4].strip())
                            if '=' in odict2[k1][4].strip():
                                _vardef.append(odict2[k1][4].strip())
                        except:
                            pass
    except:
        print("equation dictionary is empty")

    _ew.errwrite("< calc completed >", 1)
    _ew.logclose()                              # close log

                                                # echo calc
    modinit2 = ModStart()
    calcf2, pyf2, sumf2, pdff2 = modinit2.gen_filenames()     # generate filenames

    try:
        if _echoflag == 't' or _echoflag == 'b':
            _outterm(_echoflag, calcf2)
        elif _echoflag == 'o':
            _outterm(_echoflag, pdff2)
    except:
        pass

    if _cleanflag:                              # remove auxiliary files
        for i5 in fi5:
            try:
                os.remove(i5)
            except OSError:
                pass
                                                # end of program
