#! python
"""rivtcalc API  

    The API includes string input and output functions. Input functions take
    rivt-markup strings (calcs) as arguments and write formatted utf
    calculations to the terminal (calcs). Ouput functions write formatted
    calculations (docs) to files in utf-8, pdf and html formats.
    
    Rivt-markup includes unicode and reStructuredText, commands, tags and
    Python code. The options depend on the rivt-string type (R,I,V or T).

    Input functions ------------------------------------------------------------
    type     API  text  tags     commands {comment}
    ======= ===== ===== =====  =================================================
    Report   R()   yes   no    head, code, keys, pdf
    Insert   I()   yes   yes   text, table, image
    Values   V()   yes   yes   =, config, value, data, func, +insert commands
    Table    T()   no    yes   Python (pandas) simple statements+icommands  
    Skip     S()   --     --   skip rivt-string; do not evaluate

    Output functions -----------------------------------------------------------
        name                   description
    =================  =========================================================
    write_utf()         write calc to utf8 doc file
    write_pdf()         write calc to pdf doc file
    write_html()        write calc to html doc file
    write_report()      combine pdf docs into pdf report file
    =================  =========================================================

    Commands and tags for each string type are described below. Commands
    generally operate on files and include processing parameters. Tags
    generally format single lines of text and do not have parameters. The first
    line of each rivt-string is a descriptor which may also be tagged as a
    section designator . By design, string input must be indented 4 spaces
    after the first descriptor line to improve legibility.

Input Syntax and commands ------------------------------------------------------

from rivtcalc import rc_lib as rc
rc.R('''[01] The report-string defines report and repository content
    
    Report-strings may include text. The first paragraph of the report-string
    in each calc specified in the ||search command (see below) becomes part of
    the README.rst file for the project. The ||head command specifies an
    optional calc title and date printed at the top of each page, and table of
    contents printed before the string text. Arguments not in parenthesis are
    literal. Parameter options are separated by semicolons. The toc argument
    generates a table of contents from the section tags.

    ||head | (calc title) | (date) | toc; notoc  

    The ||search command specifies a list of calc numbers that are searched
    against a master category list for terms to be included in the README. The
    calc number list is also used for the ||keys and ||code commands. Because
    the search command is execcuted at the project level it is usually included
    in the first calc in a project. The command overwrites existing README
    files.

    ||search | (calc num), (calc num), (calc num)

    The ||keys command is a list of keywords included in the README that
    describe the scope of the calc, with up to five terms per command.
    
    ||keys | (discipline), (object), (purpose), (assembly), (component)

    The ||code command identifies codes used in the calculation that are listed
    in the README and calc.

    ||code | (year) | (title)
    ||code | (year) | (title)

    The ||pdf command attaches existing pdf documents to the front
    or back of the calc doc. PDF files to attach files are stored in the
    docs/attach/ folder.
    
    ||pdf | front | (calccoverfile.pdf)         
    ||pdf | back | functions; docstrings
    ||pdf | back | (appendixfile.pdf) 
    ''')
rc.I('''The insert-string contains static text, tables and images.  
    
    Insert-strings include text, static equations and images. The equation tag
    auto increments and inserts the equation number. The x and s tags 

    latex equation  [e]_
    \gamma = \frac{5}{x+y} + 3  [x]_         
    
    sympy equation  [e]_
    x = 32 + (y/2)  [s]_            
    
    ||text | file.txt | literal; indent {}  
    
    table title  [t]_
    ||table | f.csv | 60,c {width, align} | title {line 1} | 2,1,4 {include cols} 

    ||image | f.png {image file} | 1. {scale}
    figure caption [f]_

    ||image | f1.png, f2.jpg | 1.,0.5
    first figure caption (side by side)  [f]_
    second figure caption  [f]_

    Python | http://wwww.python.org [link]_ 
    ''')
rc.V('''[02] The value-string defines active values and equations
    
    Value-strings include text (excluding equal signs). Lines with equal signs
    define equations and assignments that are numerically evaluated.
    
    Set value parameters where sub means to render equations with substited
    values and the number pair specifies decimals in the result and terms.
    ||config | sub; nosub | 2,2
    
    x1 = 10.1    | unit, alt unit | description || {save if trailing ||}
    y1 = 12.1    | unit, alt unit | description  

    Import values from a csv file, starting with the second row.  The first row
    is a descriptive heading.   
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
    save an equation result to the values file [e]_
    y1 = v1 / 4   | unit, alt unit ||         

    ||func | func_file.py | func_call | var_name {import function from file}

    a table title [t]_
    ||table | x.csv | 60    
    
    figure caption [f]_
    ||image | x.png | 1.
    ''') 
rc.T('''The table-string defines tables and plots with simple Python statements
    
     Table-strings may include any simple Python statement (single line),
     insert-commands or tags.
    ''')

    Tags -----------------------------------------------------------------------
       tag               description
    ===============  ===========================================================
    [nn]_ abc def       first line - descriptor section number and title
    description [e]_    autoincrement and insert equation number and description
    title [t]_          autoincrement and insert table number and title   
    caption [f]_        autoincrement and insert figure number and caption   
    [#]_                            autonumbered footnote      
    abc def [foot]_                 footnote description
    s = b\2 [s]_                    format sympy equation
    \a = c*2 [x]_                   format LaTeX equation
    abc def [r]_                    right justify text line
    abc def [c]_                    center text line
    [literal]_                      literal text block
    [line]_                         draw horizontal line
    [page]_                         new doc page
    label | http://abc  [link]_     url link
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
_cnameS    = _cfileS.split(".py")[0]                 # calc file basename
_rivpath  = Path("rivtcalc.rivt_lib.py").parent      # rivt program path
_ppath    = _cfull.parent.parent                     # project folder path
_cpath    = _cfull.parent                            # calc folder path
_tpath    = Path(_ppath/"tmp")                       # tmp folder path
_dpath    = Path(_ppath/"docs")                      # doc folder path
_rpath    = Path(_dpath/"report")                    # report folder path
_dname    = "d"+_cnameS[1:]                          # doc file basename
_utffile  = Path(_cpath/".".join((_dname, "txt")))   # utf output
_rstfile  = Path(_ppath/".".join((_dname, "rst")))   # rst output
_expfile  = Path(_cpath /"data"/"".join(_cfileS))    # export file

# global variables; folders, sections, commmands
utfcalcS = """"""                                    # utf calc string
rstcalcS = """"""                                    # reST calc string
exportS  = """"""                                    # values export string
rivtcalcD = {}                                       # values dictonary
_rstflagB = False                                    # flag for reST generation
# folder paths
_foldD = {
"efile": _expfile,   
"ppath": _ppath,
"dpath": _dpath,
"rpath": _rpath,
"cpath": Path(_cfull).parent,
"mpath": Path(_ppath, "tmp"),
"spath": Path(_cpath, "scripts"),
"kpath": Path(_cpath, "sketches"),
"tpath": Path(_cpath, "data"),
"xpath": Path(_cpath, "text"),
"hpath": Path(_dpath, "html"),
"apath": Path(_rpath, "attach")}
# section settings
_setsectD = {"cnumS":_cnameS[1:5],"dnumS":_cnameS[1:3],"sdnumS":_cnameS[3:5],
            "snameS":"","snumS":"","swidthI":80,
            "enumI":0,"tnumI":0, "fnumI":0, "ftqueL":deque([1])}
# command settings
_setcmdD = {"cwidthI":30, "calignS":"s", "titleS":"notitle", "writeS":"table",
            "scale1F": 1., "scale2F": 1., "trmrI": 2, "trmtI": 2,
            "subB": False, "saveB": False}
# temp files
_rbak = Path(_foldD["mpath"] / ".".join((_cnameS, "bak")))
_logfile = Path(_foldD["mpath"] / ".".join((_cnameS, "log")))
_rstfile = Path(_foldD["mpath"] / ".".join((_cnameS, "rst"))) 
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
logging.info(f"""calc: {_rshortP}""" )
logging.info(f"""backup: {_bshortP}""")
logging.info(f"""logging: {_lshortP}""")
print(" ")                       # todo: check folder structure here

def _init_utf(rawS: str):
    """return rivt-string utf class instance

    Args:
        rawstr (str): rivt-string

    Returns:
        class instance: utf string-type instance
    """
    sectS,strS = rawS.split("\n",1); _section(sectS)
    strL = strS.split("\n")
    ucalc = _rc_calc.WriteUTF(strL,_foldD,_setcmdD,_setsectD, rivtcalcD, exportS)
    return ucalc 

def _init_rst(rawS: str):
    """return rivt-string reST class

    Args:
        rawstr (str): rivt-string

    Returns:
        class instance: reST string-type instance
    """
    sectS,strS = rawS.split("\n",1); _section(sectS)
    strL = strS.split("\n")
    rstcalc = _rc_calc.WriteRST(strL,_foldD,_setcmdD,_setsectD, rivtcalcD, exportS)
    return rstcalc 

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

def R(rawS: str):
    """repository-string to utf-string
    
    Args:
        rawstrS (str): repository-string
    """
    global  utfcalcS, _rstflagB, _foldD, _setsectD, _setcmdD, rivtcalcD
    
    if _rstflagB:
        rcalc = _init_rst(rawS)
        rcalcS, _setsectD = rcalc.r_rst()
        rstcalcS += rcalcS
    else:
        rcalc = _init_utf(rawS)
        rcalcS, _setsectD = rcalc.r_utf()
        utfcalcS += rcalcS

def I(rawS: str):
    """insert-string to utf-string
    
    Args:
        rawstrS (str): insert-string
    """
    global utfcalcS, _rstflagB, _foldD, _setsectD, _setcmdD, rivtcalcD
    
    if _rstflagB:
        rcalc = _init_rst(rawS)
        rcalcS, _setsectD = rcalc.r_rst()
        rstcalcS += rcalcS
    else:
        icalc = _init_utf(rawS)
        icalcS, _setsectD, _setcmdD = icalc.i_utf()
        utfcalcS += icalcS

def V(rawS: str):
    """value-string to utf-string
    
    Args:
        rawstr (str): value-string
    """
    global utfcalcS, _rstflagB, _foldD, _setsectD, _setcmdD, rivtcalcD, exportS

    if _rstflagB:
        rcalc = _init_rst(rawS)
        rcalcS, _setsectD = rcalc.r_rst()
        rstcalcS += rcalcS
    else:
        vcalc = _init_utf(rawS)
        vcalcS, _setsectD, _setcmdD, rivtcalcD, exportS = vcalc.v_utf()
        utfcalcS += vcalcS

def T(rawS: str):
    """table-string to utf-string
     
     Args:
        rawstr (str): table-string   
    """
    global utfcalcS, _rstflagB, _foldD, _setsectD, _setcmdD, rivtcalcD

    if _rstflagB:
        rcalc = _init_rst(rawS)
        rcalcS, _setsectD = rcalc.r_rst()
        rstcalcS += rcalcS
    else:
        tcalc = _init_utf(rawS)
        tcalcS, _setsectD, _setcmdD, rivtcalcD = tcalc.t_utf()
        utfcalcS += tcalcS

def S(rawS: str):
    """skip string
     
     Args:
        rawstr (str): any string to exclude
    """
    pass

def write_values():
    """ write value assignments to csv file
 
        File name: calc file name prepended with 'v'
        File path: data folder      
    """
    
    str1 =  ("""header string\n""")
    str1 = str1 + exportS
    with open(_expfile, 'w') as expF: expF.write(str1)

def write_utf():
    """write utf-calc output to file
    
    file is written to calcs folder
    """
    global utfcalcS, _rstflagB

    utfcalcS = """"""
    f1 = open(_cfull, "r"); utfcalcL = f1.readlines(); f1.close()
    print("calc file read: " + str(_cfull))
    indx = 0
    for iS in enumerate(utfcalcL):                      
        if "write_utf" in iS[1]: 
            indx = int(iS[0]); break
    utfcalcL = utfcalcL[0:indx]+utfcalcL[indx+1:]     # filter write function
    cmdS = ''.join(utfcalcL); exec(cmdS, globals(), locals())
    with open(_utffile, "wb") as f1: f1.write(utfcalcS.encode("UTF-8"))
    print("INFO  utf calc written to calc folder", flush=True)
    print("INFO  program complete")
    os._exit(1)

def write_pdffile():
    """read .rst file from tmp folder and write .pdf to docs folder 

    .rst file is converted to tex file as an intermediate step
    """
    f1 = open(_rstfile, "r"); rstcalcL = f1.readlines(); f1.close()
    print("INFO  rst file read: " + str(_rstfile))
    mpath = _foldD{mpath}
    pdffiles = {
        "cpdf":  Path(mpath/".".join(_cnameS, "pdf")),
        "chtml":  Path(mpath/".".join(_cnameS, "html")),
        "trst":  Path(tpath/".".join(_cnameS, "rst")),    
        "ttex1":  Path(tpath/".".join(_cnameS, "tex")),
        "auxfile": Path(tpath/".".join(_cnameS, ".aux")),
        "outfile":  Path(tpath/".".join(_cnameS, ".out")),
        "texmak2":  Path(tpath/".".join(_cnameS, ".fls")),
        "texmak3":  Path(tpath/".".join(_cnameS, ".fdb_latexmk"))
        }
        
        # use search to find path to standard style or use local
        fixstylepath = self.stylepathpdf.replace('\\', '/')
        try:
            pypath = os.path.dirname(sys.executable)
            rstexec = os.path.join(pypath,"Scripts","rst2latex.py")
            with open(rstexec) as f1: f1.close()
            pythoncall = 'python '
            #print("< rst2latex path 1> " + rstexec)
        except:
            try:
                pypath = os.path.dirname(sys.executable)
                rstexec = os.path.join(pypath,"rst2latex.py")
                with open(rstexec) as f1:
                    f1.close()
                pythoncall = 'python '
                #print("< rst2latex path 2> " + rstexec)
            except:
                rstexec = "/usr/local/bin/rst2latex.py"
                pythoncall = 'python '
                #print("< rst2latex path 3> " + rstexec)
        
        
        tex1 = "".join([pythoncall, rstexec
                        ,
                        " --documentclass=report ",
                        " --documentoptions=12pt,notitle,letterpaper",
                        " --stylesheet=",
                        fixstylepath + " ", self.rfile + " ", self.texfile2])
        self.el.logwrite("tex call:\n" + tex1, self.vbos)
        try:
            os.system(tex1)
            self.el.logwrite("< TeX file written >", self.vbos)
        except:
            print()
            self.el.logwrite("< error in docutils call >", self.vbos)
        self.mod_tex(self.texfile2)
        with open(tfile, 'r') as texin:
            texf = texin.read()
        texf = texf.replace("""inputenc""", """ """)
        texf = texf.replace("aaxbb ", """\\hfill""")
        texf = texf.replace("""\\begin{document}""",
                            """\\renewcommand{\contentsname}{"""+
                            self.calctitle + "}\n"+
                            """\\begin{document}"""+"\n"+
                            """\\makeatletter"""+
                            """\\renewcommand\@dotsep{10000}"""+
                            """\\makeatother"""+
                            """\\tableofcontents"""+
                            """\\listoftables"""+
                            """\\listoffigures""")    
        with open (tfile, 'w') as texout:
            print(texf, file=texout)
        os.chdir(self.xpath)
        if os.path.isfile(os.path.join(self.ppath,self.pdffile)):
            os.remove(os.path.join(self.ppath,self.pdffile))
        pdf1 ='latexmk -xelatex -quiet -f '+os.path.join(self.xpath,self.texfile)
        #print("pdf call:  ", pdf1)
        self.el.logwrite("< PDF calc written >", self.vbos)    
        os.system(pdf1)
        pdfname = self.pdffile
        pdfname = list(pdfname)
        pdfname[0]='m'
        pdfname2 = "".join(pdfname)
        pdfftemp = os.path.join(self.xpath, pdfname2)
        pdffnew = os.path.join(self.cpath, self.pdffile)
        try: os.remove(pdffnew)
        except: pass
        try: os.rename(pdfftemp, pdffnew)
        except: self.el.logwrite("< PDF calc not moved from temp >", 1)
        tocname2 = pdfname2.replace('.pdf','.toc')
        toctemp = os.path.join(self.xpath, tocname2)
        tocnew = os.path.join(self.rpath, tocname2)
        try: shutil.copyfile(toctemp, tocnew)
        except: self.el.logwrite("< TOC not moved from temp >", 1)
    print("INFO  pdf doc written to docs folder", flush=True)    
    print("INFO  program complete")
    os._exit(1)

def write_pdf(stylefileS):
    """write calc output to .rst file in tmp folder

    """
    global rstcalcS, _rstflagB

    _rstflagB = True
    rstcalcS = """"""
    f1 = open(_cfull, "r"); rstcalcL = f1.readlines(); f1.close()
    print("calc file read: " + str(_cfull))
    indx = 0
    for iS in enumerate(rstcalcL):                      
        if "write_pdf" in iS[1]: 
            indx = int(iS[0]); break
    rstcalcL = rstcalcL[0:indx]+rstcalcL[indx+1:]     # filter write function
    cmdS = ''.join(rstcalcL); exec(cmdS, globals(), locals())
    with open(_rstfile, "wb") as f1: f1.write(rstcalcS.encode("UTF-8"))
    print("INFO  rst calc written to tmp folder", flush=True)
    write_pdffile(stylefileS)

def write_html():
    """[summary]
    """
    with open(_txtfile, "wb") as f1:
        f1.write(utfcalc.encode("UTF-8"))

def write_report():
    """[summary]
    """
    pass