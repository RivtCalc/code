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

import __main__

__version__ = "0.9.2"
__author__ = "rholland@structurelabs.com"
if sys.version_info < (3, 7):
    sys.exit("rivet requires Python version 3.7 or later")

_foldd: dict = {}                                   # folder dictionary
_rivetd: dict ={}                                   # runtime dictionary
_exportl: list = []                                 # values, equations
_utfcalcs = """"""                                  # calc print string

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
# TODO: insert checks on folder structure here

def _updatehdr(hdrs:str):
    """update header dictionary
    
    Arguments:
        hdrs {str} -- header of rivet string
    """
    global _utfcalcs, _hdrd, _rdict

    _hdrd["eqnum"] = 0 
    _hdrd["fignum"] = 0
    _hdrd["tablenum"] = 0
    swidth = _hdrd["swidth"]
    rnums = _hdrd["rnum"]
    snames = _hdrd["sectname"] = hdrs[hdrs.find("]]") + 3 :].strip()
    snums = _hdrd["sectnum"] = hdrs[hdrs.find("[[")+2:hdrs.find("]]")]
    shead = " " +  snames + (str(rnums) + " - " +
           ("[" + str(snums) + "]")).rjust(swidth - len(snames) - 2)
    sstr = swidth * "="
    _utfcalcs += sstr + "\n" + shead + "\n" + sstr +"\n"

def r__(rawstr: str):
    """[summary]
    
    Arguments:
        rawstr {str} -- [description]
    """
    global  _utfcalcs, _hdrd, _rivetd
    
    hdrs,strs = rawstr.split("\n",1)
    if "[[" in hdrs: _updatehdr(hdrs)
    
    strs = textwrap.dedent(strs)
    
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

def v__(rawstr: str):
    """generate calc or doc string for insert

    """
    global _utfcalcs, _hdrd, _foldd, _rivetd

    hdrs,strs = rawstr.split("\n",1)
    if "[[" in hdrs: _updatehdr(hdrs)
    
    strl = strs.split("\n")
    calc = _rcalc.ValueU(strl, _hdrd, _foldd, _rivetd, _exportl)
    vcalc  = calc.v_parse()
    vcalcl, rivetd, equal = vcalc[0], vcalc[1], vcalc[2]
    _exportl.append(equal)
    _rivetd.update(rivetd)    
    globals().update(rivetd)
    _utfcalcs = _utfcalcs + "\n".join(vcalcl)

def e__(str0: str):
    """evaluate and format an equations rivet-string

    """
    global _utfcalcs, _hdrd, _foldd

    hdrs,strs = str0.split("\n",1)
    if "[[" in hdrs: _updatehdr(hdrs)
    
    strl = strs.split("\n")
    calc = _rcalc.EquationU(strl, _hdrd, _foldd, _rivetd, _exportl)
    ecalc  = calc.e_parse()
    ecalcl, rivetd, equal = ecalc[0], ecalc[1], ecalc[2]
    _exportl.append(equal)
    _rivetd.update(rivetd)    
    globals().update(rivetd)
    _utfcalcs = _utfcalcs + "\n".join(ecalcl)

def t__(str0: str):
    """evaluate and format a tables rivet-string
    
    """
    global _utfcalcs, _hdrd, _foldd

    hdrs,strs = str0.split("\n",1)
    if "[[" in hdrs: _updatehdr(hdrs)
    
    strl = strs.split("\n")
    calc = _rcalc.TableU(strl, _hdrd, _foldd, _rivetd, _exportl)
    tcalc  = calc.t_parse()
    tcalcl, rivetd, equal = tcalc[0], tcalc[1], tcalc[2]
    _exportl.append(equal)
    _rivetd.update(rivetd)    
    globals().update(rivetd)
    _utfcalcs = _utfcalcs + "\n".join(tcalcl)

def x__(str0: str):
    """ skip execution of string
    
    """
    pass
 
def write_utfcalc(utfcalc, _txtfile):
    """write utf calc string to file
    """
    with open(_txtfile, "wb") as f1:
        f1.write(_utfcalcs.encode("UTF-8"))

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

