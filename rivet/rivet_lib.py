#! python
"""rivet_lib - evaluate and format a rivet-string

    Exposes functions which process rivet-strings.

    The language includes five types of strings. 
    The first line of each sets string parameters.

    function and string type
    r__() : python code 
    i__() : insert text and images
    v__() : define values
    e__() : define equations
    t__() : define tables and plots
        
"""
#test 12345

import osw
import sys
import textwrap
import logging
from pathlib import Path
from typing import List, Set, Dict, Tuple, Optional

from numpy import *
import numpy.linalg as la
import pandas as pd
import sympy as sy
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from rivet.rivet_unit import *
import rivet.rivet_calc as _rcalc
#import rivet.rivet_doc as _rdoc
#import rivet.rivet_reprt as _reprt
#import rivet.rivet_chk as _rchk

import __main__

__version__ = "0.9.2"
__author__ = "rholland@structurelabs.com"
if sys.version_info < (3, 7):
    sys.exit("rivet requires Python version 3.7 or later")

setd: dict = {}                                     # formats
tagd: dict = {}                                     # subject tags
_foldd: dict = {}                                   # folder dictionary
_rund: dict ={}                                     # runtime dictionary
_export: list = []                                  # values, equations
_indxd: dict = {}                                   # calc index
_utfcalcs = """"""                                  # calc string

_rfull = Path(__main__.__file__)                    # calc file path
_rfile = Path(__main__.__file__).name               # calc file name
_rname = _rfile.split(".py")[0]                     # calc file basename
_rivpath = Path("rivet.rivet_lib.py").parent        # rivet program path
_cpath =  Path(_rfull).parent                       # calc folder path
_ppath = Path(_rfull).parent.parent                 # project folder path
_dpath = Path(_ppath / "docs")                      # doc folder path
_rpath = Path(_ppath / "reports")                   # report folder path
_txtfile = Path(_cpath / ".".join((_rname, "txt"))) # calc output
_pyfile = Path(_cpath / "scripts" / "".join(("r", _rfile)))   # pycalc export

_foldd: dict = {
"ppath": _ppath,
"cpath": Path(_rfull).parent,
"dpath": _dpath,
"rpath": _rpath,   
"spath": Path(_cpath, "scripts"),
"kpath": Path(_cpath, "sketches"),
"tpath": Path(_cpath, "tables"),
"xpath": Path(_cpath, "text"),
"hpath": Path(_dpath, "html"),
"fpath": Path(_dpath, "html/figures"),
"apath": Path(_rpath, "append"),
"mpath": Path(_rpath, "temp"),
}
_rbak = Path(_foldd["mpath"] / ".".join((_rname, "bak")))
_logfile = Path(_foldd["mpath"] / ".".join((_rname, "log")))

_hdrd: dict = {
"rnum" : _rname[0:4],
"divnum" : _rname[0:2],
"calcnum" : _rname[2:4],
"sectnum" : 0, 
"sectname" : "",
"eqnum" :  0, 
"fignum" : 0, 
"tablenum" : 0,
"calcwidth" : 80
}

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

logging.info(f"""rivet file : {_rfull}""" )
with open(_rfull, "r") as f2: calcbak = f2.read()
with open(_rbak, "w") as f3: f3.write(calcbak)  # write backup
logging.info(f"""backup file written : {_rbak}""")
# TODO: insert check on folder structure here

def _updatehdr(hdrs:str):
    """update header dictionary
    
    Arguments:
        hdrs {str} -- header of rivet string
    """
    global _utfcalcs, _hdrd, _rdict

    rnums = _hdrd["rnum"]
    snames = _hdrd["sectname"] = hdrs[hdrs.find("]]") + 3 :].strip()
    snums = _hdrd["sectnum"] = hdrs[hdrs.find("[[")+2:hdrs.find("]]")]
    calcwidth = _hdrd["calcwidth"]
    sstr = ('=' * calcwidth)
    shead = " " +  snames + (str(rnums) + " - " +
           ("[" + str(snums) + "]")).rjust(calcwidth - len(snames) - 2)
    _hdrd["eqnum"] = 0 
    _hdrd["fignum"] = 0
    _hdrd["tablenum"] = 0
    
    _utfcalcs += sstr + "\n" + shead + "\n" + sstr +"\n"

def r__(rawstr: str):
    """[summary]
    
    Arguments:
        rawstr {str} -- [description]
    """
    global  _utfcalcs, _indxd, _rund

    _indxd["calcwidth"] = 80
    try:
        _indxd["calcwidth"] = rsetd["width"]
    except:
        pass
    
    hdrs,strs = rawstr.split("\n",1)
    if "[[" in hdrs: _updatehdr(hdrs)

    
    strs = textwrap.dedent(strs)
    exec(strs, globals())
    _rund.update(locals())
    globals().update(locals())

def i__(rawstr: str):
    """generate calc or reST string for insert
    
    Arguments:
        rstr {str} -- [description]
    """
    global _utfcalcs, _hdrd, _foldd

    hdrs,strs = rawstr.split("\n",1)
    if "[[" in hdrs: _updatehdr(hdrs)

    strl = strs.split("\n")
    calc = _rcalc.InsertU(strl, _hdrd, _foldd) 
    icalcl = calc.i_parse()

    _utfcalcs = _utfcalcs + "\n".join(icalcl)
    print(_utfcalcs)

def v__(str0: str):
    """generate calc or doc string for insert

    """
    global rset, utfcalc

    str1,str2 = str0.split("\n",1)
    strset = _rsets(str1)
    calc = _utf.ValueU(str2.split("\n"), _rdict, rdir,  strset[3])
    dict1, calc1, equ1 = calc.v_parse()

    if strset[2] == 1: 
        calc(calc1, strset)
    
    _equations.append(equ1)
    _rdict.update(dict1)    
    globals().update(dict1)

def e__(str0: str):
    """evaluate and format an equations rivet-string

    """
    global rset, utfcalc

    str1,str2 = str0.split("\n",1)
    strset = _rsets(str1)
    calc = _utf.EquationU(str2.split("\n"), _rdict, rdir,  strset[3])
    dict1, calc1, equ1 = calc.e_parse()
    
    if strset[2] == 1: 
        calc(calc1, strset)
    
    _equations.append(equ1)
    _rdict.update(dict1)
    globals().update(dict1)

def t__(str0: str):
    """evaluate and format a tables rivet-string
    
    """
    global rset, utfcalc

    str1,str2 = str0.split("\n",1)
    strset = _rsets(str1)
    calc = _utf.Table_u(str2.split("\n"), _rdict, rdir,  strset[3])
    dict1, calc1, equ1 = calc.t_parse()
    
    if strset[2] == 1: 
        calc(calc1, strset)
    
    _equations.append(equ1)
    _rdict.update(dict1)
    globals().update(dict1)

def x__(str0: str):
    """ skip execution of string
    
    """
    pass

def _print_utfcalc(_utfcalc: str, strset: list):
    """ print utfcalc to terminal
    
    Args:
        rivets (list): text 
        pp (int): pretty print flag
        indent (int): indent flag 
    """    
    global utfcalc

    rivstr1 = []
    sect_num = int(strset[3][1])
    descrip = strset[1]
 

def write_utfcalc(utfcalc, _txtfile):
    """write utf calc string to file
    """
    with open(_txtfile, "wb") as f1:
        f1.write(_utfcalcs.encode("UTF-8"))

def write_htmldoc():
    """[summary]
    """
    with open(_txtfile, "wb") as f1:
        f1.write(utfcalc.encode("UTF-8"))

def write_pdfdoc():
    with open(_txtfile, "wb") as f1:
        f1.write(utfcalc.encode("UTF-8"))

def write_pdfreport():
    """[summary]
    """
    pass

def write_pycalc():
    """ write rivet independent python file
 
        Write a Python file with values and _equations and excluding
        explanatory text and formatting.  Used for extensions and 
        importing design information into other rivet files.      
    """
    str1 =  ("""\nThis file contains Python _equations 
            from the rivet design file 
            for lsti in zip(vlistx, vlisty)
            if __name__ == "__main__":\n
            vlist()\n\n""")
    _rfile.write("\n")

def _write_rstcalc(pline, pp, indent):
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

