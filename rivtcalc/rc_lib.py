#! python
"""exposes RivtCalc API.  

    The API includes string input and output functions. Input functions take
    rivt-markup strings as arguments and output utf-formatted calcs to the
    terminal. Ouput functions write formatted calculations to files in utf-8,
    pdf and html formats.
    
    Markup includes unicode text, commands, tags and Python code. Options
    depend on the rivt-string type (R,I,V or T). Strings may also include
    reStructuredText markup. 

    Input functions ------------------------------------------------------------
    type     API  text  tags     commands {comment}
    ======= ===== ===== =====  =================================================
    report   R()   yes   no    heading, tag, pdf
    insert   I()   yes   yes   tex, sym, text, table, image
    values   V()   yes   yes   =, config, value, data, func, +insert commands
    table    T()   no    yes   Python (pandas) simple statements+insert commands  
    skip     S()   --     --   skip processing rivt-string processing

    Output functions -----------------------------------------------------------
        name                   description
    =================  =========================================================
    1.write_utf()        write calc to utf8 doc file
    2.write_pdf()        write calc to pdf doc file
    3.write_html()       write calc to html doc file
    4.write_report()     combine pdf docs into pdf report file
    =================  =========================================================

    Commands and tags for each string type are described below. The first line
    of each rivt-string is a descriptor which may include a section designator
    and title. String text must be indented 4 spaces after the first descriptor
    line.

Input Syntax and commands ------------------------------------------------------

from rivtcalc import rc_lib as rc
rc.R('''report-string defines respository and document formats
    
    Report-strings may include general text at the start of the string. The
    ||heading command specifies an optional calc title and date printed at the
    top of each page. Arguments in brackets are user provided. Parameters not
    in brackets are input as shown. Options are separated by semicolon. The toc
    parameter generates a table of contents from section tags. The read
    parameter writes a README.rst file for Github or other online repositories.
    The first paragraph of the report-string becomes part of the README.rst
    file for the project. 

    ||heading | [calc title] | toc; notoc | read; noread | [date]

    The ||tag command lists terms describing the scope of the calc with up to
    five terms per command. Tags and a generated index of search terms from the
    calc are also included in the README.
    
    ||tag | [discipline], [object], [purpose], [assembly], [component]
    ||tag | [code1], [code2], [code3], .... 

    The ||pdf command attaches, in order, existing pdf documents to the front
    or back of the calc doc. PDF files to attach files are stored in the
    docs/attach/ folder.
    
    ||pdf | front | [calccoverfile.pdf]         
    ||pdf | back | functions; docstrings
    ||pdf | back | [appendixfile.pdf] 
    ''')
rc.I('''insert-string contains static text, tables and images.  
    
    Insert-strings generate formatted static text, equations and images. They
    may include arbitrary text.
                                                               equations [e]_
    ||tex | \gamma = x + 3 # latex equation 
    ||sym | x = y/2 # sympy equation 
    ||text | f.txt | 60 \ literal {max char. width or literal}  
    
    table title [t]_
    ||table | f.csv | 60,c {width, align} | title {in csv} | [2,1,4] {cols} 

    figure caption [f]_
    ||image | f.png {image file} | 1. {scale}
    
    first figure caption (side by side) [f]_
    second figure caption [f]_
    ||image | f1.png, f2.jpg | 1.,0.5
    ''')
rc.V('''value-string defines active values and equations
    
    Value-strings may include arbitrary text that does not include an equal
    sign.  Lines with equal signs define equations and assignments that 
    will be numerically evaluated.
    
    Set value parameters where sub means to render equation with substition.
    ||config | sub {or nosub} | 2,2 {truncate result, terms}  
    
    x1 = 10.1    | unit, alt unit | description || {save if trailing ||}
    y1 = 12.1    | unit, alt unit | description  

    Import values from a csv file, starting with the second row.    
    ||value | file | f.csv
    
    Import a list of values from rows of a csv file 
    ||data | f.csv | [1:4] {rows to import} 

    For a value file the csv file must have the structure:
    [literal]_
    variable name, value, primary unit, secondary unit, description 
    
    For a data file the csv file must have the structure:
    [literal]_
    variable name, value1, value2, value3, ....
    
    an equation [e]_
    v1 = x + 4*M  | unit, alt unit
    save an equation result to file [e]_
    y1 = v1 / 4   | unit, alt unit ||         

    ||func | func_file.py | func_call | var_name {import function from file}

    a table title [t]_
    ||table | x.csv | 60    
    
    figure caption [f]_
    ||image | x.png | 1.
    ''') 
rc.T('''table-string defines tables and plots with simple Python statements
    
     Table-strings may include any simple Python statement (single line),
     insert-commands or tags.
    ''')

    Tags -----------------------------------------------------------------------
       tag               description
    ===============  ===========================================================
    [nn]_ abc def       section title and number in descriptor line (first line)
    [#]_                autonumbered footnote      
    abc def [foot]_     footnote description
    abc def [t]_        right justify table title, autoincrement number   
    abc def [e]_        right justify equation label, autoincrement number
    abc def [f]_        right justify caption, autoincrement number   
    abc def [r]_        right justify line of text
    abc def [c]_        center line of text
    [literal]_          literal text block
    [line]_             draw horizontal line
    [page]_             new doc page
    http://abc [link]_  link
"""
import os
import sys
import time
import textwrap
import logging
import warnings
import re
import runpy
import numpy as np
from pathlib import Path
from collections import deque
from typing import List, Set, Dict, Tuple, Optional
from rivtcalc.rc_unit import *
import rivtcalc.rc_calc as _rc_calc
from contextlib import suppress
#import rivt.rivt_doc as _rdoc
#import rivt.rivt_reprt as _reprt
#import rivt.rivt_chk as _rchk                   

try: _calcfileS = sys.argv[1]                           #  check source of file
except: _calcfileS = sys.argv[0]
if ".py" not in _calcfileS:
    import __main__; _calcfileS = (__main__.__file__)
    #print("model file from IDE: ", _modfileS)
 
_cwdS = os.getcwd()
_cfull = Path(_calcfileS)                            # calc file full path
_cfileS   = _cfull.name                              # calc file name
_cname    = _cfileS.split(".py")[0]                  # calc file basename
_rivpath  = Path("rivtcalc.rivt_lib.py").parent      # rivt program path
_cpath    = _cfull.parent                            # calc folder path
_ppath    = _cfull.parent.parent                     # project folder path
_dpath    = Path(_ppath / "docs")                    # doc folder path
_rppath   = Path(_dpath / "report")                  # report folder path
_rname    = "c"+_cname[1:]                           # calc file basename
_utffile  = Path(_cpath / ".".join((_rname, "txt"))) # utf output
_expfile  = Path(_cpath / "data" / "".join(_cfileS)) # export file

# global settings
utfcalcS = """"""                                    # utf calc string
rstcalcS = """"""                                    # reST calc string
exportS  = """"""                                    # values export string
rivtcalcD = {}                                       # values dictonary
# folder paths
_foldD: dict = {
"efile": _expfile,   
"ppath": _ppath,
"dpath": _dpath,
"rpath": _rppath,
"cpath": Path(_cfull).parent,
"mpath": Path(_ppath, "tmp"),
"spath": Path(_cpath, "scripts"),
"kpath": Path(_cpath, "sketches"),
"tpath": Path(_cpath, "data"),
"xpath": Path(_cpath, "text"),
"hpath": Path(_dpath, "html"),
"apath": Path(_rppath, "attach")}
# section settings
_setsectD = {"cnumS": _cname[1:5], "dnumS": _cname[1:3], "sdnumS": _cname[3:5],
            "snameS": "", "snumS": "", "swidthI":80, "enumI":0, "tnumI":0,
    "figqueL":deque([[0,"cap"]]), "eqqueL":deque([1]), "ftqueL":deque([1])}
# command settings
_setcmdD = {"cwidthI":30, "calignS":"s", "titleS":"notitle", 
                     "scale1F": 1.,"scale2F": 1.,"writeS":"table",
                     "subst": False, "saveB": False, "trmrI": 2,"trmtI": 2}

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
print(" ")                       # todo: check folder structure here

def _initclass(rawS: str):
    """return class instance for rivt-string

    Args:
        rawstr (str): rivt-string

    Returns:
        class instance: string-type instance
    """
    sectS,strS = rawS.split("\n",1); _section(sectS)
    strL = strS.split("\n")
    ucalc = _rc_calc.ParseUTF(strL,_foldD,_setcmdD,_setsectD, rivtcalcD, exportS)
    return ucalc 

def _section(hdrS: str):
    """format section headings and settings 

    Args:
        hdrS (str): section heading line
    """
    global utfcalcS, _setsectD

    _rgx = r'\[\d\d\]'
    if re.search(_rgx,hdrS):        
        _setsectD["enumI"] = 0               # equation number
        _setsectD["fnum"] = 0               # figure number
        _setsectD["tnumI"] = 0               # table number
        nameS = _setsectD["snameS"] = hdrS[hdrS.find("]") + 2:].strip()
        snumSS = _setsectD["snumS"] = hdrS[hdrS.find("[")+1:hdrS.find("]")]
        cnumSS = str(_setsectD["cnumS"])
        widthI = int(_setsectD["swidthI"])
        headS = " " +  nameS + (cnumSS + " - " +
                ("[" + snumSS + "]")).rjust(widthI - len(nameS) - 1)
        bordrS = widthI * "_"
        utfS = "\n" + bordrS + "\n\n" + headS + "\n" + bordrS +"\n"
        print(utfS); utfcalcS += utfS

def write_values():
    """ write value assignments to csv file
 
        File name: calc file name prepended with 'v'
        File path: data folder      
    """
    
    str1 =  ("""header string\n""")
    str1 = str1 + exportS
    with open(_expfile, 'w') as expF: expF.write(str1)

def write_utf():
    """write utf-string and reST-string files
    """
    global utfcalcS

    f1 = open(_cfull, "r"); utfcalcL = f1.readlines(); f1.close()
    print("model file read: " + str(_cfull))
    for iS in enumIerate(utfcalcL):
        if "write_utf" in iS[1]: 
            indx = int(iS[0]); break
    utfcalcL = utfcalcL[0:indx]+utfcalcL[indx+1:]
    cmdS = ''.join(utfcalcL)
    exec(cmdS, globals(), locals())
    with open(_utffile, "wb") as f1: f1.write(utfcalcS.encode("UTF-8"))
    print("utf calc written to file", flush=True)
    with suppress(BaseException): raise SystemExit()
    print("program complete")
    utfcalcS = """"""

def write_pdf():
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

def write_html():
    """[summary]
    """
    with open(_txtfile, "wb") as f1:
        f1.write(utfcalc.encode("UTF-8"))

def write_report():
    """[summary]
    """
    pass

def R(rawS: str):
    """repository-string to utf-string
    
    Args:
        rawstrS (str): repository-string
    """
    global  utfcalcS,  _foldD, _setsectD, _setcmdD, rivtcalcD, exportS
    
    rcalc = _initclass(rawS)
    rcalcS, _setsectD = rcalc.r_utf()
    utfcalcS += rcalcS

def I(rawS: str):
    """insert-string to utf-string
    
    Args:
        rawstrS (str): insert-string
    """
    global utfcalcS,  _foldD, _setsectD, _setcmdD, rivtcalcD, exportS
    
    icalc = _initclass(rawS)
    icalcS, _setsectD, _setcmdD = icalc.i_utf()
    utfcalcS += icalcS

def V(rawS: str):
    """value-string to utf-string
    
    Args:
        rawstr (str): value-string
    """
    global utfcalcS,  _foldD, _setsectD, _setcmdD, rivtcalcD, exportS

    vcalc = _initclass(rawS)
    vcalcS, _setsectD, _setcmdD, rivtcalcD, exportS = vcalc.v_utf()
    utfcalcS += vcalcS

def T(rawS: str):
    """table-string to utf-string
     
     Args:
        rawstr (str): table-string   
    """
    global utfcalcS,  _foldD, _setsectD, _setcmdD, rivtcalcD, exportS

    tcalc = _initclass(rawS)
    tcalcS, _setsectD, _setcmdD, rivtcalcD = tcalc.t_utf()
    utfcalcS += tcalcS

def X(rawS: str):
    """exclude string from processing
     
     Args:
        rawstr (str): any string to exclude
    """
    pass
