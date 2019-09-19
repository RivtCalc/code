#! python
"""rivet_lib
    Processes the r-i-v-e-t design file to a calc and sets files and paths

    The language includes five types of f-strings where each type of string is
    evaluated by a function. The first line of each f-string can be a settings
    string.

    r__() : string of python code 
    i__() : string inserts text and images
    v__() : string defines calculation values
    e__() : string defines calculation equations
    t__() : string inserts tables and plots
    
"""

import sys
import os
import inspect
import __main__ as main
from pathlib import Path

from numpy import *
import pandas as pd
import sympy as sy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from IPython.display import Image, Math, Latex, HTML, display

import rivet.rivet_check as _chk
import rivet.rivet_utf as _utf
#import rivet.rivet_pdf as _pdf
#import rivet.rivet_rst as _rst
#import rivet.rivet_units as _units

# import rivet.rivet_report as reprt
# from rivet.rivet_units import *
# from rivet.rivet_config import *
# from rivet.rivet_html import *
# from rivet.rivet_pdf import *


__version__ = "0.9.1"
__author__ = "rholland"
if sys.version_info < (3, 7):
    sys.exit("rivet requires Python version 3.7 or later")

# set up folders, files and dictionaries
global_rivet_dict = {}

ad_init = {
"adpath" : main._set["path"],
"adfile" : main._set["file"],
"rivetpath" : os.path.dirname("rivet.rivet_lib.py"),
"projpath" : os.pardir,
"reptpath" : os.path.join(os.pardir, "reports")
}
ad_fold = {
"adbase": ad_init["adfile"].split(".")[0],
"spath": os.path.join(ad_init["adpath"], "scripts"),
"tpath": os.path.join(ad_init["adpath"], "table"),
"upath": os.path.join(ad_init["adpath"], "txt"),
"rpath": os.path.join(ad_init["reptpath"], "pdf"),
"xpath": os.path.join(ad_init["reptpath"], "temp"),
"fpath": os.path.join(ad_init["reptpath"], "figures"),
"hpath": os.path.join(ad_init["reptpath"], "html"),
}    
ad_file = {    
"ctxt":  ".".join((ad_fold["adbase"], "txt")),
"cpdf":  ".".join((ad_fold["adbase"], "pdf")),
"chtml":  ".".join((ad_fold["adbase"], "html")),
"trst":  ".".join((ad_fold["adbase"], "rst")),
"tlog":  ".".join((ad_fold["adbase"], "log")),
"ttex1":  ".".join((ad_fold["adbase"], "tex")),
"auxfile": ".".join((ad_fold["adbase"], ".aux")),
"outfile":  ".".join((ad_fold["adbase"], ".out")),
"texmak2":  ".".join((ad_fold["adbase"], ".fls")),
"texmak3":  ".".join((ad_fold["adbase"], ".fdb_latexmk")),
"bakfile": ".".join((ad_fold["adbase"], ".bak"))
}

ad_par = {
    "clean":  (ad_file["auxfile"],
             ad_file["outfile"]),
    "pdf": (0,"margins"), 
    "title" : "Model Title"    
}

_adfile = ad_init["adfile"]
_adpath = ad_init["adpath"]
_adfull = os.path.join(_adpath,_adfile)
_adbak = os.path.join(_adpath,ad_file["bakfile"])
_calcnum = _adfile[1:5]
_calcwidth = 80
with open(_adfull, "r") as f2:
    adbak = f2.read()
with open(_adbak, "w") as f3:
    f3.write(adbak)
print("\n\npath: ", _adpath, ";", _adfile)
print("checks: folders checked ; ad file backup written", "\n\n")
# start checks and logs
#_chk1 = chk.CheckRivet(_tlog)
#_chk1.logstart()
#_chk1.logwrite("< begin model processing >", 1

def _string_settings(first_line):
    """prarse design string settings line

    Method called for each design string. 
    
    """
    exec_flg = -1
    sect_num = -1
    section_flg = -1
    source_flg = -1
    design_descrip = " " 
    par1 = first_line
    #print(par1)
    section_flg = par1.find("]")
    if section_flg > -1:
        design_descrip = par1[section_flg + 1:].strip()
        sect_num = par1[section_flg-2:section_flg]
        sect_num = sect_num.strip("]").strip("[")
    if "[h]" in par1:
        exec_flg = 2
        design_descrip = i[0].replace("[h]","").strip()                
    elif "[x]" in par1:
        exec_flg = 1
        design_descrip = i[0].replace("[x]","").strip()
    else:
        exec_flg = 0

    #print(exec_flg) 
    return [exec_flg, sect_num, design_descrip]

def _prt_sect(sets):
    """Print sections to UTF-8.
    
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

def _write_utf(pline, pp, indent):
    
    """ Write model text to utf-8 encoded file.
    
    Args:
        mentry (string): text 
        pp (int): pretty print flag
        indent (int): indent flag
        
    """
    f1 = open(ad_file["ctxt"], 'a')
    if pp: pline = sy.pretty(pline, use_unicode=True, num_columns=80)
    if indent: pline = " "*4 + pline
    print(pline, file = f1)
    f1.close()

def r__(fstr):
    """run python code

    """
    fstr1 = fstr.split("\n", 1)
    fstr2 = fstr1[1].splitlines()
    str_set = _string_settings(fstr1[0])
    if str_set[0] == 2:
        return
    if str_set[0] == 0:
        if int(str_set[1]) > -1:
            _prt_sect(str_set)
        for i in fstr2:
            exec(i.strip())

    global_rivet_dict.update(locals())

def i__(fstr):
    """evaluate insert string
    
    """
    global eqnum
    fstr1 = fstr.split("\n", 1)
    fstr2 = fstr1[1].splitlines()
    str_set = _string_settings(fstr1[0])
    if str_set[0] == 2:
        return
    if str_set[0] == 0:
        if int(str_set[1]) > -1:
            _prt_sect(str_set)
        for i in fstr2:
            print(i.strip())

    global_rivet_dict.update(locals())

def v__(fstr):
    """evaluate value string

    """
    global eqnum, sectnum
    fstr1 = fstr.split("\n", 1)
    fstr2 = fstr1[1].splitlines()
    str_set = _string_settings(fstr1[0])
    
    if str_set[0] == 2:
        return
    if str_set[0] == 1:
        vcalc = _utf.ExecV(fstr2, global_rivet_dict)
        vdict1, vcalc1 = vcalc.vutf()
        global_rivet_dict.update(vdict1)
        return
    if str_set[0] == 0:
        vcalc = _utf.ExecV(fstr2, global_rivet_dict)
        vdict1, vcalc1 = vcalc.vutf()
        global_rivet_dict.update(vdict1)
        if int(str_set[1]) > -1:
            _prt_sect(str_set)            
        for i in vcalc1:
            if "=" in i:
                print(" "*4 + i)
            else:
                print(i)

def e__(fstr):
    """evaluate equation string

    """
    global eqnum, sectnum
    fstr1 = fstr.split("\n", 1)
    fstr2 = fstr1[1].splitlines()
    str_set = _string_settings(fstr1[0])
    #print('equation', str_set)
    
    if str_set[0] == 2:
        return
    if str_set[0] == 1:
        ecalc = _utf.ExecE(fstr2, global_rivet_dict)
        edict1, ecalc1 = ecalc.eutf()
        global_rivet_dict.update(edict1)
        return
    if str_set[0] == 0:
        ecalc = _utf.ExecE(fstr2, global_rivet_dict)
        edict1, ecalc1 = ecalc.eutf()
        global_rivet_dict.update(edict1)
        if int(str_set[1]) > -1:
            _prt_sect(str_set)
        for i in ecalc1:
            if "=" in i:
                print(" "*4 + i)
            else:
                print(i)

def t__(fstr):
    """evaluate table string
    
    """

    global eqnum, sectnum
    settings = _string_settings(fstr[0])

    global_rivet_dict.update(locals())

