#! python
"""Exposes rivet-string functions.

    **rivet** markup is used in the five string functions and 4 processing
    functions exposed in this module. rivet-strings may include any unicode
    (UF-8). The first line of each string is a description. Each string type
    includes a set of commands (lines begin with ||) and tags (bracketed with
    []_). The strings may also include reStructuredText markup (
    https://docutils.sourceforge.io/docs/user/rst/quickref.html ).

    String functions with commands and tags (parameters not shown)
    --------------------------------------------------------------
    r__('''r-string''') : repository and calc data 
        || summary          : summary paragraph and table of contents
        || labels           : labels for search and database
        || append           : pdf files to append
    i__('''i-string''') : insert text and images
        || text             : text from file
        || tex              : LaTeX equation
        || sym              : sympy equation
        || img              : image from file
        || table            : table from file or inline
        || cite             : citation description    
        || foot             : footnote description
        [abc]_              : citation        
        [#]_                : footnote
    v__('''v-string''') : define values        
    e__('''e-string''') : define equations
        || format           : equation format
        || cite             : citation description    
        || foot             : footnote description
        [abc]_              : citation        
        [#]_                : footnote
    t__('''t-string''') : define tables and plots
        || create           : define new table
        || write            : write table data to file
        || read             : read table data from file
        || table            : insert table from data file
        || plot             : define new plot from data file
        || add              : add data to plot
        || save             : write plot image to file
        || img              : image from file
        || cite             : citation description    
        || foot             : footnote description    
        [abc]_              : citation        
        [#]_                : footnote
    Commands and tags for all rivet-strings
        || link             : http link
        [page]_             : new doc page
        [line]_             : draw horizontal line
        [r]_                : right justify line

    Process functions
    -----------------
    utfcalc()    : writes calc to text file
    pyvalues()   : writes all variable - values relations to python file
    pdfdoc()     : writes calc to pdf file
    htmldoc()    : writes calc to html file
    pdfreport()  : writes report to pdf file

"""
import __main__
import os
import sys
import textwrap
import logging
from pathlib import Path
from collections import deque
from typing import List, Set, Dict, Tuple, Optional
from rivet.rivet_unit import *
import rivet.rivet_calc as _rivcalc
#import rivet.rivet_doc as _rdoc
#import rivet.rivet_reprt as _reprt
#import rivet.rivet_chk as _rchk

__version__ = "0.9.0"
__author__ = "rholland@structurelabs.com"
if sys.version_info < (3, 7):
    sys.exit("rivet requires Python version 3.7 or later")

_rivetD: dict ={}                                   # runtime dictionary
_exportL: list = []                                 # values
_utfcalcS = """"""                                  # calc print string
_rfull = Path(__main__.__file__)                    # calc file path
_rfile = Path(__main__.__file__).name               # calc file name
_rname = _rfile.split(".py")[0]                     # calc file basename
_rivpath = Path("rivet.rivet_lib.py").parent        # rivet program path
_cpath =  Path(_rfull).parent                       # calc folder path
_ppath = Path(_rfull).parent.parent                 # project folder path
_dpath = Path(_ppath / "docs")                      # doc folder path
_rpath = Path(_ppath / "reports")                   # report folder path
_txtfile = Path(_cpath / ".".join((_rname, "txt"))) # calc output
_pyfile = Path(_cpath / "scripts" / "".join(("r", _rfile))) # pycalc export

# folders 
_foldD: dict = {
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
"mpath": Path(_rpath, "temp")
}
_rbak = Path(_foldD["mpath"] / ".".join((_rname, "bak")))
_logfile = Path(_foldD["mpath"] / ".".join((_rname, "log")))

# section headers
_hdrD: dict = {"rnum": _rname[0:4],"divnum": _rname[0:2],"calcnum": _rname[2:4],
"sectnum": 0, "sectname": "",
"eqnum":  0, "fignum": 0, "tablenum" : 0,
"footnum": 0,"footnote": 0,"footque": deque([1]),
"swidth": 80}

# command settings
_setD = {"txtwidth": 60, "scale1": 1, "scale2": 1,
        "row": "[:]", "col": "[:]", 
        "equ": 2, "ans": 2 , "chk": 0, "prt": 2}

def shorten_path(file_path: str, length: int)-> str:
    """split path and return path of depth = length
    
    Args:
        file_path (str): path to shorten
        length (int): path depth
    
    Returns:
        str: shortened path
    """
    return Path(*Path(file_path).parts[-length:])

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

_rshort = shorten_path(_rfull, 3)
logging.info(f"""rivet file : {_rshort}""" )
with open(_rfull, "r") as f2: calcbak = f2.read()
with open(_rbak, "w") as f3: f3.write(calcbak)  # write backup
_rshort = shorten_path(_rbak, 4)
logging.info(f"""backup file written : {_rshort}""")
# TODO: call check on folder structure here

def _updatehdr(hdrS:str):
    """update header dictionary
    
    Arguments:
        hdrs {str} -- header of rivet string
    """
    global _utfcalcS, _hdrD, _rivetD

    _hdrD["eqnum"] = 0 
    _hdrD["fignum"] = 0
    _hdrD["tablenum"] = 0
    swidthI = int(_hdrD["swidth"])
    rnumS = str(_hdrD["rnum"])
    snameS = _hdrD["sectname"] = hdrS[hdrS.find("]_") + 2:].strip()
    snumS = _hdrD["sectnum"] = hdrS[hdrS.find("[")+2:hdrS.find("]_")]
    sheadS = " " +  snameS + (rnumS + " - " +
           ("[" + str(snumS) + "]")).rjust(swidthI - len(snameS) - 2)
    sstrS = swidthI * "="
    _utfcalcS += sstrS + "\n" + sheadS + "\n" + sstrS +"\n"

def r__(rawstrS: str):
    """convert repo-string to calc or reST string
    
    Args:
        rawstrS (str): repo-string
    """
    global  _utfcalcS, _hdrD, _rivetD
    
    hdrS,strS = rawstrS.split("\n",1)
    if "]_" in hdrS: _updatehdr(hdrS)
    
    strL = strS.split("\n")
    rcalc = _rivcalc.RepoU(strL, _hdrD, _foldD) 
    rcalcS = rcalc.r_parse()
    _utfcalcS = _utfcalcS + rcalcS

def i__(rawstrS: str):
    """convert insert-string to calc or reST string
    
    Args:
        rawstrS (str): insert-string
    """
    global _utfcalcS, _hdrD, _foldD, _setD

    hdrS,strS = rawstrS.split("\n",1)
    if "]_" in hdrS: _updatehdr(hdrS)

    strL = strS.split("\n")
    icalc = _rivcalc.InsertU(strL, _hdrD, _foldD, _setD) 
    icalcS, _hdrD, _setD = icalc.i_parse()
    _utfcalcS = _utfcalcS + icalcS

def v__(rawstrS: str):
    """generate calc or reST from value-string
    
    Args:
        rawstr (str): value-string
    """
    global _utfcalcS, _hdrD, _foldD, _rivetD, _setD, _exportL

    hdrS,strS = rawstrS.split("\n",1)
    if "]_" in hdrS: _updatehdr(hdrS)
    
    strL = strS.split("\n")
    vcalc = _rivcalc.ValueU(strL, _hdrD, _foldD, _rivetD)
    vcalcS, _exportS, _hdrD, _rivetD = vcalc.v_parse()
    _utfcalcS = _utfcalcS + vcalcS

def e__(rawstrS: str):
    """evaluate and format an equations rivet-string

    """
    global _utfcalcS, _hdrD, _foldD, _rivetD, _setD, _exportL

    hdrS,strS = rawstrS.split("\n",1)
    if "]_" in hdrS: _updatehdr(hdrS)
    
    strL = strS.split("\n")
    ecalc = _rivcalc.EquationU(strL, _exportL, _hdrD, _foldD, _rivetD, _setD)
    ecalcS, _exportS, _hdrD, _rivetD = ecalc.e_parse()
    _utfcalcS = _utfcalcS + ecalcS

def t__(rawstrS: str):
    """evaluate and format a tables rivet-string
    
    """
    global _utfcalcS, _hdrD, _foldD, _rivetD, _setD, _exportL

    hdrS,strS = rawstrS.split("\n",1)
    if "]_" in hdrS: _updatehdr(hdrS)
    
    strL = strS.split("\n")
    tcalc = _rivcalc.TableU(strL, _hdrD, _foldD, _exportL, _rivetD)
    vcalcS, _imgD, _tableD = vcalc.i_parse()
    _utfcalcS = _utfcalcS + vcalcS

def x__(str0: str):
    """ skip execution of string
    
    """
    pass
 
def _rstcalc(pline, pp, indent):
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
def utfcalc(utfcalc, _txtfile):
    """write utf calc string to file
    """
    with open(_txtfile, "wb") as f1:
        f1.write(_utfcalcS.encode("UTF-8"))

def pyvalues():
    """ write rivet independent python file of values
 
        Write a Python file with values and _equation results.  
        Used for extensions and importing design information 
        into other rivet or python files.  File name
        is the calc file name prepended with 'v'.      
    """
    str1 =  ("""\nThis file contains Python _equations 
            from the rivet design file 
            for lsti in zip(vlistx, vlisty)
            if __name__ == "__main__":\n
            vlist()\n\n""")
    _rfile.write("\n")
    
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
