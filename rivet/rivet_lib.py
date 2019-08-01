#! python
"""rivet_lib
    The module processes the r-i-v-e-t language and sets files and paths

    The language includes five types of f-strings where each type of string is
    evaluated by a function. The first line of each f-string can be a settings
    string.

    r__() : string of python code 
    i__() : string that inserts text and images
    v__() : string that defines values
    e__() : string that defines equations
    t__() : string that defines tabls and plots
    
"""

import os
import sys
import sympy as sy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from IPython.display import Image, Math, Latex, HTML, display
from numpy import *
from pandas import *

import rivet.rivet_cfg as cfg
import rivet.rivet_check as chk
import rivet.rivet_utf as _utf

# import rivet.rivet_report as reprt
# from rivet.rivet_units import *
# from rivet.rivet_config import *
# from rivet.rivet_html import *
# from rivet.rivet_pdf import *

__version__ = "0.9.1"
__author__ = "rholland"

if sys.version_info < (3, 7):
    sys.exit("rivet requires Python version 3.7 or later")

var_rivet_dict = {}     # global calc variable dictionary

def setfiles(_designfile):
    """set paths and files
    
    Arguments:
        _designfile {[type]} -- [description]
    """
    cfg.designfile = _designfile
    
    try:
        cfg.rivetpath = os.path.dirname("rivet.rivetcfg.lib")
        cfg.designpath = os.path.dirname(cfg.designfile)
        cfg.designname = os.path.basename(cfg.designfile)
        cfg.projpath = os.path.dirname(cfg.designpath)
        cfg.calcpath = os.path.join(cfg.projpath, "calcs")
        cfg.bakfile = cfg.designfile.split(".")[0] + ".bak"
        with open(cfg.designfile, "r") as f2:
            cfg.designbak = f2.read()
        with open(cfg.bakfile, "w") as f3:
            f3.write(cfg.designbak)
        print("< folders checked and design file backup written >")
    except:
        sys.exit("folders and files not found - program stopped")

    # design paths
    cfg.fpath = os.path.join(cfg.designpath, "figures")
    cfg.spath = os.path.join(cfg.designpath, "scripts")
    cfg.tpath = os.path.join(cfg.designpath, "table")
    # calc paths
    cfg.rpath = os.path.join(cfg.calcpath, "pdf")
    cfg.upath = os.path.join(cfg.calcpath, "txt")
    cfg.xpath = os.path.join(cfg.calcpath, "temp")

    # calc file names
    cfg.designbase = cfg.designname.split(".")[0]
    cfg.ctxt = ".".join([cfg.designbase, "txt"])
    cfg.chtml = ".".join([cfg.designbase, "html"])
    cfg.cpdf = ".".join([cfg.designbase, "pdf"])
    cfg.trst = ".".join([cfg.designbase, "rst"])
    cfg.tlog = ".".join([cfg.designbase, "log"])

    # laTex file names
    cfg.ttex1 = ".".join([cfg.designbase, "tex"])
    cfg.auxfile = os.path.join(cfg.designbase, ".aux")
    cfg.outfile = os.path.join(cfg.designbase, ".out")
    cfg.texmak2 = os.path.join(cfg.designbase, ".fls")
    cfg.texmak3 = os.path.join(cfg.designbase, ".fdbcfg.latexmk")
    cfg.cleantemp = (cfg.auxfile, cfg.outfile, cfg.texmak2, cfg.texmak3)

    # flags and variables
    cfg.pdfflag = 0
    cfg.nocleanflag = 0
    cfg.verboseflag = 0
    cfg.defaultdec = "3,3"
    cfg.calcwidth = 80
    cfg.calctitle = "\n\nModel Title"  # default model title
    cfg.pdfmargin = "1.0in,0.75in,0.9in,1.0in"

# check config file and folder structure and start log
#_chk1 = chk.CheckRivet(cfg.tlog)
#_chk1.logstart()
#_chk1.logwrite("< begin model processing >", 1
# )

def r__(fstr):
    """run python code

    """
    settings = string_sets(fstr)
    fstr1 = _fstr.split("\n", 1)
    fstr2 = fstr1[1].splitlines()
    for i in fstr2:
        exec(i.strip())
    return var_rivet_dict.update(locals())


def i__(fstr):
    """process insert string (text and figures)
    
    """
    settings = string_sets(fstr)

    print(fstr)


def v__(fstr):
    """process value string

    """
    settings = string_sets(fstr)
    vlist = _fstr.split("\n")
    vfunc = _utf.ExecV(vlist)
    callv1 = vlist[0].split('|')
    if vfunc.process == "s":
        return
    for i in vlist:
        if "=" in i:
            exec(i.strip())
    globals().update(locals())
    vfunc.vprint()
    return var_rivet_dict.update(locals())


def e__(fstr):
    """process equation string
    
    """
    settings = string_sets(fstr)
    for j in fstr.split("\n"):
        if len(j.strip()) > 0:
            if "=" in j:
                k = j.split("=")[1]
                nstr3 = str(j) + " = " + str(eval(k))
                print(nstr3)
                exec(j.strip(), globals())
            else:
                print(j)
    return var_rivet_dict.update(locals())


def t__(fstr):
    """process table string
    
    """
    settings = string_sets(fstr)
    return var_rivet_dict.update(locals())


def string_sets(first_line):
    """evaluate string settings
    
    """

    new_str = first_line
    section_flg = 0
    str_descrip = " " 
    prt_state = 0  
    str_source = "" 
    source_flg = 0

    splt_string = first_line.split('|')
    if len(splt_string) > 1:
        try:
            for i in splt_string:        
                start = i[0].find("[s]") 
                if start > -1:
                    section_flg = 1
                    str_descrip = i[0][start+3:].strip()
                else:
                    str_descrip = i[0].strip()

                chk_flg = i[1].strip()
                if chk_flg == "[p]":
                    prt_state = 0
                elif chk_flg == "[h]":
                    prt_state = 1
                elif chk_flg == "[x]":
                    prt_state = 2
        
                start = i[2].find("[i]") 
                if start > -1:
                    source_flg = 1
                    str_source = i[0][start+3:].strip()
                else:
                    str_source = i[2].strip()
        except:
            pass

    return [new_str, section_flg, str_descrip, prt_state, 
                str_source, source_flg]

