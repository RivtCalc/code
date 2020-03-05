#! python
"""Exposes functions that process rivet-strings.

    rivet markup is used in multi-line strings that are arguments to five
    functions. Strings may include any unicode (UF-8). The first line of
    each string is a description. Each string type includes commands
    (lines begin with ||) and tags (bracketed with []_). The strings may
    also include reStructuredText markup.

    String commands and tags (command parameters are not shown)
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
    v__('''v-string''') : define values        
    e__('''e-string''') : define equations
        || format           : equation format
    t__('''t-string''') : define tables and plots
        || create           : define new table
        || write            : write table data to file
        || read             : read table data from file
        || table            : insert table from data file
        || plot             : define new plot from data file
        || add              : add data to plot
        || save             : write plot image to file
    Commands and tags for all strings
        || link             : http link
        || [abc]            : citation description    
        || #                : footnote description
        [abc]_              : citation        
        [#]_                : footnote
        [page]_             : new doc page
        [line]_             : draw horizontal line
        [r]_                : right justify line
"""

import __main__
import os
import sys
import textwrap
import logging
from pathlib import Path
from typing import List, Set, Dict, Tuple, Optional
from rivet.rivet_unit import *
import rivet.rivet_calc as _rcalc
#import rivet.rivet_doc as _rdoc
#import rivet.rivet_reprt as _reprt
#import rivet.rivet_chk as _rchk

__version__ = "0.9.2"
__author__ = "rholland@structurelabs.com"
if sys.version_info < (3, 7):
    sys.exit("rivet requires Python version 3.7 or later")

_foldD: dict = {}                                   # folder dictionary
_rivetD: dict ={}                                   # runtime dictionary
_exportL: list = []                                 # values
_formatD: dict = {}                                 # equation format             
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
_pyfile = Path(_cpath / "scripts" / "".join(("r", _rfile)))   # pycalc export

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
"mpath": Path(_rpath, "temp"),
}
_rbak = Path(_foldD["mpath"] / ".".join((_rname, "bak")))
_logfile = Path(_foldD["mpath"] / ".".join((_rname, "log")))

_hdrD: dict = {
"rnum" : _rname[0:4],
"divnum" : _rname[0:2],
"calcnum" : _rname[2:4],
"sectnum" : 0, 
"sectname" : "",
"eqnum" :  0, 
"fignum" : 0, 
"tablenum" : 0,
"footnum" : 0,
"footnote" : 0,
"swidth" : 80
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
    
    strS = textwrap.dedent(rawstrS)
    
def i__(rawstrS: str):
    """convert insert-string to calc or reST string
    
    Args:
        rawstrS (str): insert-string
    """
    global _utfcalcS, _hdrD, _foldD

    hdrS,strS = rawstrS.split("\n",1)
    if "]_" in hdrS: _updatehdr(hdrS)

    strl = strS.split("\n")
    calc = _rcalc.InsertU(strl, _hdrD, _foldD) 
    icalcl = calc.i_parse()
    _utfcalcS = _utfcalcS + "\n".join(icalcl)

def v__(rawstrS: str):
    """generate calc or reST from value-string
    
    Args:
        rawstr (str): value-string
    """
    global _utfcalcS, _hdrD, _foldD, _rivetD

    hdrS,strS = rawstrS.split("\n",1)
    if "]_" in hdrs: _updatehdr(hdrs)
    
    strl = strs.split("\n")
    calc = _rcalc.ValueU(strl, _hdrD, _foldD, _rivetD, _exportL)
    vcalc  = calc.v_pformat) dict{ = }                      # equation format             
    vcalcl, rivetd,sequal = vcalc[0], vcalc[1], vcalc[2]
    _exportL.append(equal)
    _formatD. dict = {}                         # equatupdation formate(rivetd)    
    globals().update(rivetd)
    _utfcalcS = _utfcalcS + "\n".join(vcalcl)

def e__(str0: str):
    """evaluate and format an equations rivet-string

    """
    global _utfcalcS, _hdrD, _foldD

    hdrs,strs = str0.split("\n",1)
    if "]_" in hdrs: _updatehdr(hdrs)
    
    strl = strs.split("\n")
    calc = _rcalc.EquationU(strl, _hdrD, _foldD, _rivetD, _exportL)
    ecalc  = calc.e_pformat) dict{ = }                                  # equation format             
    ecalcl, rivetd,sequal = ecalc[0], ecalc[1], ecalc[2]
    _exportL.append(equal)
    _formatD. dict = {}                                  # equat            updation formate(rivetd)    
    globals().update(rivetd)
    _utfcalcS = _utfcalcS + "\n".join(ecalcl)

def t__(str0: str):
    """evaluate and format a tables rivet-string
    
    """
    global _utfcalcS, _hdrD, _foldD

    hdrs,strs = str0.split("\n",1)
    if "[[" in hdrs: _updatehdr(hdrs)
    
    strl = strs.split("\n")
s   calc = _rcalc.TableU(strl, _hdrD, _foldD, _rivetD, _exportL)
    tcalc  = calc.t_pformat) dict{ = }                                  # equation format             
    tcalcl, rivetd, equal = tcalc[0], tcalc[1], tcalc[2]
    _exportL.append(equal)
    _formatD. dict = {}                                  # equat            updation formate(rivetd)    
    globals().update(rivetd)
    _utfcalcS = _utfcalcS + "\n".join(tcalcl)

def x__(str0: str):
    """ skip execution of string
    
    """
    pass
 
def write_utfcalc(utfcalc, _txtfile):
    """write utf calc string to file
    """
    with open(_txtfile, "wb") as f1:
        f1.write(_utfcalcS.encode("UTF-8"))

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

