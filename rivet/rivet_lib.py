#! python
"""rivet_lib - evaluate and format rivet-strings

    Specifies five functions. Each function takes a syntax specfic f-string.
    The first line of each f-string includes process parameters for the string.
    Strings are written to txt, rst, html or pdf files after evaluation and
    formatting.
    
    Methods:
        r__(fstring): run python code 
        i__(fstring): evaluate text and images
        v__(fstring): evaluate values
        e__(fstring): evaluate equations
        t__(fstring): evaluate tables and plots
        _riv_strset(dictionary): set evaluation and formatting parameters
        _write_utf(string): write utf8 formatted string to stdout and calc-file
        _write_rst(string): write rst formatted string to calc-file
        _write_py(string): write equations and values to python file
"""

import os
import sys
from pathlib import Path
from typing import List, Set, Dict, Tuple, Optional

from numpy import *
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy.linalg as la
import pandas as pd
import sympy as sy
from IPython.display import HTML, Image, Latex, Math, display
import rivet.rivet_check as _chk
import rivet.rivet_utf as _utf
from rivet.rivet_unit import *
#import rivet.rivet_rst as _rst
#import rivet.rivet_reprt as _reprt

import __main__

__version__ = "0.9.1"
__author__ = "rholland"
if sys.version_info < (3, 7):
    sys.exit("rivet requires Python version 3.7 or later")

# set up files, folders and dictionaries
_rivfull = Path(__main__.__file__)
_rivfile = Path(__main__.__file__).name
_rivbase = (Path(_rivfull).name).split(".py")[0]
_rivpath = Path(_rivfull).parent
_projpath = Path(_rivfull).parent.parent
_rivbak = Path(_rivpath / str(_rivbase + ".bak"))
_txtfile =  ".".join((_rivbase, "txt"))
_logfile =  ".".join((_rivbase, "log"))
_rivetpath = os.path.dirname("rivet.rivet_lib.py")
_folders = {
"spath": Path(_rivpath / "scripts"),
"tpath": Path(_rivpath / "tables"),
"rpath": Path(_projpath / "pdf"),
"xpath": Path(_projpath / "temp"),
"fpath": Path(_projpath / "figures"),
"hpath": Path(_projpath / "html"),
"reptpath": Path(_projpath / "reports")
}    
rivdat: dict = {"test" : 1}
rivet: dict = {}
equations: list = []
_calcnum: int = _rivbase[:3]
_calcwidth = 80; _sectnum = 0; _eqnum = 0; _fignum = 0

# initial checks on input
with open(_rivfull, "r") as f2:
    designbak = f2.read()
with open(_rivbak, "w") as f3:
    f3.write(designbak)
print("\n\nfile: ", _rivfile)
print("path: ", _rivpath)
print("checks: folders checked; file backup written to temp folder", "\n\n")

def _logs():
    #_chk1 = _chk.CheckRivet(_tlog)
    pass

def _riv_strset(line1: str) -> tuple:
    """ parse rivet-string settings
    
    Args:
        line1 (string): rivet-string settings (from first line)
    
    Returns:
        tuple: exec flag, str description, str type
    """
    #print(line1)
    opt = rivdat["opt"]
    strnum = [int(opt[1]), -1, 0, 0]
    sect_num = strnum[1]
    eq_num = strnum[2]
    fig_num =strnum[3]
    str_descrip = " "
    exec_flg  = -1 
    line2 = line1.split("|")[1]
    str_type = line2[0].strip()
    sect_num = line2.find("]]")
    if sect_num > -1:
        str_descrip = line2[sect_num + 1:].strip()
        sect_num = line2[sect_num-2:sect_num]
        sect_num = sect_num.strip("]]").strip("[[")
        strnum[1] = sect_num
    if "--hide" in line2:
        exec_flg = 1
        str_descrip = line2[0].replace("--hide","").strip()                
    else:
        exec_flg = 0
    return [str_type, str_descrip, exec_flg, strnum]

def _write_py(self):
    """ write rivet independent python file
 
        Write an executable Python file without rivet_lib dependencies 
        but with other imports, values, and equations while excluding
        explanatory text and formatting.  Useful for extensions of analysis 
        and design and importing design information into other rivet files.      
    """
    str1 =  ("""\nThis file contains Python equations 
            from the rivet design file 
            for lsti in zip(vlistx, vlisty)
            if __name__ == "__main__":\n
            vlist()\n\n""")
    _rivfile.write("\n")

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

def _write_utf(rivstring: List[str], strset: list):
    """ write model text to utf-8 encoded file.
    
    Args:
        mentry (string): text 
        pp (int): pretty print flag
        indent (int): indent flag
         
    """
    rivstring1 = []
    sect_num = int(strset[3][1])
    descrip = strset[2]
    calcwidth = int(strset[3][0])
    if sect_num > -1:
        rivstring1.append('=' * calcwidth)
        descrip1 = " " +  descrip + (_calcnum + "-" +
            sect_num).rjust(calcwidth - len(descrip) - 2)
        rivstring1.append('=' * calcwidth)
    rivstring2 = rivstring1 + rivstring
    with open(Path(_rivpath / _txtfile), 'a') as f1:
        f1.writelines(rivstring2)
    print(*rivstring2, sep="\n")
    
def r__(fstr: str):
    """ select rivet-string type
    
    Args:
        fstr (string): [description]
    """
    global rivdat
    fstr1 = fstr.split("\n", 1)[0]
    fstr2 = fstr.split("\n", 1)[1]
    if fstr1[0] == "r": rs__(fstr1, fstr2)
    elif fstr1[0] == "i": is__(fstr1, fstr2)
    elif fstr1[0] == "v": vs__(fstr1, fstr2)
    elif fstr1[0] == "e": es__(frstr1, fstr2)
    elif fstr1[0] == "t": ts__(fstr1, fstr2)
    else:
        print(" < rivet string " + str(fstr1[0]) + " type not found >")
    
def rs__(fstr1: str, fstr2: str):
    """ execute and format a rivet-string of python code
    
    Args:
        fstr (string): [description]
    """
    global rivdat
    fstr3 = "".join(fstr2.split("\n"))
    fstr3 = fstr3.replace(" ","") 
    exec(fstr3, globals())
    strset = _riv_strset(fstr1)
    #calc = _utf.Rexec_u(fstr2.split("\n"))
    #dict1, calc1, equ1 = calc.r_utf()

    if strset[2] == 0: _write_utf(fstr2.split("\n"), strset)

    #equations.append(equ1)
    #rivet.update(dict1)
    #globals.update(dict1)

def is__(fstr1: str, fstr2: str):
    """ format a rivet-string of text and images
    
    """
    strset = _riv_strset(fstr1)
    calc = _utf.Iexec_u(fstr2.split("\n"), rivet, _folders, strset[3])
    dict1, calc1, equ1 = calc.i_str()
    
    if strset[2] == 0: _write_utf(calc1, strset)
    
    equations.append(equ1)
    rivet.update(dict1)
    globals.update(dict1)

def vs__(fstr1: str, fstr2: List[str]):
    """evaluate and format a rivet-string of values

    """
    strset = _riv_strset(fstr1)
    calc = _utf.Vexec_u(fstr2.split("\n"), rivet, _folders,  strset)
    dict1, calc1, equ1 = calc.v_utf()
    
    if fstr1[0] == 0: _write_utf(calc1)
    
    equations.append(equ1)
    rivet.update(dict1)    
    globals.update(dict1)

def es__(fstr1: str, fstr2: List[str]):
    """evaluate and format a rivet-string of equations

    """

    if fstr1[0] == 2: return
    calc = _utf.Eexec_u(fstr2.split("\n"), rivet)
    dict1, calc1, equ1 = calc.e_utf()
    if fstr1[0] == 0: _write_utf(calc1)
    equations.append(equ1)
    rivet.update(dict1)
    globals.update(dict1)

def ts__(fstr1: str, fstr2: List[str]):
    """evaluate and format a rivet-string of tables
    
    """

    if fstr1[0] == 2: return
    calc = _utf.Texec_u(fstr2.split("\n"), rivet)
    dict1, calc1, equ1 = calc.t_utf()
    if fstr1[0] == 0: _write_utf(calc1)
    equations.append(equ1)
    rivet.update(dict1)
    globals.update(dict1)