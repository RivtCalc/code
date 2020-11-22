#! python
"""rivtcalc API  

    The API includes eight functions. Input functions take a rivt-markup string
    (calc) as the single function argument and write formatted utf calculations
    to the terminal. Ouput functions take a file of rivt-strings (calcs) and
    write formatted calculations to files in utf-8, pdf and html formats
    (docs).

    Example calcs are here:

    
    and interactive calcs are here:


    Rivt-strings are written in rivt-markup which includes unicode,
    reStructuredText, rivt commands, rivt tags and Python code. The options
    depend on the rivt function (R,I,V or T). Commands include processing
    parameters generally operate on files, and start in the first column with
    ||. Tags are encapsulated with []_ and generally operate on a single line
    of text. Block tags are encapsulated with []__ and operate on indented
    blocks.

    Rivt function - Input -----------------------------------------------------
    type     API  any text       commands 
    ======= ===== ========= ===================================================
    Repo     R()    yes       head, search, info, keys, text, table, pdf
    Insert   I()    yes       text, table, image, latex
    Values   V()    no        =, config, value, data, func, + insert commands
    Table    T()    no        Python simple statements, + insert commands  
    Skip     S()    --        Skip rivt-string evaluation


    Rivt tags -----------------------------------------------------------------
       tag                                 description
    ===============  ==========================================================
    [nn]_ (abc def)       string descriptor section number and title
    (description) [e]_    autoincrement and insert equation number and description
    (title) [t]_          autoincrement and insert table number and title   
    (caption) [f]_        autoincrement and insert figure number and caption   
    [#]_                  autonumbered footnote      
    (abc def) [foot]_     footnote description
    (s = (b+2)/3) [s]_    format sympy equation
    (\a = c*2^2) [x]_     format LaTeX equation
    (abc def) [r]_        right justify text line
    (abc def) [c]_        center text line
    [line]_               draw horizontal line
    [page]_               new doc page
    (label)|(http://abc.xyz) [link]_    label_ is a clickable link in docs
    [literal]__           literal text block
    [latex]__             LaTeX text block


    Rivt function - Output ----------------------------------------------------
        name                          description
    ============================ ==============================================
    write_text()                    write calc to utf8 doc file
    write_doc(type, style)         write calc to pdf or html doc file
    write_report()                 combine pdf docs into pdf report file
    ============================ ==============================================
    
    The first line of each rivt-string includes the string function name and
    description, which may be tagged as a section. String input, by design,
    must be indented 4 spaces after the function call line to provide code
    structure and improve legibility.
    
    in the examples below, arguments in parenthesis are provided by the user.
    Either/or argumens are separated by semi-colons. Comments are in braces
    below the arguments.

Input Syntax and commands -----------------------------------------------------

from rivtcalc import rc_lib as rc
rc.R('''[01]_ The repository-string defines repository and report content
    
    Repository-strings may include arbitrary text. The first paragraph of the
    calcs specified in the ||search command (see below) becomes part of the
    README.rst file for the project. The README is used in various repository
    search functions (i.e. Github). Arguments to commands in parenthesis are
    used provided. Otherwise they are literal. Parameter options are separated
    by semicolons.
    
    || search | (calc num), (calc num), (calc num) ...

    The || search command generates a README and specifies a list of calc
    numbers that are searched against a master category list for terms to be
    included in the README. Because the search command is executed at the
    project level across multiple calcs, it is usually included in the first
    project calc. The command overwrites any existing README file.

    The calc number list is also used for the ||keys command. The ||keys
    command is a list of keywords included in the README that describe the
    scope of the calc, with up to six calcs per command.
    
    || keys | (discipline), (object), (purpose), (assembly), (component)

    The || info command is similar to the the ||table and ||text commands with
    differences in file location and use. See those commands for details.
    ||info files are used for project specific information (clients, addresses,
    etc) and are read from the docs/info folder which is not shared. Also, the
    info command is only written to docs, and not to utf-calcs. This keeps
    confidential project information separated from the shareable calc
    information contained in the calcs folder. || info tables do not contain
    titles and should not be numbered.

    || info | (project.txt) | literal; indent
    || info | (project.csv or .xlsx) | ([1,2,3] or [:]
    
    The || pdf command attaches existing pdf documents, stored in the
    docs/attach folder, to the front or back  of the calc doc. The *functions*
    or *docstrings* arguments determine whether the complete function code or
    just the docstrings of functions used with the ||func commmand are appended
    to the calc. The title is written to a cover page that can be referred to
    in the calcs.
    
    || pdf | front | (calccoverfile.pdf) | (title)        
    || pdf | back | functions; docstrings |(title)
    || pdf | back | (appendixfile.pdf) | (title)
    ''')
rc.I('''The insert-string contains static text, tables and images.  
    
    Insert-strings include text, static equations and images. The equation tag
    [e]_ auto-increments the equation labels. The [s]_ and [x]_  tags format 
    LaTeX and sympy equations respectively.

    latex equation  [e]_
    \gamma = \frac{5}{x+y} + 3  [x]_         
    
    sympy equation  [e]_
    x = 32 + (y/2)  [s]_            
    
    || text | (file.txt) | literal; indent 

    || latex | (file.txt) 
    
    table title  [t]_
    || table | (file.csv or .xlst) | (60,c) | title; notitle | (2,1,4; :) 
    
    || image | (file.png) | (50) 
                        {scale as percent of page wdith}
    figure caption [f]_ 
    
    Insert two images side by side using the following:
    || image | f1.png, f2.jpg | (45,45) 
    [a] first figure caption  [f]_
    [b] second figure caption  [f]_

    (label) | http://wwww.someurl.suffix [link]_ 
    ''')
rc.V('''[02]_ The value-string defines active values and equations
    
    Value-strings include text (excluding equal signs). Lines with equal signs
    define equations and assignments that are numerically evaluated.
    
    Set value parameters where sub means to render equations with substited
    values and the number pair specifies decimals in the result and terms.
    ||config | sub; nosub | 2,2
    
    Assign values to variables.  A blank line ends the value block and a table
    is output.

    (x1 = 10.1)    | (unit, alt unit | description 
    (y1 = 12.1)    | (unit, alt unit | description ||
                            {save to value file if trailing ||} 


    || values | (file.csv or .xlxs)

    Import values from a csv or xlxs file, starting with the second row. The
    first row is a descriptive heading. For a value file the csv or xlsx file
    must have the structure:
    
    [literal]__
        variable name, value, primary unit, secondary unit, description
    
    
    || data | file.csv | [1:4] {rows to import} 

    Import a list of values from rows of a csv or xlsx file. For a data file
    the csv file must have the structure:
    [literal]__
        variable name, value1, value2, value3, ....

    
    an equation [e]_
    v1 = x + 4*M  | unit, alt unit
    save an equation result to the values file by appending double bars [e]_
    y1 = v1 / 4   | unit, alt unit ||         

    Functions may be defined in a table-string or imported from a file.
    || func | (function_file.py) | (function_name) | 

    A table title [t]_
    || table | x.csv | 60    
    
    || image | x.png | 50
    A figure caption [f]_
    ''') 
rc.T('''The table-string defines active tables and plots that use simple Python statements
    
     Table-strings may include any simple Python statement (single line),
     and all commands or tags, except value assignments with an = sign.  It may
     not include 
    ''')
"""
import os
import sys
import time
import textwrap
import logging
import warnings
import re
import importlib.util
import shutil
import numpy as np
from pathlib import Path
from collections import deque
from typing import List, Set, Dict, Tuple, Optional
from contextlib import suppress
from rivtcalc.rc_unit import *
import rivtcalc.rc_calc as _rc_calc
import rivtcalc.rc_doc as _rc_doc

# import rivt.rivt_reprt as _reprt
# import rivt.rivt_chk as _rchk

try:
    # print("argv1", sys.argv[1])
    _calcfileS = sys.argv[1]
except:
    # print("argv0", sys.argv[0])
    _calcfileS = sys.argv[0]
if ".py" not in _calcfileS:
    import __main__

    _calcfileS = __main__.__file__

_cwdS = os.getcwd()
_cfull = Path(_calcfileS)  # calc file full path
_cfileS = _cfull.name  # calc file name
_cnameS = _cfileS.split(".py")[0]  # calc file basename
_cnumS = _cnameS[0:5]
_rivpath = Path("rivtcalc.rivt_lib.py").parent  # rivtcalc program path
_ppath = _cfull.parent.parent  # project folder path
_cpath = _cfull.parent  # calc folder path
_mpath = Path(_ppath / "tmp")  # tmp folder path
_dpath = Path(_ppath / "docs")  # doc folder path
_rstfile = Path(_mpath / ".".join((_cnameS, "rst")))  # rst output
_pdffile = Path(_dpath / ".".join((_cnameS, "pdf")))  # pdf output

# global variables and dictionaries
utfcalcS = """"""  # utf calc string
rstcalcS = """"""  # reST calc string
exportS = """"""  # values string exports
rivtcalcD = {}  # values dictonary
_rstflagB = False  # reST generation flag
# folder paths
_foldD = {
    "ppath": _ppath,
    "docpath": _dpath,
    "cpath": Path(_ppath, "calcs"),
    "dpath": Path(_ppath, "docs"),
    "mpath": Path(_ppath, "tmp"),
    "spath": Path(_cpath, "scripts"),
    "kpath": Path(_cpath, "scripts", "sketches"),
    "hpath": Path(_dpath, "html"),
    "ipath": Path(_dpath, "info"),
}
# section settings
_setsectD = {
    "fnumS": _cnameS[0:5],
    "cnumS": _cnameS[1:5],
    "dnumS": _cnameS[1:3],
    "sdnumS": _cnameS[3:5],
    "snameS": "",
    "snumS": "",
    "swidthI": 80,
    "enumI": 0,
    "tnumI": 0,
    "fnumI": 0,
    "ftqueL": deque([1]),
}
# command settings
_setcmdD = {
    "cwidthI": 30,
    "calignS": "s",
    "writeS": "table",
    "scale1F": 1.0,
    "scale2F": 1.0,
    "trmrI": 2,
    "trmtI": 2,
    "subB": False,
    "saveB": False,
}

# temp files
_rbak = Path(_mpath / ".".join((_cnameS, "bak")))
_logfile = Path(_mpath / ".".join((_cnameS, "log")))
_rstfile = Path(_mpath / ".".join((_cnameS, "rst")))
# logs and checks
with open(_cfull, "r") as f2:
    calcbak = f2.read()
with open(_rbak, "w") as f3:
    f3.write(calcbak)  # write backup
warnings.filterwarnings("ignore")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename=_logfile,
    filemode="w",
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)-8s %(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)
_rshortP = Path(*Path(_cfull).parts[-3:])
_bshortP = Path(*Path(_rbak).parts[-4:])
_lshortP = Path(*Path(_logfile).parts[-4:])
logging.info(f"""calc: {_rshortP}""")
logging.info(f"""backup: {_bshortP}""")
logging.info(f"""logging: {_lshortP}""")
print(" ")
# todo: check folder structure
# todo: check for units file in c0000, supplement default units


def _init_utf(rawS: str):
    """return rivt-string utf class instance

    Args:
        rawS (str): rivt-string

    Returns:
        class instance: utf string-type instance
    """
    sectS, strS = rawS.split("\n", 1)
    _section(sectS)
    strL = strS.split("\n")
    ucalc = _rc_calc.OutputUTF(strL, _foldD, _setcmdD, _setsectD, rivtcalcD, exportS)
    return ucalc


def _init_rst(rawS: str):
    """return rivt-string reST class

    Args:
        rawstr (str): rivt-string

    Returns:
        class instance: reST string-type instance
    """
    sectS, strS = rawS.split("\n", 1)
    _section(sectS)
    strL = strS.split("\n")
    rstcalc = _rc_doc.OutputRST(strL, _foldD, _setcmdD, _setsectD, rivtcalcD, exportS)
    return rstcalc


def _section(hdrS: str):
    """format section headings and settings

    Args:
        hdrS (str): section heading line
    """
    global utfcalcS, _setsectD, rstcalcS

    _rgx = r"\[\d\d\]"
    if re.search(_rgx, hdrS):
        nameSS = _setsectD["snameS"] = hdrS[hdrS.find("]") + 2 :].strip()
        snumSS = _setsectD["snumS"] = hdrS[hdrS.find("[") + 1 : hdrS.find("]")]
        cnumSS = str(_setsectD["cnumS"])
        widthI = int(_setsectD["swidthI"])
    if _rstflagB:
        # draw horizontal line
        headS = (
            ".. raw:: latex"
            + "\n\n"
            + "   ?x?textbf{"
            + nameSS
            + "}"
            + "   ?x?hfill?x?textbf{Section "
            + snumSS
            + "}\n"
            + "   ?x?newline"
            + "   ?x?vspace{-.15}   {?x?color{black}?x?hrulefill}"
            + "\n"
        )
        rstcalcS += headS
    else:
        headS = (
            " "
            + nameSS
            + (cnumSS + " - " + ("[" + snumSS + "]")).rjust(widthI - len(nameS) - 1)
        )
        bordrS = widthI * "_"
        utfS = "\n" + bordrS + "\n\n" + headS + "\n" + bordrS + "\n"
        print(utfS)
        utfcalcS += utfS


def R(rawS: str):
    """repository-string to utf-string

    Args:
        rawstrS (str): repository-string
    """
    global utfcalcS, rstcalcS, _rstflagB, _foldD, _setsectD, _setcmdD, rivtcalcD

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
    global utfcalcS, rstcalcS, _rstflagB, _foldD, _setsectD, _setcmdD, rivtcalcD

    if _rstflagB:
        rcalc = _init_rst(rawS)
        rcalcS, _setsectD, _setcmdD = rcalc.i_rst()
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
    global utfcalcS, rstcalcS, _rstflagB, _foldD, _setsectD, _setcmdD, rivtcalcD, exportS

    if _rstflagB:
        rcalc = _init_rst(rawS)
        rcalcS, _setsectD, _setcmdD, rivtcalcD, exportS = rcalc.v_rst()
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
    global utfcalcS, rstcalcS, _rstflagB, _foldD, _setsectD, _setcmdD, rivtcalcD

    if _rstflagB:
        rcalc = _init_rst(rawS)
        rcalcS, _setsectD = rcalc.t_rst()
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


def write_text(filepathS: str):
    """write utf-calc and values to files

    .txt calc file is written to calc subfolder (default)
    .csv value file is written to calc subfolder
    """

    global utfcalcS, _rstflagB

    utfcalcS = """"""
    f1 = open(_cfull, "r")
    utfcalcL = f1.readlines()
    f1.close()
    print("INFO calc file read: " + str(_cfull))
    indx = 0
    for iS in enumerate(utfcalcL):
        if "write_text" in iS[1]:
            indx = int(iS[0])
            break
    utfcalcL = utfcalcL[0:indx] + utfcalcL[indx + 1 :]  # avoid recursion
    cmdS = "".join(utfcalcL)
    exec(cmdS, globals(), locals())

    utffile = Path(_cpath / _setsectD("fnumS") / ".".join((_cnameS, "txt")))
    exprtfile = Path(_cpath / _setsectD("fnumS") / ".".join(_cnameS, "csv"))

    str1 = """header string\n"""  # write values file
    str1 = str1 + exportS
    with open(exprtfile, "w") as expF:
        expF.write(str1)
    print("INFO  values file written to calc folder", flush=True)

    if filepathS == "defaultpath":  # check calc file write location
        utfpthS = Path(utffile)
    else:
        utfpthS = Path(_cpath / filepathS / ".".join((_cnameS, "txt")))

    with open(utfpthS, "wb") as f1:
        f1.write(utfcalcS.encode("UTF-8"))
    print("INFO  utf calc written to calc folder", flush=True)
    print("INFO  program complete")

    os._exit(1)


def _write_pdf(stylefileS: str, calctitleS: str):
    """read .rst file, write .tex and .pdf to tmp folder

    move .pdf file to doc subfolder

    """


def _write_html(stylefileS):
    pass


def write_pdf(doctypeS: str, stylefileS: str, calctitleS: str):
    """write rst-calc and values to files

    .csv value file is written to calc subfolder
    .rst calc file is written to tmp folder
    .style file is read from rivtcalc library (default)
    .tex file is written to tmp folder (default)

    """
    global rstcalcS, _rstflagB

    _rstflagB = True
    rstcalcS = """"""
    f1 = open(_cfull, "r")
    rstcalcL = f1.readlines()
    f1.close()
    print("INFO calc file read: " + str(_cfull))

    indx = 0
    for iS in enumerate(rstcalcL):  # find write_doc
        if "write_doc" in iS[1]:
            indx = int(iS[0])
            break
    rstcalcL = rstcalcL[0:indx] + rstcalcL[indx + 1 :]  # now skip write_doc
    cmdS = "".join(rstcalcL)
    exec(cmdS, globals(), locals())
    with open(_rstfile, "wb") as f1:
        f1.write(rstcalcS.encode("UTF-8"))
    print("INFO  rst calc written to tmp folder", flush=True)

    f1 = open(_rstfile, "r", encoding="utf-8", errors="ignore")
    rstcalcL = f1.readlines()
    f1.close()
    print("INFO  rst file read: " + str(_rstfile))

    mpath = _foldD["mpath"]
    pdfD = {
        "cpdfP": Path(mpath / ".".join([_cnameS, "pdf"])),
        "chtml": Path(mpath / ".".join([_cnameS, "html"])),
        "trst": Path(mpath / ".".join([_cnameS, "rst"])),
        "ttex1": Path(mpath / ".".join([_cnameS, "tex"])),
        "auxfile": Path(mpath / ".".join([_cnameS, ".aux"])),
        "outfile": Path(mpath / ".".join([_cnameS, ".out"])),
        "texmak2": Path(mpath / ".".join([_cnameS, ".fls"])),
        "texmak3": Path(mpath / ".".join([_cnameS, ".fdb_latexmk"])),
    }

    style_path = Path(_dpath / "d0000" / stylefileS)
    print("INFO  style sheet: " + str(style_path))
    pythoncallS = "python "
    if sys.platform == "linux":
        pythoncallS = "python3 "
    elif sys.platform == "darwin":
        pythoncallS = "python3 "

    # generate tex file
    rst2xeP = Path(rivpath / "scripts" / "rst2xetex.py")
    texfileP = pdfD["ttex1"]
    tex1S = "".join(
        [
            pythoncallS,
            str(rst2xeP),
            " --embed-stylesheet ",
            " --documentclass=report ",
            " --documentoptions=12pt,notitle,letterpaper ",
            " --stylesheet=",
            str(style_path) + " ",
            str(_rstfile) + " ",
            str(texfileP),
        ]
    )
    os.chdir(mpath)
    # print(tex1S)
    os.system(tex1S)
    print("INFO  tex file written : " + str(texfileP) + "\n")

    # fix escape sequences
    with open(texfileP, "r", encoding="utf-8", errors="ignore") as texin:
        texf = texin.read()
        texf = texf.replace("?x?", """\\""")
        texf = texf.replace(
            """fancyhead[L]{\leftmark}""",
            """fancyhead[L]{\\normalsize  """ + calctitleS + "}",
        )

    # texf = texf.replace(
    #     """\\begin{document}""",
    #     """\\renewcommand{\contentsname}{"""
    #     + self.calctitle
    #     + "}\n"
    #     + """\\begin{document}"""
    #     + "\n"
    #     + """\\makeatletter"""
    #     + """\\renewcommand\@dotsep{10000}"""
    #     + """\\makeatother"""
    #     + """\\tableofcontents"""
    #     + """\\listoftables"""
    #     + """\\listoffigures""",
    # )

    with open(texfileP, "w") as texout:
        texout.write(texf)

    if doctypeS == "pdf":  # generate pdf
        dnameS = _cnameS.replace("c", "d", 1)
        dfolderS = str(_setsectD["fnumS"]).replace("c", "d", 1)
        docpdfP = Path(_dpath / dfolderS / ".".join([dnameS, "pdf"]))
        # clean temp files and generate pdf file
        pdfmkS = "latexmk -pdf -xelatex -quiet -f " + str(texfileP)
        os.chdir(mpath)
        os.system("latexmk -c")
        print("\nINFO  temporary Tex files deleted \n")
        os.system(pdfmkS)
        print("\nINFO  pdf file written: " + ".".join([_cnameS, "pdf"]))

        # move pdf to specified folder
        os.chdir(mpath)
        pdfS = ".".join([_cnameS, "pdf"])
        shutil.move(pdfS, docpdfP)
        os.chdir(_dpath)
        print("INFO  pdf file moved to docs folder", flush=True)
        print("INFO  program complete")
    os._exit(1)


def write_report():
    """[summary]"""
    pass
