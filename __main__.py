#!

""" on-c-e
The program is wwritten in pure Python and produces formatted, searchable
calculation documents that are suitable for structural engineering collaboration
and construction permit packages. 

The program takes a **on-c-e** markup ASCII input file with a filename of the
form *mrrcc_modelname.txt* and returns a UTF-8 formatted calculation file
*crrcc_modelname.txt* and an optional PDF-LaTeX formatted file (including
graphics) *crrcc.modelname.pdf* if **Tex Live** is installed;
 where **rrcc** is the calculation number made up of a report 
 **rr** and calculation **cc** section number reference.

All calcs and supporting files for a project are contained in a project folder
with the following required subfolders: *calc, image, scrpt, table, temp*.
The subfolders are created by the program if they do not exist.  The *model*
subfolder must exist for the program to run. 

The program takes text files tagged with **on-c-e** markup as input, referred to
as models, and processes them through **sympy**, **docutils** and
**LaTeX** libraries into formatted text or PDF calculation files, referred to as
calcs.

OS Platforms: Windows, Linux, OSX, iOS (Pythonista), Android (QPython3)
Recommended IDE: Komodo X or Komodo Edit X 
Compatible IDE: Notepad++, Atom 
Interactive: Python shell, IPython, Jupyter 

**Test the installation**
Copy the **on-c-e** program folder to the *python/Lib/site-packages* folder and
open a terminal window in any folder, referred to as the project folder.
Type the following:

.. code:: python

            python -m once


which will display help. Next type

.. code:: python

            python -m once -test
            

which writes the built-in example model *m0101_example.txt*
to the project folder and runs it.

**Program links**
contact:                    once.pyproject@gmail.com
overview:                   http://structurelabs.com/once
program and source docs:    http://on-c-e.github.io/
database:                   http://on-c-e.net
English forum:              http://zero-construction-productivity-growth.net
Brazil forum:               http://on-c-e-br.net
Japan forum:                http://on-c-e-jp.net
India forum:                http://on-c-e-in.net
China forum:                http://on-c-e-cn.net
Mexico forum:               http://on-c-e-mx.net
**Other links**
Python distribution:        https://www.continuum.io/downloads
Komodo IDE:                 https://www.activestate.com/komodo-ide
Komodo Edit:                https://www.activestate.com/komodo-edit
DejaVu fonts:               http://dejavu-fonts.org/wiki/Main_Page
Tex Live (LaTex):           https://www.tug.org/texlive/
"""

from __future__ import division, print_function
import sys
import os
from once import config as cfg
from once.calcheck import *
from once import calstart

__version__ = "0.9.0"
__author__ = 'rholland'
#locale.setlocale(locale.LC_ALL, '')

                                                        
if __name__ == '__main__': 
    print(sys.argv)
    cfg.sysargv = sys.argv                               # read command line
    try:
        _mfile = cfg.mfile = sys.argv[1].strip()         # model name
        _mpath = cfg.mpath = os.getcwd()                 # model path
        _ppath = cfg.ppath = os.path.split(_mpath)[0]    # project path
        #print("model file", _mpath, _mfile)
        _f2 = open(_mfile, 'r')                          # does model exist
        _f2.close()
    except:                                              # run a utility script
        try:
            if '-s' == sys.argv[1].strip():
                _spath = os.path.join(oncedir, "calscripts")
                shellcmd = str(sys.argv[2])
                _scpath = os.path.join(_spath, shellcmd)
                shellcmd2 = "python " + _scpath 
                #print("shell command: ", shellcmd2)
                os.system(shellcmd2)
                sys.exit(1)
            else:
                calstart.cmdlinehelp()
                sys.exit(0)    
        except:
            sys.exit(1)
 
    _ofolders = ('dbcalc', 'dbscrpt', 'dbtable', 'rprt','temp','image') 
    
    _calcnum = cfg.calcnum =  _mfile.split('_')[0][1:]   # write names to cfg
    _mbase = cfg.mbase = _mfile.split('.')[0] 
    _cfilepdf = cfg.cfilepdf = "c" + _mbase[1:] + ".pdf"
    _cfileutf = cfg.cfileutf = "c" + _mbase[1:] + ".txt"
    _cfilepy = cfg.cfilepy = _mbase + ".py" 
    _tpath = cfg.tpath = os.path.join(_ppath, "dbtable")
    _spath = cfg.spath = os.path.join(_ppath, "dbscrpt")
    _cpath = cfg.cpath = os.path.join(_ppath, "dbcalc")
    _ipath = cfg.ipath = os.path.join(_ppath, "image")   
    _rpath = cfg.rpath = os.path.join(_ppath, "reprt")   
    _xpath = cfg.xpath = os.path.join(_ppath, "temp")
    _logfile = cfg.logfile = _calcnum + ".log.txt"           # temp folder
    _logpath = cfg.logpath = os.path.join(_xpath, _logfile)
    _texfile = cfg.texfile = _mbase + ".tex"
    _texmak1 = cfg.texfile2 = os.path.join(_xpath, _texfile)
    _rstfile = cfg.rstfile = os.path.join(_xpath, _mbase + '.rst')     
    _auxfile =  os.path.join(_xpath, _mbase + '.aux')
    _outfile =  os.path.join(_xpath, _mbase + '.out')
    _texmak2 =  os.path.join(_xpath, _mbase + '.fls')
    _texmak3 =  os.path.join(_xpath, _mbase + '.fdb_latexmk')

    _calcfiles = (_cfileutf, _cfilepdf, _cfilepy, _texfile)   # file lists
    _cleanlist = (_rstfile, _auxfile, _outfile, _texmak2, _texmak3)
    
    _el = ModCheck()
    _logwrite = _el.logstart()                          # start log
    _el.logwrite("< begin model processing >", 1)
    calstart._filesummary()                             # write file summary
    with open(_mfile, 'r') as f1:
        readlines1 = f1.readlines()
        calstart._paramline(readlines1[0])              # write config flags 
    os.chdir(_ppath)                                    # set project path
    sys.path.append(_ppath)
    mdict1 = calstart._gencalc()                        # run calc   
    
    # on return clean up and echo result summaries
    vbos = cfg.verboseflag
    if cfg.cleanflag:                                   # check noclean flag
        _el.logwrite("<cleanflag setting = " + str(cfg.cleanflag) + ">", vbos)
        os.chdir(_tpath)
        for _i4 in _cleanlist:                            
            try:
                os.remove(_i4)
            except OSError:
                pass
        os.chdir(_ppath)
    if cfg.echoflag:                                    # check echo calc flag 
        _el.logwrite("<echoflag setting = " + str(cfg.echoflag) +">", vbos)
        try:
            with open(_cfile, 'r') as file2:
                for il2 in file2.readlines():
                    print(il2.strip('\n'))
        except:
            _el.logwrite("< utf calc file could not be opened >", vbos)    
    if cfg.openflagpdf:                                 # check open PDF flag 
        try:
            pdffilex = os.path.join(_ppath, _cpath, _cfilepdf)
            os.system(pdffilex)
        except:
            _el.logwrite("< pdf calc file could not be opened >", vbos)

    calstart._variablesummary()                          # echo calc results
    _el.logwrite("< end of once program >", 1)
    _el.logclose()                                      # close log
                                                        # end of program
