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

def ad_paths(_settings):
    _path_dict = {
    "adpath" : _settings["path"],
    "adfile" : _ad_set["file"],
    "rivetpath" : os.path.dirname("rivet.rivet_lib.py"),
    "projpath" : os.chdir(os.pardir),
    "reptpath" : os.path.join(_projpath, "reports"),
    }
    ad_folders = {
    "spath" :  os.path.join(ad_paths["adpath"], "scripts"),
    "tpath" :  os.path.join(ad_paths["adpath"], "table"),
    "upath" :  os.path.join(ad_paths["adpath"], "txt"),
    "rpath" :  os.path.join(ad_paths["reptpath"], "pdf"),
    "xpath" :  os.path.join(ad_paths["reptpath"], "temp"),
    "fpath" :  os.path.join(ad_paths["reptpath"], "figures"),
    "hpath" :  os.path.join(ad_paths["reptpath"], "html"),
    "adbase" : ad_set["adfile"].split(".")[0]
    }    
    ad_files = {    
    "ctxt" :  ".".join(["adbase"], "txt"),
    "cpdf" :  ".".join(["adbase"], "pdf"),
    "chtml" :  ".".join(["adbase"], "html"),
    "trst" :  ".".join(["adbase"], "rst"),
    "tlog" :  ".".join(["adbase"], "log"),
    "ttex1" :  ".".join(["adbase"], "tex"),
    "auxfile" : ".".join(["adbase"], ".aux"),
    "outfile" :  ".".path.join(["adbase"], ".out"),
    "texmak2" :  ".".path.join(["adbase"], ".fls"),
    "texmak3" :  ".".path.join(["adbase"], ".fdb_latexmk")
    }

return _path_dict, _settings

def ad_flags():
    _cleantemp =  (ad_files["auxfile"],
                        outfile,   
                        texmak2, 
                        texmak3
                        )
    _pdfflag = 0
    _nocleanflag = 0
    _verboseflag = 0
    _defaultdec = "3,3"
    _calcwidth = 80
    _calctitle = "\n\nModel Title"  # default model title
    _pdfmargin = "1.0in,0.75in,0.9in,1.0in"
    _calcnum = _designbase[1:5]
    _bakfile = _adfile.split(".")[0] + ".bak"

_adfile = _path_dict["adfile"]
with open(_adfile, "r") as f2:
    _adbak = f2.read()
with open(_bakfile, "w") as f3:
    f3.write(_adbak)
print("\n\nad file : ", _adfile)
print("checks : folders checked; ad file backup written", "\n\n")


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

def _prt_sect(settings):
    """Print sections to UTF-8.
    
    """
    sect_num = settings[1]
    descrip = settings[2]
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
    f1 = open(_ctxt, 'a')
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

