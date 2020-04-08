#! python
"""Exposes rivet-string and output functions.

    **rivet** markup is used within five string functions exposed in this
    module. The first line of each string is a descriptor. Markup includes a
    set of commands (lines begin with ||), key symbols (=) and tags (bracketed
    with []_). They may also include unicode (UTF-8) and reStructuredText
    (https://docutils.sourceforge.io/docs/user/rst/quickref.html).

    String functions and commands (see rivet_calc.py for doc strings)
    -----------------------------------------------------------------
    r__('''r-string''') : repository and calc data 
        || summary          : summary paragraph and table of contents
        || labels           : labels for search
        || append           : append pdf files
    i__('''i-string''') : insert text and images
        || tex              : LaTeX equation
        || sym              : sympy equation
        || table            : insert table from file or inline
        || image            : insert image from file
        || image2           : insert side by side images from files
    v__('''v-string''') : define values
         =                  : assign value        
        || values           : values from file
        || vectors          : vectors from file
    e__('''e-string''') : define equations
         =                  : define equation or function
        || format           : format parameters
        || funct            : function from file   
    t__('''t-string''') : define tables and plots
        || data             : define new table
        || read             : read table data from csv file
        || save             : write data or plot image to file
        || table            : insert table from csv file
        || plot             : define new plot for table
        || add              : add data to plot from table
        || image            : insert image from file
        || image2           : insert side by side images from files

        Tags (* not included in r__)
        ----------------------------
        [abc123]_       : citation *        
        [#]_            : footnote *
        [cite]_         : citation description *    
        [foot]_         : footnote description *
        [link]_         : http link
        [page]_         : new doc page *
        [line]_         : draw horizontal line *
        [r]_            : right justify line
        [c]_            : center line
        [t]_            : right justify line with table number *   
        [e]_            : right justify line with equation number *   

    Output functions
    ----------------
    list_values()      : write value assignments stdout table
    write_values()     : write value assignments to python file
    write_calc()       : write calc to utf8 text file
    write_pdf()        : write calc to pdf file
    write_html()       : write calc to html file
    write_report()     : write calcs to pdf report file
"""
import __main__
import os
import sys
import textwrap
import logging
import numpy
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
_rivetD: dict ={}                                   # runtime vars dictionary
_utfcalcS = """"""                                  # utf print string
_exportS = """"""                                   # values export string
_rfull = Path(__main__.__file__)                    # calc file path
_rfile = Path(__main__.__file__).name               # calc file name
_rname = _rfile.split(".py")[0]                     # calc file basename
_rivpath = Path("rivet.rivet_lib.py").parent        # rivet program path
_cpath =  Path(_rfull).parent                       # calc folder path
_ppath = Path(_rfull).parent.parent                 # project folder path
_dpath = Path(_ppath / "docs")                      # doc folder path
_rppath = Path(_ppath / "reports")                  # report folder path
_utffile = Path(_cpath / ".".join((_rname, "txt"))) # utf calc output
_expfile = Path(_cpath / "scripts" / "".join(("v", _rfile))) # export file
# folder dictionary
_foldD: dict = {
"efile": _expfile,   
"ppath": _ppath,
"cpath": Path(_rfull).parent,
"dpath": _dpath,
"rpath": _rppath,
"spath": Path(_cpath, "scripts"),
"kpath": Path(_cpath, "sketches"),
"tpath": Path(_cpath, "tables"),
"xpath": Path(_cpath, "text"),
"hpath": Path(_dpath, "html"),
"fpath": Path(_dpath, "html/figures"),
"apath": Path(_rppath, "append"),
"mpath": Path(_rppath, "temp")
}
# temp folder files
_rbak = Path(_foldD["mpath"] / ".".join((_rname, "bak")))
_logfile = Path(_foldD["mpath"] / ".".join((_rname, "log")))
_rstfile = Path(_foldD["mpath"] / ".".join((_rname, "rst"))) 
# section settings
_setsectD: dict = {"rnum": _rname[0:4],"dnum": _rname[0:2],"cnum": _rname[2:4],
"snum": "", "sname": "", "swidth": 80,
"enum":  0, "fnum": 0, "tnum" : 0,
"ftnum": 0,"ftqueL": deque([1]), "cite": " ", "ctqueL": deque([1])
}
# command settings
_setcmdD = {"cwidth": 50, "scale1": 1., "scale2": 1., 
            "prec": 2, "trim": 2, "replace": False, "code": False}
#logs and checks
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=_logfile,
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
with open(_rfull, "r") as f2: calcbak = f2.read()
with open(_rbak, "w") as f3: f3.write(calcbak)  # write backup
_rshortP = Path(*Path(_rfull).parts[-3:])
_bshortP = Path(*Path(_rbak).parts[-4:])
logging.info(f"""rivet file : {_rshortP}""" )
logging.info(f"""backup file written : {_bshortP}""")
# todo: check folder structure here

def _update(hdrS:str):
    """update section setting dictionary
    
    Args:
        hdrs {str}: rivet-string header
    """
    global _utfcalcS, _setsectD

    _setsectD["enum"] = 0 
    _setsectD["fnum"] = 0
    _setsectD["tnum"] = 0
    swidthI = int(_setsectD["swidth"])
    rnumS = str(_setsectD["rnum"])
    snameS = _setsectD["sname"] = hdrS[hdrS.find("]_") + 2:].strip()
    snum = _setsectD["snum"] = hdrS[hdrS.find("[")+1:hdrS.find("]_")]
    sheadS = " " +  snameS + (rnumS + " - " +
            ("[" + str(snum) + "]")).rjust(swidthI - len(snameS) - 2)
    sstrS = swidthI * "="
    utfS = sstrS + "\n" + sheadS + "\n" + sstrS +"\n"
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
 
        The file may be used for exchanging output between files. 
        The file name is the calc file name prepended with 'v'
        written to the scripts folder.      
    """
    
    str1 =  ("""\nThis file contains values
            from the rivet design file 
            for lsti in zip(vlistx, vlisty)
            if __name__ == "__main__":\n
            vlist()\n\n""")
    str1 = str1 + _exportS
    with open(_expfile, 'w') as expF:
        expF.write(str1)

def utfcalc(utfcalc, _txtfile):
    """write utf calc string to file
    """
    with open(_txtfile, "wb") as f1:
        f1.write(_utfcalcS.encode("UTF-8"))

def _rstcalc(_rstcalcS, _rstfile):
    """[summary]
    
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

def r__(rawS: str):
    """convert repo-string to utf or rst-string
    
    Args:
        rawstrS (str): repo-string
    """
    global  _utfcalcS, _setsectD, _rivetD
    
    sectS,strS = rawS.split("\n",1)
    if "]_" in sectS: _update(sectS)
    
    strL = strS.split("\n")
    rcalc = _rivcalc._R_utf(strL, _foldD, _setsectD) 
    rcalcS, _setsectD = rcalc.r_parse()
    _utfcalcS = _utfcalcS + rcalcS

def i__(rawS: str):
    """convert insert-string to utf or rst-string
    
    Args:
        rawstrS (str): insert-string
    """
    global _utfcalcS, _setsectD, _foldD, _setcmdD

    sectS,strS = rawS.split("\n",1)
    if "]_" in sectS: _update(sectS)

    strL = strS.split("\n")
    icalc = _rivcalc._I_utf(strL, _foldD, _setcmdD, _setsectD) 
    icalcS, _setsectD, _setcmdD = icalc.i_parse()
    _utfcalcS = _utfcalcS + icalcS

def v__(rawS: str):
    """convert value-string to utf or rst-string
    
    Args:
        rawstr (str): value-string
    """
    global _utfcalcS, _setsectD, _foldD, _rivetD, _setcmdD, _exportS

    sectS,strS = rawS.split("\n",1)
    if "]_" in sectS: _update(sectS)
    
    strL = strS.split("\n")
    vcalc = _rivcalc._V_utf(strL, _foldD, _setcmdD, _setsectD, _rivetD, _exportS)
    vcalcS, _setsectD, _rivetD, _exportS = vcalc.v_parse()
    _utfcalcS = _utfcalcS + vcalcS

def e__(rawS: str):
    """convert equation-string to utf or rst-string

    """
    global _utfcalcS, _setsectD, _foldD, _rivetD, _setcmdD, _exportS

    sectS,strS = rawS.split("\n",1)
    if "]_" in sectS: _update(sectS)
    
    strL = strS.split("\n")
    ecalc = _rivcalc._E_utf(strL, _foldD, _setcmdD, _setsectD, _rivetD, _exportS)
    ecalcS, _setsectD, _rivetD, _exportS = ecalc.e_parse()
    _utfcalcS = _utfcalcS + ecalcS

def t__(rawS: str):
    """convert table-string to utf or rst-string
    
    """
    global _utfcalcS, _setsectD, _foldD, _setcmdD, _exportS

    sectS,strS = rawS.split("\n",1)
    if "]_" in sectS: _update(sectS)
    
    strL = strS.split("\n")
    tcalc = _rivcalc._T_utf(strL, _foldD, _setcmdD, _setsectD, _rivetD, _exportS)
    tcalcS, _setsectD, _exportS = tcalc.t_parse()
    _utfcalcS = _utfcalcS + tcalcS

def x__(rawS: str):
    """skip execution of a rivet-string
    """
    pass
