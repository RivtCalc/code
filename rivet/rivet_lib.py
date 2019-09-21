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

import sys
import os
import __main__ as _main
from pathlib import Path

from numpy import *
import numpy.linalg as la
import pandas as pd
import sympy as sy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from IPython.display import Image, Math, Latex, HTML, display

from rivet.rivet_unit import *
import rivet.rivet_check as _chk
import rivet.rivet_utf as _utf
#import rivet.rivet_rst as _rst
#import rivet.rivet_reprt as _reprt

__version__ = "0.9.1"
__author__ = "rholland"
if sys.version_info < (3, 7):
    sys.exit("rivet requires Python version 3.7 or later")

# set up folders, files and dictionaries
rivet_dict = {}
equation_list = []
_adfile = _main._set["file"]
_adpath = _main._set["path"]
_adfull = os.path.join(_adpath,_adfile)
_adbak = os.path.join(_adpath,_adfile.split(".")[0]+".bak")
_rivetpath = os.path.dirname("rivet.rivet_lib.py"),
_projpath = os.pardir
_calcnum = _adfile[1:5]
_calcwidth = 80
ad_fold = {
"adbase": _main._set["file"].split(".")[0],
"reptpath" : os.path.join(os.pardir, "reports"),
"spath": os.path.join(_adpath, "scripts"),
"tpath": os.path.join(_adpath["adpath"], "table"),
"upath": os.path.join(_adpath["adpath"], "txt"),
"rpath": os.path.join(_adpath["reptpath"], "pdf"),
"xpath": os.path.join(_adpath["reptpath"], "temp"),
"fpath": os.path.join(_adpath["reptpath"], "figures"),
"hpath": os.path.join(_adpath["reptpath"], "html"),
}    
ad_file = {    
"ctxt":  ".".join((ad_fold["adbase"], "txt")),
"cpdf":  ".".join((ad_fold["adbase"], "pdf")),
"chtml":  ".".join((ad_fold["adbase"], "html")),
"trst":  ".".join((ad_fold["adbase"], "rst")),
"tlog":  ".".join((ad_fold["adbase"], "log"))
}
with open(_adfull, "r") as f2:
    adbak = f2.read()
with open(_adbak, "w") as f3:
    f3.write(adbak)
print("\n\npath: ", _adpath, "; ", _adfile)
print("checks: folders checked; ad-file backup written to report/temp folder", "\n\n")

# start checks and logs
#_chk1 = chk.CheckRivet(_tlog)
#_chk1.logstart()
#_chk1.logwrite("< begin model processing >", 1
# os.chdir(once.__path__[0])                  #5 check LaTeX install
# f4 = open('once.sty')
# f4.close()
# os.chdir(cfg.ppath)
# _el.logwrite("< style file found >", vbos)
# os.system('latex --version')                
# _el.logwrite("< Tex Live installation found>", vbos)
# pdfout1.gen_pdf()                           #5 generate PDF calc

def _riv_strset(line1: string) -> list:
    """ parse rivet-string settings
    
    Args:
        line1 (string): rivet-string settings (from first line)
    
    Returns:
        list: execution flag, section number, string description
    """
    #print(line1)
    exec_flg = -1
    sect_num = -1
    str_descrip = " " 
    #print(line1)
    sect_num = line1.find("]")
    if sect_num > -1:
        str_descrip = line1[sect_num + 1:].strip()
        sect_num = line1[sect_num-2:sect_num]
        sect_num = sect_num.strip("]").strip("[")
    if "[h]" in line1:
        exec_flg = 2
        str_descrip = line1[0].replace("[h]","").strip()                
    elif "[x]" in line1:
        exec_flg = 1
        str_descrip = line1[0].replace("[x]","").strip()
    else:
        exec_flg = 0
    #print(exec_flg) 
    return [exec_flg, sect_num, str_descrip]

def _write_utf(pline, pp, indent):
    """ write model text to utf-8 encoded file.
    
    Args:
        mentry (string): text 
        pp (int): pretty print flag
        indent (int): indent flag
         
    """
    sect_num = sets[1]
    descrip = sets[2]
    print('=' * _calcwidth)
    _write_utf('=' * _calcwidth, 0, 0)
    descrip1 = " " +  descrip + (_calcnum + "-" +
        sect_num).rjust(_calcwidth - len(descrip) - 2)
    print(descrip1)
    _write_utf(descrip1, 1, 0)
    print('=' * _calcwidth)
    _write_utf('=' * _calcwidth, 0, 0)
    
    f1 = open(ad_file["ctxt"], 'a')
    if pp: pline = sy.pretty(pline, use_unicode=True, num_columns=80)
    if indent: pline = " "*4 + pline
    print(pline, file = f1)
    f1.close()

    if txt[0].strip() == '|' : return
    elif txt[0].strip() == "::" : return                        
    elif txt[0].strip() == '`' : return
    elif txt[0][2:4] == ".." : return                        
    elif txt[0][0] == '|' : self._write_utf(txt[0], 1, 0) 
    elif txt[0][2] == "\\" : self._write_utf(txt[0], 1, 0)                
    else: _write_utf(txt[0], 1, 0)

def _write_code(str1, set1):
    """ format and write python string in r__() to _utf
    
    Args:
        str1 ([type]): [description]
        set1 ([type]): [description]
    """
    pass

def _write_rst(pline, pp, indent):
    
    pdf_files = {    
        "ttex1":  ".".join((ad_fold["adbase"], "tex")),
        "auxfile": ".".join((ad_fold["adbase"], ".aux")),
        "outfile":  ".".join((ad_fold["adbase"], ".out")),
        "texmak2":  ".".join((ad_fold["adbase"], ".fls")),
        "texmak3":  ".".join((ad_fold["adbase"], ".fdb_latexmk"))
    }

def _write_py(self):
    """ write executable python code to file
 
        Write imports, values, equations and function to Python file. This file
        contains the executable ad-file without the explanatory text or
        formatting.
        
    """
    str1 =  ('"""\nThis file contains Python equations from the '
            'on-c-e model \n\n  '+ self.mfile + '\n'
            '\nFor interactive analysis open the file\n'
            'in an IDE executable shell e.g. Pyzo,\n'
            'Spyder, Jupyter Notebook or Komodo IDE \n'
            '""" \n')
        
    str2 =  ('import os\n'
            'import sys\n'
            'from sympy import *\n'
            'from numpy import *\n'
            'import numpy.linalg as LA\n'
            'import importlib.util\n'
            'import once.config as cfg\n')
                            
    str2a = ('pypath = os.path.dirname(sys.executable)\n'
            'oncedir = os.path.join(pypath,"Lib","site-packages","once")\n'
            'cfg.opath = oncedir\n'
            'from once.calunit import *\n')

    str5 = ('\ndef vlist(vlistx = vlist1, vlisty= vlist2):\n'
            '   """Utility function for interactively listing once\n'
            '      variable values. Variables are stored in vlist1 and'
            '      definitions in vlist2. Type vlist()\n'
            '      to list updated variable summary after executing\n'
            '      calc Python script\n'
            '   """\n\n'
            '   for lsti in zip(vlistx, vlisty):\n'
            '       item1 = eval(str(lsti[0]))\n'
            '       def1 = lsti[1]\n'
            '       cncat1 = str(lsti[0]) + " = " + str(item1) + " "*30\n'
            '       print(cncat1[:25] + "# " + def1)\n\n'
            'if __name__ == "__main__":\n'
            '       vlist()'
            '       \n\n')

    _adfile.write('#\n# variables\nvlist1 = ' + str4 + '\n')
    
def r__(fstr: string):
    """ evaluate and format a rivet-string of python code
    
    Args:
        fstr (string): [description]
    """
    fstr1 = fstr.split("\n", 1)
    fstr2 = fstr1[1].splitlines()
    str_set = _riv_strset(fstr1[0])
    if str_set[0] == 2:
        return
    for i in fstr2:
        exec(i.strip())
    if str_set[0] == 0:
        _write_code(fstr2, str_set)

    equation_list.update()
    rivet_dict.update(locals())

def i__(fstr: string):
    """ evaluate and format a rivet-string of text and images
    
    """
    fstr1 = fstr.split("\n", 1)
    fstr2 = fstr1[1].splitlines()
    str_set = _riv_strset(fstr1[0])
    if str_set[0] == 2:
        return
    icalc = _utf.Iexec_u(fstr2, rivet_dict)
    idict1, icalc1 = icalc.vutf()
    rivet_dict.update(idict1)
    if str_set[0] == 0:
        _write_utf(icalc1, str_set)    

def v__(fstr: string):
    """evaluate and format a rivet-string of values

    """
    fstr1 = fstr.split("\n", 1)
    fstr2 = fstr1[1].splitlines()
    str_set = _riv_strset(fstr1[0])
    if str_set[0] == 2:
        return
    vcalc = _utf.Vexec_u(fstr2, rivet_dict)
    vdict1, vcalc1 = vcalc.vutf()
    rivet_dict.update(vdict1)
    if str_set[0] == 0:
        _write_utf(vcalc1, str_set)            

def e__(fstr: string):
    """evaluate and format a rivet-string of equations

    """
    fstr1 = fstr.split("\n", 1)
    fstr2 = fstr1[1].splitlines()
    str_set = _riv_strset(fstr1[0])
    if str_set[0] == 2:
        return
    ecalc = _utf.Eexec_u(fstr2, rivet_dict)
    edict1, ecalc1 = ecalc.eutf()
    rivet_dict.update(edict1)
    if str_set[0] == 0:
        _write_utf(ecalc1, str_set)   

def t__(fstr: string):
    """evaluate and format a rivet-string of tables
    
    """
    fstr1 = fstr.split("\n", 1)
    fstr2 = fstr1[1].splitlines()
    str_set = _riv_strset(fstr1[0])
    if str_set[0] == 2:
        return
    tcalc = _utf.Texec_u(fstr2, rivet_dict)
    tdict1, tcalc1 = tcalc.tutf()
    rivet_dict.update(tdict1)
    if str_set[0] == 0:
        _write_utf(tcalc1, str_set)   

