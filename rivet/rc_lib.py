#! python
"""Exposes rivet functions.

    This module exposes five string functions that take **rivet** markup as
    arguments. The first line of each string is a descriptor. The remaining
    lines include arbitrary unicode text or Python code along with the following
    commands and tags.
    
    Unicode text may include reStructuredText markup.  See here for details:
    (https://docutils.sourceforge.io/docs/user/rst/quickref.html).

    Functions and inputs (see rivet_calc.py for doc strings)
    -----------------------------------------------------------------
    #%%                 : designates start of an interactive cell
    r__('''r-string''') : repository and calc data 
        link tag
        || summary |         : summary paragraph and table of contents
        || toc |             : table of contents
        || labels |          : labels for search
        || attach |          : attach pdf files
    i__('''i-string''') : insert text and images
        Unicode text and tags
        || tex |             : LaTeX equation
        || sym |             : sympy equation
        || table |           : insert table from file or inline
        || image |           : insert image from file
        || image2 |          : insert side by side images from files
    v__('''v-string''') : define values
        Unicode text (except equal sign) and tags
         =                  : assign value        
        || values           : values from file
        || vectors          : vectors from file
    e__('''e-string''') : define equations
        Unicode text (except equal sign) and tags
         =                  : define equation or function
        || format |         : format settings
        || func |           : import function from file   
    t__('''t-string''') : define tables and plots
        Single line Python statements (no blocks)
        || table            : insert table from csv file
        || image            : insert image from file
        || image2           : insert side by side images from files

        Tags
        --------------------------------------------
        abc def [s]_         : designates section and title
        [abc123]_            : citation        
        abc def [cite]_      : citation description    
        [#]_                 : autonumbered footnote
        abc def [foot]_      : footnote description
        abc def [r]_         : right justify line
        abc def [c]_         : center line
        abc def [t]_         : right justify title with table number   
        abc def [e]_         : right justify lable with equation number
        abc def [f]_         : caption with figure number   
        [page]_              : new doc page
        [line]_              : draw horizontal line
        http://abc [link]_   : link

    
    Output functions
    -----------------------------------------------------------------
    write_values()     : write values to python file for import
    write_calc()       : write calc to utf8 text file
    write_pdf()        : write doc to pdf file
    write_html()       : write doc to html file
    write_report()     : write docs to pdf report file
"""
import __main__
import os
import sys
import textwrap
import logging
import numpy
import warnings
from pathlib import Path
from collections import deque
from typing import List, Set, Dict, Tuple, Optional
from tabulate import tabulate
from rivet.rivet_unit import *
import rivet.rivet_calc as _rivcalc
#import rivet.rivet_doc as _rdoc
#import rivet.rivet_reprt as _reprt
#import rivet.rivet_chk as _rchk

__version__ = "0.9.5"
__author__ = "rholland@structurelabs.com"
if sys.version_info < (3, 7):
    sys.exit("rivet requires Python version 3.7 or later")

#start-up variables
_rivetD: dict ={}                                    # runtime vars dictionary
_utfcalcS = """"""                                   # utf print string
_exportS  = """"""                                   # values export string
_cfull    = Path(__main__.__file__)                  # calc file path
_cfile    = Path(__main__.__file__).name             # calc file name
_cname    = _cfile.split(".py")[0]                   # calc file basename
_rivpath  = Path("rivet.rivet_lib.py").parent        # rivet program path
_cpath    =  Path(_cfull).parent                     # calc folder path
_ppath    = Path(_cfull).parent.parent               # project folder path
_dpath    = Path(_ppath / "docs")                    # doc folder path
_rppath   = Path(_ppath / "reports")                 # report folder path
_utffile  = Path(_cpath / ".".join((_cname, "txt"))) # utf calc output
_expfile  = Path(_cpath / "scripts" / "".join(("v", _cfile))) # export file
# folder dictionary
_foldD: dict = {
"efile": _expfile,   
"ppath": _ppath,
"dpath": _dpath,
"rpath": _rppath,
"cpath": Path(_cfull).parent,
"spath": Path(_cpath, "scripts"),
"kpath": Path(_cpath, "sketches"),
"tpath": Path(_cpath, "data"),
"xpath": Path(_cpath, "text"),
"mpath": Path(_cpath, "tmp"),
"hpath": Path(_dpath, "html"),
"fpath": Path(_dpath, "html/figures"),
"apath": Path(_rppath, "attach"),
}
# temp folder files
_rbak = Path(_foldD["mpath"] / ".".join((_cname, "bak")))
_logfile = Path(_foldD["mpath"] / ".".join((_cname, "log")))
_rstfile = Path(_foldD["mpath"] / ".".join((_cname, "rst"))) 
# section settings
_setsectD: dict = {"rnum": _cname[0:4],"dnum": _cname[0:2],"cnum": _cname[2:4],
"snum": "", "sname": "", "swidth": 80,
"enum":  0, "fnum": 0, "tnum" : 0,
"ftnum": 0,"ftqueL": deque([1]), "cite": " ", "ctqueL": deque([1])
                    }
# command settings
_setcmdD = {"cwidth": 50, "scale1": 1., "scale2": 1., 
            "prec": 2, "trim": 2, "replace": False, "code": False}

with open(_rfull, "r") as f2: calcbak = f2.read() 
with open(_rbak, "w") as f3: f3.write(calcbak)  # write backup

#logs and checks
warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=_logfile,
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
_rshortP = Path(*Path(_rfull).parts[-3:])
_bshortP = Path(*Path(_rbak).parts[-4:])
logging.info(f"""file: {_rshortP}""" )
logging.info(f"""backup: {_bshortP}""")
print("logfile:", _logfile)

# todo: check folder structure here

def _update(hdrS:str):
    """format section heading and update settings

    Args:
        hdrS (str): section heading line
    """
    global _utfcalcS, _setsectD

    _setsectD["enum"] = 0 
    _setsectD["fnum"] = 0
    _setsectD["tnum"] = 0
    nameS = _setsectD["sname"] = hdrS[hdrS.find("]_") + 2:].strip()
    snumS = _setsectD["snum"] = hdrS[hdrS.find("[")+1:hdrS.find("]_")]
    rnumS = str(_setsectD["rnum"])
    widthI = int(_setsectD["swidth"])
    headS = " " +  nameS + (rnumS + " - " +
            ("[" + snumS + "]")).rjust(widthI - len(nameS) - 2)
    bordrS = widthI * "="
    utfS = bordrS + "\n" + headS + "\n" + bordrS +"\n"
    print(utfS); _utfcalcS += utfS

def list_values():
    """write table of values to terminal 
    """
    rivetL = [[k,v] for k,v in _rivetD.items()]
    rivetT = []
    for i in rivetL:
        if isinstance(i[1], numpy.ndarray):
            if numpy.size(i[1]) > 3:
                i[1] = numpy.hstack([i[1][:4],["..."]])
            rivetT.append(i)

    print("." * _setsectD["swidth"])
    print("Values List")
    print("." * _setsectD["swidth"])                
    print(tabulate(rivetT, tablefmt="grid", headers=["variable", "value"]))
    print("." * _setsectD["swidth"] + "\n")

def write_values():
    """ write value assignments to Python file
 
        Use file for exchanging values between calcs. 
        File name is the calc file name prepended with 'v'
        written to the scripts folder.      
    """
    
    str1 =  ("""header string""")
    str1 = str1 + _exportS
    with open(_expfile, 'w') as expF:
        expF.write(str1)

def utfcalc(utfcalc, _txtfile):
    """write utf calc string to file
    """
    with open(_txtfile, "wb") as f1:
        f1.write(_utfcalcS.encode("UTF-8"))

def _rstcalc(_rstcalcS, _rstfile):
    """write reST calc string to file
    
    Args:
        pline ([type]): [description]
        pp ([type]): [description]
        indent ([type]): [description]
    """
    pdf_files = {
        "cpdf":  ".".join((_rbase, "pdf")),
        "chtml":  ".".join((_rbase, "html")),
        "trst":  ".".join((_rbase, "rst")),    
        "ttex1":  ".".join((_rbase, "tex")),
        "auxfile": ".".join((_rbase, ".aux")),
        "outfile":  ".".join((_rbase, ".out")),
        "texmak2":  ".".join((_rbase, ".fls")),
        "texmak3":  ".".join((_rbase, ".fdb_latexmk"))
    }
    with open(_rstfile, "wb") as f1:
        f1.write(_rstcalcS.encode("UTF-8"))

def htmldoc():
    """[summary]
    """
    with open(_txtfile, "wb") as f1:
        f1.write(utfcalc.encode("UTF-8"))

def pdfdoc():
    with open(_txtfile, "wb") as f1:
        f1.write(utfcalc.encode("UTF-8"))

def pdfreport():
    """[summary]
    """
    pass

def R(rawS: str):
    """transform repository-string to utf and reST calc
    
    Args:
        rawstrS (str): repository-string
    """
    global  _utfcalcS, _setsectD, _rivetD
    
    sectS,strS = rawS.split("\n",1)
    if "]_" in sectS: _update(sectS)
    
    strL = strS.split("\n")
    rcalc = _rivcalc._Rutf(strL, _foldD, _setsectD) 
    rcalcS, _setsectD = rcalc.r_parse()
    _utfcalcS = _utfcalcS + rcalcS

def I(rawS: str):
    """transform insert-string to utf and reST calc
    
    Args:
        rawstrS (str): insert-string
    """
    global _utfcalcS, _setsectD, _foldD, _setcmdD

    sectS,strS = rawS.split("\n",1)
    if "]_" in sectS: _update(sectS)

    strL = strS.split("\n")
    icalc = _rivcalc._Iutf(strL, _foldD, _setcmdD, _setsectD) 
    icalcS, _setsectD, _setcmdD = icalc.i_parse()
    _utfcalcS = _utfcalcS + icalcS

def V(rawS: str):
    """transform insert-string to utf and reST calc
    
    Args:
        rawstr (str): value-string
    """
    global _utfcalcS, _setsectD, _foldD, _rivetD, _setcmdD, _exportS

    sectS,strS = rawS.split("\n",1)
    if "]_" in sectS: _update(sectS)
    
    strL = strS.split("\n")
    vcalc = _rivcalc._Vutf(strL, _foldD, _setcmdD, _setsectD, _rivetD, _exportS)
    vcalcS, _setsectD, _rivetD, _exportS = vcalc.v_parse()
    _utfcalcS = _utfcalcS + vcalcS

def E(rawS: str):
    """convert equation-string to utf or rst-string

    """
    global _utfcalcS, _setsectD, _foldD, _rivetD, _setcmdD, _exportS

    sectS,strS = rawS.split("\n",1)
    if "]_" in sectS: _update(sectS)
    
    strL = strS.split("\n")
    ecalc = _rivcalc._Eutf(strL, _foldD, _setcmdD, _setsectD, _rivetD, _exportS)
    ecalcS, _setsectD, _rivetD, _exportS = ecalc.e_parse()
    _utfcalcS = _utfcalcS + ecalcS

def T(rawS: str):
    """convert table-string to utf or rst-string
    
    """
    global _utfcalcS, _setsectD, _foldD, _setcmdD, _exportS

    sectS,strS = rawS.split("\n",1)
    if "]_" in sectS: _update(sectS)
    
    strL = strS.split("\n")
    tcalc = _rivcalc._Tutf(strL, _foldD, _setcmdD, _setsectD, _rivetD, _exportS)
    tcalcS, _setsectD, _exportS = tcalc.t_parse()
    _utfcalcS = _utfcalcS + tcalcS

def X(rawS: str):
    """skip execution of rivet-string
    """
    pass
