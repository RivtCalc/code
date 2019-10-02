#! python
"""rivet_lib - evaluate and format rivet-strings

    Specifies five functions. Each function takes a syntax specfic f-string.
    The first line of each f-string includes process parameters for the string.
    Strings are written to txt, rst, html or pdf files after evaluation and
    formatting.
    
    Methods:
        r__(fstring): run a string of python code 
        i__(fstring): evaluate a string with text and images
        v__(fstring): evaluate a string with values
        e__(fstring): evaluate a string with equations
        t__(fstring): evaluate a string with tables and plots
        _riv_strset(dictionary): set evaluation and formatting parameters
        _write_utf(string): write utf8 formatted string to stdout and calc-file
        _write_rst(string): write rst formatted string to calc-file
        _write_py(string): write equations and values to python file
"""

import os
import sys
from pathlib import Path
from typing import List, Set, Dict, Tuple, Optional

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy.linalg as la
import pandas as pd
import rivet.rivet_check as _chk
import rivet.rivet_utf as _utf
import sympy as sy
from IPython.display import HTML, Image, Latex, Math, display
from numpy import *
from rivet.rivet_unit import *

import __main__

#import rivet.rivet_rst as _rst
#import rivet.rivet_reprt as _reprt

__version__ = "0.9.1"
__author__ = "rholland"
if sys.version_info < (3, 7):
    sys.exit("rivet requires Python version 3.7 or later")

# set up folders, files and dictionaries
_rivfile = __main__.fileset["file"]
_rivbase = __main__.fileset["file"].split(".")[0]
_rivpath = __main__.fileset["path"]
_rivfull = Path(_rivpath / _rivfile)
_rivbak = Path(_rivpath / _rivfile.split(".")[0]+".bak")
_txtfile =  ".".join((_rivbase, "txt"))
_logfile =  ".".join((_rivbase, "log"))
_rivetpath = os.path.dirname("rivet.rivet_lib.py")
_projpath = os.pardir
_opt = __main__.fileset["opt"]

_folders = {
"reptpath" : os.path.join(os.pardir, "reports"),
"spath": Path(_rivpath / "scripts"),
"tpath": Path(_rivpath["adpath"] / "table"),
"upath": Path(_rivpath["adpath"] / "txt"),
"rpath": Path(_rivpath["reptpath"] / "pdf"),
"xpath": Path(_rivpath["reptpath"] / "temp"),
"fpath": Path(_rivpath["reptpath"] / "figures"),
"hpath": Path(_rivpath["reptpath"] / "html")
}    

rivet_dict = {}
equation_list = []
_calcnum = _rivbase[:3]
_calcwidth = 80; _sectnum = 0; _eqnum = 0; _fignum = 0
_strset =[_calcwidth, _sectnum, _eqnum, _fignum]

# initial checks on input
with open(_rivfull, "r") as f2:
    adbak = f2.read()
with open(_rivbak, "w") as f3:
    f3.write(adbak)
print("\n\npath: ", _rivpath, "; ", _rivfile)
print("checks: folders checked; file backup written to temp folder", "\n\n")

# start checks and logs
#_chk1 = chk.CheckRivet(_tlog)
#_chk1.logstart()
#_chk1.logwrite("< begin model processing >", 1
# os.chdir(once.__path__[0])
# f4 = open('once.sty')
# f4.close()
# os.chdir(cfg.ppath)
# _el.logwrite("< style file found >", vbos)
# os.system('latex --version')                
# _el.logwrite("< Tex Live installation found>", vbos)
# pdfout1.gen_pdf() 

def _riv_strset(line1: string) -> Tuple(str, str, int, List[int]):
    """ parse rivet-string settings
    
    Args:
        line1 (string): rivet-string settings (from first line)
    
    Returns:
        Tuple[int,str,str]: exec flag, str description, str type
    """
    #print(line1)
    _strnum = [_opt[4], -1, 0, 0]
    sect_num = _strnum[1]
    exec_flg  = -1 
    str_descrip  = " "
    str_type = " "
    line2 = line1.split("|")[1]
    str_type = line2[0].strip()
    sect_num = line2.find("]]")
    if sect_num > -1:
        str_descrip = line2[sect_num + 1:].strip()
        sect_num = line2[sect_num-2:sect_num]
        sect_num = sect_num.strip("]]").strip("[[")
        _strnum[1] = sect_num
    if "--hide" in line2:
        exec_flg = 1
        str_descrip = line2[0].replace("--hide","").strip()                
    else:
        exec_flg = 0
    return [str_type, str_descrip, exec_flg, _strnum]

def _write_rst(pline, pp, indent):
    """[summary]
    
    Args:
        pline ([type]): [description]
        pp ([type]): [description]
        indent ([type]): [description]
    """
    pdf_files = {
        "cpdf":  ".".join((_rivbase, "pdf")),
        "chtml":  ".".join((_rivbase, "html")),
        "trst":  ".".join((_rivbase, "rst")),    
        "ttex1":  ".".join((_rivbase, "tex")),
        "auxfile": ".".join((_rivbase, ".aux")),
        "outfile":  ".".join((_rivbase, ".out")),
        "texmak2":  ".".join((_rivbase, ".fls")),
        "texmak3":  ".".join((_rivbase, ".fdb_latexmk"))
    }

def _write_py(self):
    """ write rivet independent python file
 
        Write an executable Python file without rivet_lib dependencies 
        but with other imports, values, and equations while excluding
        explanatory text and formatting.  Useful for extensions of analysis 
        and design and importing design information into other rivet files.      
    """
    str1 =  ("""\nThis file contains Python equations from the
            on-c-e model \n\n  '+ self.mfile + '\n
            \nFor interactive analysis open the file\n
            in an IDE executable shell e.g. Pyzo,\n
            Spyder, Jupyter Notebook or Komodo IDE \n
            import os\n
            import sys\n
            from sympy import *\n
            from numpy import *\n
            import numpy.linalg as LA\n
            import importlib.util\n
            import once.config as cfg\n     
            \ndef vlist(vlistx = vlist1, vlisty= vlist2):\n
            Utility function for interactively listing once\n
            variable values. Variables are stored in vlist1 and
            definitions in vlist2. Type vlist()\n
            to list updated variable summary after executing\n
            calc Python script\n\n\n
            for lsti in zip(vlistx, vlisty):\n
                item1 = eval(str(lsti[0]))\n
                def1 = lsti[1]\n
                cncat1 = str(lsti[0]) + " = " + str(item1) + " "*30\n
                print(cncat1[:25] + "# " + def1)\n\n
            if __name__ == "__main__":\n
                   vlist()\n\n""")
    _rivfile.write("\n")

def _write_utf(rivstring: List[str], _strset: List[str]):
    """ write model text to utf-8 encoded file.
    
    Args:
        mentry (string): text 
        pp (int): pretty print flag
        indent (int): indent flag
         
    """
    rivstring1 = []
    sect_num = int(_strset[3][1])
    descrip = _strset[2]
    _calcwidth = int(_strset[3][0])
    if sect_num > -1:
        rivstring1.append('=' * _calcwidth)
        descrip1 = " " +  descrip + (_calcnum + "-" +
            sect_num).rjust(_calcwidth - len(descrip) - 2)
        rivstring1.append('=' * _calcwidth)
    rivstring2 = rivstring1 + rivstring
    f1 = open(_rivfull, 'a')
    f1.write(rivstring2)
    f1.close()
    print(rivstring2)
    
def r__(fstr: string):
    """ evaluate and format a rivet-string
    
    Args:
        fstr (string): [description]
    """
    fstr1 = fstr.split("\n", 1)
    fstr2 = fstr1[1].splitlines()
    _strset = _riv_strset(fstr1[0])
    if _strset[0] == "r": rs__(_strset, fstr2)
    elif _strset[0] == "i": is__(_strset, fstr2)
    elif _strset[0] == "v": vs__(_strset, fstr2)
    elif _strset[0] == "e": es__(_strset, fstr2)
    elif _strset[0] == "t": ts__(_strset, fstr2)
    else:
        print(fstr2, " < rivet string type not found >")
    

def rs__(_strset: List[int], fstr2: List[str]):
    """ execute and format a rivet-string of python code
    
    Args:
        fstr (string): [description]
    """
    calc = _utf.Rexec_u(fstr2, rivet_dict)
    dict1, calc1, equ1 = calc.r_utf()

    if _strset[0] == 0: 
        _write_utf(calc1, _strset)

    equation_list.append(equ1)
    rivet_dict.update(dict1)

def is__(_strset: List[int], fstr2: List[str]):
    """ format a rivet-string of text and images
    
    """
    calc = _utf.Iexec_u(fstr2, rivet_dict, _folders, _strset)
    dict1, calc1, equ1 = calc.i_utf()
    
    if _strset[3] == 0: 
        _write_utf(calc1, _strset)
    
    equation_list.append(equ1)
    rivet_dict.update(dict1)

def vs__(_strset: List[int], fstr2: List[str]):
    """evaluate and format a rivet-string of values

    """
    calc = _utf.Vexec_u(fstr2, rivet_dict, _folders,  _strset)
    dict1, calc1, equ1 = calc.v_utf()
    
    if _strset[0] == 0: 
        _write_utf(calc1)
    
    equation_list.append(equ1)
    rivet_dict.update(dict1)    

def es__(_strset: List[int], fstr2: List[str]):
    """evaluate and format a rivet-string of equations

    """

    if _strset[0] == 2: return
    calc = _utf.Eexec_u(fstr2, rivet_dict)
    dict1, calc1, equ1 = calc.e_utf()
    if _strset[0] == 0: _write_utf(calc1)
    equation_list.append(equ1)
    rivet_dict.update(dict1)

def ts__(_strset: List[int], fstr2: List[str]):
    """evaluate and format a rivet-string of tables
    
    """

    if _strset[0] == 2: return
    calc = _utf.Texec_u(fstr2, rivet_dict)
    dict1, calc1, equ1 = calc.t_utf()
    if _strset[0] == 0: _write_utf(calc1)
    equation_list.append(equ1)
    rivet_dict.update(dict1)
