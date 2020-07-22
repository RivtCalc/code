#! python
"""This module exposes the API for **RivetCalc**.  

    The API, summarized below, includes string input and write functions. 
    The string functions take **rivet** markup strings as arguments. 
    The first line of a string is a descriptor (may include a 
    section title). Markup options depend on the string type, and 
    includes unicode text, commands, tags and Python code. Text may 
    also include reStructuredText markup. The write functions control 
    calculation output type e.g. UTF-8, PDF, HTML.

    String input functions
    ----------------------

    type     API  text     commands {comment}
    ======= ===== ===== ================================================
    repo     R()   yes    calc, scope, attach
    insert   I()   yes    tex, sym, text, table, image
    value    V()   yes    =, values, vector, format, func, table, image 
    table    T()   no     {Python simple statements}, table, image 
    exclude  X()   --     {skip processing of rivet-string}

    Command syntax  
    ---------------
R(''' The repo-string defines repository and report data
    
    May include general text at the start of the string. No text is processed
    after reading a command. The toc argument generates a table of contents
    from section tags. The date argument generates a date string before the
    calc title.
    
    The first paragraph of the summary is included in the Github 
    README.rst file.
    
    || calc | calc title | date: mm,dd,yy | toc | readme

    || scope | discipline, object, condition, intent, assembly, component 
    
    || attach | front | calccover.pdf         
    || attach | back | functions 
    || attach | back | docstrings
    || attach | back | appendix1.pdf 
    ''')

I(''' The insert-string inserts predefined text, tables and images.  
    
    May include arbitrary text.
    
    || tex | \gamma = x + 3 # latex equation | 1. # image scale
    || sym | x = y/2 # sympy equation | 1.
    || table | x.txt | 60 # max paragraph width - characters 
    || table | x.csv | 60,[:] # max column width - characters, line range  
    || table | x.rst | [:] # line range

                                                             figure caption [f]_
    || image | x.png {image file} | 1. {scale}
    ''')

V(''' The value-string defines values and equations
    
    May include arbitrary text that does not include an equal sign.

    x = 10.1*IN      | description | unit, alt unit | {trailing, write to file}

    || vector | x.csv | VECTORNAME r[n] {row in file to vector}
    || vector | x.csv | VECTORNAME c[n] {column in file to vector}    
    || value | rccdd_values.py | [:] {import values from file}

    ||format | 2,2 {truncate result, terms} | sym {symbolic} | 

    v1 = x + 4*M  | unit, alt unit

    y1 = v1 / 4      | unit, alt unit | {if trailing |, write value to file}         

    || func | func_file.py | func_call | var_name {import function from file}
    || table | x.csv | 60    
    || image | x.png | 1.
    ''') 

T('''The table-string defines tables and plots
    
    {May include any simple Python statement (single line)}

    || table | x.csv | 60    
    || image | x.png, y.jpg | 0.5,0.5
    figure1 caption
    figure2 caption
    ''')

    Tags
    -------------------------------------------------------------------
    [nn]_ abc def      : section title and number
    [abc123]_          : citation        
    abc def [cite]_    : citation description    
    [#]_               : autonumbered footnote
    abc def [foot]_    : footnote description
    abc def [t]_       : right justify table title, autoincrement number   
    abc def [e]_       : right justify equation label, autoincrement number
    abc def [f]_       : right justify caption, autoincrement number   
    abc def [r]_       : right justify line of text
    abc def [c]_       : center line of text
    [literal]_         : literal text block
    [line]_            : draw horizontal line
    [page]_            : new doc page
    http://abc [link]_ : link

    Output functions
    -------------------------------------------------------------------
    write_values()     : write values to python file for import
    write_calc()       : write calc to utf8 text file
    write_pdf()        : write doc to pdf file
    write_html()       : write doc to html file
    write_report()     : write docs to pdf report file
    write_template()   : make template from project
"""
import __main__
import os
import sys
import textwrap
import logging
import warnings
import re
import numpy as np
from pathlib import Path
from collections import deque
from typing import List, Set, Dict, Tuple, Optional
from rivetcalc.rc_unit import *
import rivetcalc.rc_calc as _rc_calc
#import rivet.rivet_doc as _rdoc
#import rivet.rivet_reprt as _reprt
#import rivet.rivet_chk as _rchk

__version__ = "0.9.5"
__author__ = "rholland@structurelabs.com"
if sys.version_info < (3, 7):
    sys.exit("rivet requires Python version 3.7 or later")
# calc variables - global 
exportS  = """"""                                   # calc values export string
rivetcalcD: dict ={}                                # calc values dictonary
# start variables
_utfcalcS = """"""                                   # utf calc string
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
# settings - global 
_setsectD: dict = {"rnum": _cname[1:5],"dnum": _cname[1:3],"cnum": _cname[3:5],
"sname": "", "snum": "", "swidth": 80,
"enum":  0, "fnum": 0, "tnum" : 0, "ftnum": 0, "cite": " ",
"ftqueL": deque([1]), "ctqueL": deque([1])}
_setcmdD = {"cwidth": 50,"scale1": 1.,"scale2": 1.,"truncin": 2,"truncout": 2}
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
"apath": Path(_rppath, "attach")}
# temp files
_rbak = Path(_foldD["mpath"] / ".".join((_cname, "bak")))
_logfile = Path(_foldD["mpath"] / ".".join((_cname, "log")))
_rstfile = Path(_foldD["mpath"] / ".".join((_cname, "rst"))) 
#logs and checks
with open(_cfull, "r") as f2: calcbak = f2.read() 
with open(_rbak, "w") as f3: f3.write(calcbak)  # write backup
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
_rshortP = Path(*Path(_cfull).parts[-3:])
_bshortP = Path(*Path(_rbak).parts[-4:])
_lshortP = Path(*Path(_logfile).parts[-4:])
logging.info(f"""model: {_rshortP}""" )
logging.info(f"""backup: {_bshortP}""")
logging.info(f"""logging: {_lshortP}""")
print(" ")

# todo: check folder structure here



def _update(hdrS:str):
    """format section heading and update section settings

    Args:
        hdrS (str): section heading line
    """
    global _utfcalcS, _setsectD

    _rgx = r'\[\d\d\]\_'
    if re.search(_rgx,hdrS):        
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

def _callclass(rawS: str):
    """updates sections and returns class instance for rivet string

    Args:
        rawstr (str): rivet string

    Returns:
        class instance: string type instance
    """
    sectS,strS = rawS.split("\n",1);
    _update(sectS)
    strL = strS.split("\n")
    ucalc = _rc_calc.ParseUTF(strL, _foldD, _setcmdD, _setsectD, 
                                        rivetcalcD, exportS)
    return ucalc

def _rstcalc(_rstcalcS, _rstfile):
    """write reST calc string to file
    
    Args:
        pline ([type]): [description]
        pp ([type]): [description]
        indent ([type]): [description]
    """

    with open(_rstfile, "wb") as f1:
        f1.write(_rstcalcS.encode("UTF-8"))

def list_values():
    """write table of values to terminal 
    """
    rivetL = [[k,v] for k,v in rivetcalcD.items()]
    rivetT = []
    for i in rivetL:
        if isinstance(i[1], np.ndarray):
            if np.size(i[1]) > 3:
                i[1] = np.hstack([i[1][:4],["..."]])
            rivetT.append(i)

    print("." * _setsectD["swidth"])
    print("Values List")
    print("." * _setsectD["swidth"])                
    print(tabulate(rivetT, tablefmt="grid", headers=["variable", "value"]))
    print("." * _setsectD["swidth"] + "\n")

def write_values():
    """ write value assignments to Python file
 
        File name: calc file name prepended with 'v'
        File path: scipts folder      
    """
    
    str1 =  ("""header string""")
    str1 = str1 + _exportS
    with open(_expfile, 'w') as expF:
        expF.write(str1)

def write_utfcalc(utfcalc, _pyfile):
    """write utf calc string to file
    """
    pyfile = " "
    with open(pyfile, "wb") as f1:
        f1.write(_utfcalcS.encode("UTF-8"))

def write_htmldoc():
    """[summary]
    """
    with open(_txtfile, "wb") as f1:
        f1.write(utfcalc.encode("UTF-8"))

def write_pdfdoc():
    txtfile = " "
    with open(txtfile, "wb") as f1:
        f1.write(utfcalc.encode("UTF-8"))
    pdf_files = {
        "cpdf":  ".".join((_rbase, "pdf")),
        "chtml":  ".".join((_rbase, "html")),
        "trst":  ".".join((_rbase, "rst")),    
        "ttex1":  ".".join((_rbase, "tex")),
        "auxfile": ".".join((_rbase, ".aux")),
        "outfile":  ".".join((_rbase, ".out")),
        "texmak2":  ".".join((_rbase, ".fls")),
        "texmak3":  ".".join((_rbase, ".fdb_latexmk"))}

def write_pdfreport():
    """[summary]
    """
    pass

def R(rawS: str):
    """transform repository-string to utf and reST-string
    
    Args:
        rawstrS (str): repository-string
    """
    global  _utfcalcS,  _foldD, _setsectD, _setcmdD, rivetcalcD, exportS
    
    rcalc = _callclass(rawS)
    rcalcS, _setsectD = rcalc.r_utf()
    _utfcalcS += rcalcS

def I(rawS: str):
    """transform insert-string to utf and reST-string
    
    Args:
        rawstrS (str): insert-string
    """
    global _utfcalcS,  _foldD, _setsectD, _setcmdD, rivetcalcD, exportS
    
    icalc = _callclass(rawS)
    icalcS, _setsectD, _setcmdD = icalc.i_utf()
    _utfcalcS += icalcS

def V(rawS: str):
    """transform value-string to utf and reST-string
    
    Args:
        rawstr (str): value-string
    """
    global _utfcalcS,  _foldD, _setsectD, _setcmdD, rivetcalcD, exportS

    vcalc = _callclass(rawS)
    vcalcS, _setsectD, rivetcalcD, exportS = vcalc.v_utf()
    _utfcalcS += vcalcS

def T(rawS: str):
    """convert table-string to utf and reST-string
     
     Args:
        rawstr (str): table-string   
    """
    global _utfcalcS,  _foldD, _setsectD, _setcmdD, rivetcalcD, exportS

    tcalc = _callclass(rawS)
    tcalcS, _setsectD, exportS = tcalc.t_utf()
    _utfcalcS += tcalcS

def X(rawS: str):
    """exclude string
     
     Args:
        rawstr (str): any string to exclude
    """
    pass
