#! python
"""exposes RivtCalc API.  

    The API includes string input and output functions. Input functions take
    rivt-markup strings as arguments and output utf-formatted calcs to the
    terminal. Ouput functions write formatted calculations to files in utf-8,
    pdf and html formats.
    
    Markup includes unicode text, commands, tags and Python code. Options
    depend on the rivt-string type (R,I,V or T). Strings may also include
    reStructuredText markup. 

    Input functions ----------------------------------------------------
    type     API  text   tags     commands {comment}
    ======= ===== ===== ====== =========================================
    repo     R()   yes    no    header, scope, codes, attach
    insert   I()   yes    yes   tex, sym, text, table, image
    value    V()   yes    yes   =, value, {and insert commands}
    table    T()   no     yes   {Python simple statements and insert commands}  
    exclude  X()   --      --   {skip processing of rivt-string}

    Output functions -----------------------------------------------------
        name                   description
    =================  ===================================================
    write_values()     write values to python file for import
    write_utf()        write calc to utf8 text file
    write_pdf()        write calc to pdf file
    write_html()       write doc to html file
    write_report()     write docs to pdf report file

    Commands and tags for each string type are described below in the context
    of the string function type. The first line of a rivt-string is a
    descriptor (may include a section title). For clarity, string text must be
    indented 4 spaces after the first descriptor line.


Input Syntax ----------------------------------------------------

R('''repo-string defines repository and report data
    
    Repo strings may include general text at the start of the string. The first
    paragraph of the summary becomes part of the Github README.rst file for the
    project.
    
    The ||calc command specifies the calc title and date printed at the top of
    each page. The toc argument generates a table of contents from section tags
    at the beginning of the calc. The readme argument triggers a README.txt
    output for Github. A generated index of search terms from the calc is
    included in the README. The scope command provides high level descriptive 
    labels for searching.
    
    ||header | calc title | mm,dd,yy {date} | toc | readme

    ||scope | discipline, object, condition, intent, assembly, component
    ||codes | code1, code2 
    
    ||attach | front | calccover.pdf         
    ||attach | back | functions 
    ||attach | back | docstrings
    ||attach | back | appendix1.pdf 
    ''')
I('''insert-string contains static text, tables and images.  
    
    Insert-strings generate formatted static text, equations and images. They
    may include arbitrary text.

                                                                  equations [e]_
    ||tex | \gamma = x + 3 # latex equation 
    ||sym | x = y/2 # sympy equation 
    ||text | x.txt | 60 {max char. width}  
    
                                                                table title [t]_
    ||table | x.csv | 60 {max width} | [2,1,3,4] {cols} | [1,3] {totals} | [4]

    ||image | x.png {image file} | 1. {scale}
                                                             figure caption [f]_
    
    Side by side images.
    ||image | x.png, y.jpg | 1.,0.5
                                                       first figure caption [f]_
                                                      second figure caption [f]_
    ''')
V('''value-string defines active values and equations
    
    Value-strings may include arbitrary text that does not include an equal
    sign.  Lines with equal signs define equations and assignments that 
    are numerically evaluated.

    x1 = 10.1*IN    | description | unit, alt unit || {save if trailing ||}
    y1 = 12.1*FT    | description | unit, alt unit 


    Set value parameters where sub means to render equation with substition.
    ||value | sub {or nosub} | 2,2 {truncate result, terms}  
    
    Import values from csv or xlxs file, starting with the second row.    
    ||value | file | file.csv or file.xlsx
    
    The csv file must have the structure:
    [literal]_
    variable name, value, description, primary unit, secondary unit

    Import a list of values from a csv file 
    ||value | list | file.csv | [1:4] {rows to import}

    The csv file must have the structure:
    [literal]_
    variable name, value1, value2, value3, ....
    


    v1 = x + 4*M  | unit, alt unit

                                                           another equation [e]_
    y1 = v1 / 4   | unit, alt unit || {save if trailing ||}         

    ||func | func_file.py | func_call | var_name {import function from file}

                                                        another table title [t]_
    ||table | x.csv | 60    
    
    ||image | x.png | 1.
                                                             figure caption [f]_
    ''') 
T('''table-string defines tables and plots with simple Python statements
    
    {Table-strings may include any simple Python statement (single line),
     insert-string command or tag}

    ''')

    Tags -----------------------------------------------------------------
       tag               description
    ===============  ======================================================
    [nn]_ abc def       section title and number in first (descriptor) line
    [abc123]_           citation        
    abc def [cite]_     citation description    
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
import textwrap
import logging
import warnings
import re
import numpy as np
from pathlib import Path
from collections import deque
from typing import List, Set, Dict, Tuple, Optional

from rivtcalc.rc_unit import *
import rivtcalc.rc_calc as _rc_calc
#import rivt.rivt_doc as _rdoc
#import rivt.rivt_reprt as _reprt
#import rivt.rivt_chk as _rchk                   

try:
    _modfileS = sys.argv[1]                           #  check source of file
except:
    _modfileS = sys.argv[0]
if ".py" in _modfileS:
    print("model file from command line: ", _modfileS)
    write_utf()
else:
    import __main__
    _modfileS = (__main__.__file__)
    print("model file from IDE: ", _modfileS)
 
_cwdS = os.getcwd()
_cfull = Path(_modfileS)                             # model file full path
_cfileS   = _cfull.name                              # model file name
_cname    = _cfileS.split(".py")[0]                  # model file basename
_rivpath  = Path("rivtcalc.rivt_lib.py").parent    # rivt program path
_cpath    = _cfull.parent                            # calc folder path
_ppath    = _cfull.parent.parent                     # project folder path
_dpath    = Path(_ppath / "docs")                    # doc folder path
_rppath   = Path(_ppath / "reports")                 # report folder path
_rname    = "c"+_cname[1:]                           # calc file basename
_utffile  = Path(_cpath / ".".join((_rname, "txt"))) # utf calc output
_expfile  = Path(_cpath / "scripts" / "".join(_cfileS)) # export file
# settings - global 
utfcalcS = """"""                                   # utf calc string
rstcalcS = """"""                                   # reST calc string
exportS  = """"""                                   # calc values export string
rivtcalcD: dict ={}                                # calc values dictonary
_setsectD: dict = {"rnum": _cname[1:5],"dnum": _cname[1:3],"cnum": _cname[3:5],
                    "sname": "", "snum": "", "swidth": 80,
                    "enum":  0, "fnum": 0, "tnum" : 0, "ftnum": 0, "cite": " ",
                    "ftqueL": deque([1]), "ctqueL": deque([1])}
_setcmdD = {"cwidth": 50,"scale1F": 1.,"scale2F": 1.,"writeS": "table",
                                    "saveB": False, "trmrI": 2,"trmtI": 2}
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
"fpath": Path(_dpath, "html"),
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
print(" ")                       # todo: check folder structure here
        
def _initclass(rawS: str):
    """return class instance for rivt-string

    Args:
        rawstr (str): rivt-string

    Returns:
        class instance: string-type instance
    """
    sectS,strS = rawS.split("\n",1); _update(sectS)
    strL = strS.split("\n")
    ucalc = _rc_calc.ParseUTF(strL,_foldD,_setcmdD,_setsectD, rivtcalcD, exportS)
    return ucalc 

def _update(hdrS: str):
    """format section headings and settings 

    Args:
        hdrS (str): section heading line
    """
    global utfcalcS, _setsectD

    _rgx = r'\[\d\d\]'
    if re.search(_rgx,hdrS):        
        _setsectD["enum"] = 0               # equation number
        _setsectD["fnum"] = 0               # figure number
        _setsectD["tnum"] = 0               # table number
        nameS = _setsectD["sname"] = hdrS[hdrS.find("]") + 2:].strip()
        snumS = _setsectD["snum"] = hdrS[hdrS.find("[")+1:hdrS.find("]")]
        rnumS = str(_setsectD["rnum"])
        widthI = int(_setsectD["swidth"])
        headS = " " +  nameS + (rnumS + " - " +
                ("[" + snumS + "]")).rjust(widthI - len(nameS) - 1)
        bordrS = widthI * "="
        utfS = bordrS + "\n" + headS + "\n" + bordrS +"\n"
        print(utfS); utfcalcS += utfS

def _write_reST():
    pass

def write_utf():
    """write utf calc and reST-string files
    """
    global utfcalcS
    
    with open(_utffile, 'wb') as f1:
        f1.write(utfcalcS.encode("UTF-8"))
    print("utf calc written to file")
    _write_reSt():
    #with open(_rstfile, "wb") as f1:
    #    f1.write(rstcalcS.encode("UTF-8"))
    print("reST calc written to file")
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

def write_values():
    """ write value assignments to Python file
 
        File name: calc file name prepended with 'v'
        File path: scipts folder      
    """
    
    str1 =  ("""header string\n""")
    str1 = str1 + exportS
    with open(_expfile, 'w') as expF: expF.write(str1)

def R(rawS: str):
    """repository-string to utf calc-string
    
    Args:
        rawstrS (str): repository-string
    """
    global  utfcalcS,  _foldD, _setsectD, _setcmdD, rivtcalcD, exportS
    
    rcalc = _initclass(rawS)
    rcalcS, _setsectD = rcalc.r_utf()
    utfcalcS += rcalcS

def I(rawS: str):
    """insert-string to utf calc-string
    
    Args:
        rawstrS (str): insert-string
    """
    global utfcalcS,  _foldD, _setsectD, _setcmdD, rivtcalcD, exportS
    
    icalc = _initclass(rawS)
    icalcS, _setsectD, _setcmdD = icalc.i_utf()
    utfcalcS += icalcS

def V(rawS: str):
    """value-string to utf calc-string
    
    Args:
        rawstr (str): value-string
    """
    global utfcalcS,  _foldD, _setsectD, _setcmdD, rivtcalcD, exportS

    vcalc = _initclass(rawS)
    vcalcS, _setsectD, _setcmdD, rivtcalcD, exportS = vcalc.v_utf()
    utfcalcS += vcalcS

def T(rawS: str):
    """table-string to utf calc-string
     
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
