#! python
'''rivtcalc API  

    The API includes six functions. Input functions take a rivt-string as the
    single argument and write formatted utf8 calculations to the
    terminal. Ouput functions take a file of rivt-strings (calc) and write
    a formatted calculation file (doc) to files in utf8, pdf or html formats.

    Example calcs are here:

    
    and interactive calcs are here:


    Rivt-strings are written in rivt-markup which includes unicode,
    reStructuredText, rivt commands, rivt tags and Python code. Valid markup
    depends on the rivt function (R,I,V or T). Commands generally operate on
    files and start in the first column with ||. Tags are encapsulated with
    []_ and generally format a single line of text. Block tags are
    encapsulated with []__ and operate on indented blocks of text.

    Rivt functions ------------------------------------------------------------
    type       API      any text       string commands / arguments
    ======= ========== ========= ==============================================
    Repo    rc.R(rivt)    yes      search, info, keys, text, table, pdf
    Insert  rc.I(rivt)    yes      text, table, image, latex
    Values  rc.V(rivt)   yes(=)    =, config, value, data, func, I() commands
    Table   rc.T(rivt)    no       Python simple statements, I() commands  
    Skip    rc.S(rivt)    --       Skip rivt-string evaluation
    Write   rc.doc(args)  --       (type, style, title, page)

    Rivt tags -----------------------------------------------------------------
      format tag               description (user input)
    ===============  ==========================================================
    [nn]_ (abc def)       option section number and title / descriptor
    (description) [e]_    autoincrement, insert equation number and description
    (title) [t]_          autoincrement, insert table number and title   
    (caption) [f]_        autoincrement, insert figure number and caption   
    (sympy eq) [s]_       format sympy equation
    (latex eq) [x]_       format LaTeX equation
    (abc def) [r]_        right justify line of text
    (abc def) [c]_        center line of text
    [#]_                  autonumbered footnote      
    (abc def) [foot]_     footnote description
    [line]_               draw horizontal line
    [page]_               start new doc page
    [literal]__           literal text block (note double underscore)
    [latex]__             LaTeX text block (note double underscore)
    [link]_ http://abc.xyz label   where label is a clickable doc link

rivt Strings ------------------------------------------------------------------

    The first line of each rivt-string includes the string description, which
    may also be a section title via a tag. String input, by design, must be
    indented 4 spaces after the function call line to provide code structure
    and improve legibility.
    
    in the examples below, arguments in parenthesis are provided by the user.
    Either/or argumens are separated by semi-colons. Comments are in braces
    below the arguments.

from rivtcalc import rc_lib as rc
rc.R(
    """[01]_ Repository-string defines repository and report content
    
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
    """
)
rc.I(
    """[02]_ Insert-string defines static text, tables and images.  
    
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
    """
)
rc.V(
    """[02]_ Value-string defines active values and equations
    
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
    """
) 
rc.T(
    """[04]_ Table-string builds tables and plots and executes statements
    
     Table-strings may include any simple Python statement (single line),
     and any command or tag that does not include an = sign.
    """
)
'''
import os
import sys
import subprocess
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
import rivtcalc.rc_tex as _rc_tex

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

    # print(dir(__main__))
    _calcfileS = __main__.__file__

_cwdS = os.getcwd()
_cfull = Path(_calcfileS)  # calc file full path
_cfileS = _cfull.name  # calc file name
_cnameS = _cfileS.split(".py")[0]  # calc file basename
_cnumS = _cnameS[0:5]
_rivpath = Path("rivtcalc.rivt_lib.py").parent  # rivtcalc program path
_cpath = _cfull.parent.parent  # calc folder path
_ppath = _cfull.parent.parent.parent  # project folder path
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
    "calignS": "C",
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
_logfile = Path(_mpath / ".".join((_cnameS, "logging")))
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
logconsole = logging.StreamHandler()
logconsole.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)-8s %(message)s")
logconsole.setFormatter(formatter)
logging.getLogger("").addHandler(logconsole)
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
    rstcalc = _rc_tex.OutputRST(strL, _foldD, _setcmdD, _setsectD, rivtcalcD, exportS)
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
            + "   ?x?vspace{.2in}"
            + "   ?x?textbf{"
            + nameSS
            + "}"
            + "   ?x?hfill?x?textbf{SECTION "
            + snumSS
            + "}\n"
            + "   ?x?newline"
            + "   ?x?vspace{.05in}   {?x?color{black}?x?hrulefill}"
            + "\n\n"
        )
        rstcalcS += headS
    else:
        headS = (
            " "
            + nameSS
            + (cnumSS + " - " + ("[" + snumSS + "]")).rjust(widthI - len(nameSS) - 1)
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


def gen_utf8(cmdS: str, filepathS: str, calctitleS: str):
    """write utf-calc to calc subfolder"""

    global utfcalcS

    utfcalcS = """"""
    exec(cmdS, globals(), locals())

    utffile = Path(_cpath / _setsectD["fnumS"] / ".".join([_cnameS, "txt"]))
    if filepathS == "default":  # check file write location
        utfpthS = Path(utffile)
    else:
        utfpthS = Path(_cpath / filepathS / ".".join((_cnameS, "txt")))

    with open(utfpthS, "wb") as f1:
        f1.write(utfcalcS.encode("UTF-8"))
    print("INFO  utf calc written to calc folder", flush=True)
    print("INFO  program complete")

    os._exit(1)


def gen_pdf(texfileP):

    global rstcalcS, _rstflagB

    time.sleep(1)
    os.system("latexmk -c")
    time.sleep(1)
    dnameS = _cnameS.replace("c", "d", 1)
    dfolderS = str(_setsectD["fnumS"]).replace("c", "d", 1)
    docpdfP = Path(_dpath / dfolderS / ".".join([dnameS, "pdf"]))
    # clean temp files and generate pdf file

    mpath = _foldD["mpath"]
    pdfmkS = (
        "perl.exe d:/texlive/2020/texmf-dist/scripts/latexmk/latexmk.pl "
        + "-pdf -xelatex -quiet -f "
        + str(texfileP)
    )
    os.chdir(mpath)

    print("\nINFO  temporary Tex files deleted \n")
    os.system(pdfmkS)
    print("\nINFO  pdf file written: " + ".".join([_cnameS, "pdf"]))

    time.sleep(1)  # move pdf to doc folder
    os.chdir(mpath)
    pdfS = ".".join([_cnameS, "pdf"])
    shutil.move(pdfS, docpdfP)
    os.chdir(_dpath)
    print("INFO  pdf file moved to docs folder", flush=True)
    print("INFO  program complete")

    cfgP = Path(_dpath / "d0000" / "rc_cfg.txt")  # get pdf program
    with open(cfgP) as f2:
        cfgL = f2.readlines()
        cfg1S = cfgL[0].split("|")
        cfg2S = cfg1S[1].strip()
    cmdS = cfg2S + " " + str(docpdfP)
    print(cmdS)
    subprocess.run(cmdS)

    os._exit(1)


def gen_tex(doctypeS, stylefileS, calctitleS, startpageS):

    global rstcalcS, _rstflagB

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
    if stylefileS == "default":
        stylefileS = "pdf_style.sty"
    else:
        stylefileS == stylefileS.strip()
    style_path = Path(_dpath / "d0000" / stylefileS)
    print("INFO  style sheet: " + str(style_path))
    pythoncallS = "python "
    if sys.platform == "linux":
        pythoncallS = "python3 "
    elif sys.platform == "darwin":
        pythoncallS = "python3 "

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
    os.system(tex1S)
    print("INFO  tex file written : " + str(texfileP) + "\n")

    # fix escape sequences
    fnumS = _setsectD["fnumS"]
    with open(texfileP, "r", encoding="utf-8", errors="ignore") as texin:
        texf = texin.read()
    texf = texf.replace("?x?", """\\""")
    texf = texf.replace(
        """fancyhead[L]{\leftmark}""",
        """fancyhead[L]{\\normalsize  """ + calctitleS + "}",
    )
    texf = texf.replace("x*x*x", fnumS)
    texf = texf.replace("""\\begin{tabular}""", "%% ")
    texf = texf.replace("""\\end{tabular}""", "%% ")
    texf = texf.replace(
        """\\begin{document}""",
        """\\begin{document}\n\\setcounter{page}{""" + startpageS + "}\n",
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
    #     + """\\listoffigures"""
    # )

    with open(texfileP, "w", encoding="utf-8") as texout:
        texout.write(texf)

    if doctypeS == "pdf":
        gen_pdf(texfileP)

    os._exit(1)


def gen_html(stylefileS):

    global rstcalcS, _rstflagB
    pass


def gen_rst(cmdS, doctypeS, stylefileS, calctitleS, startpageS):

    global rstcalcS, _rstflagB

    _rstflagB = True
    rstcalcS = """"""
    exec(cmdS, globals(), locals())

    with open(_rstfile, "wb") as f1:
        f1.write(rstcalcS.encode("UTF-8"))
    print("INFO  rst calc written to tmp folder", flush=True)

    f1 = open(_rstfile, "r", encoding="utf-8", errors="ignore")
    rstcalcL = f1.readlines()
    f1.close()
    print("INFO  rst file read: " + str(_rstfile))

    if doctypeS == "tex" or doctypeS == "pdf":
        gen_tex(doctypeS, stylefileS, calctitleS, startpageS)
    elif doctypeS == "html":
        gen_html()
    else:
        print("INFO doc type not recognized")

    os._exit(1)


def gen_report():
    """[summary]"""
    pass


def doc(
    doctypeS="utf8",
    stylefileS="default",
    calctitleS="RivtCalc Calculation",
    startpageS="1",
    clrS="clr",
):

    """write rst-calc and values to files

    cnnnn_calc.txt file is written to calc subfolder
    cnnnn_values.csv file is written to calc subfolder
    .csv value file is written to calc subfolder
    .style files are read from d0000 folder (default)
    .rst calc file is written to tmp folder
    .tex file is written to tmp folder (default)

    """
    global utfcalcS, rstcalcS, _rstflagB

    f1 = open(_cfull, "r")
    utfcalcL = f1.readlines()
    f1.close()
    print("INFO calc file read: " + str(_cfull))

    indx = 0  # avoid recursion
    for iS in enumerate(utfcalcL):
        if "rc.doc" in iS[1]:
            indx = int(iS[0])
            break
    rstcalcL = utfcalcL = utfcalcL[0:indx] + utfcalcL[indx + 1 :]
    cmdS = "".join(utfcalcL)

    exprtfile = Path(_cpath / _setsectD["fnumS"] / ".".join([_cnameS, "csv"]))
    str1 = """header string\n"""  # write values file
    str1 = str1 + exportS
    with open(exprtfile, "w") as expF:
        expF.write(str1)
    print("INFO  values file written to calc folder", flush=True)

    if doctypeS == "utf8":
        gen_utf8(cmdS, stylefileS, calctitleS)

    elif doctypeS == "tex" or doctypeS == "pdf" or doctypeS == "html":
        if clrS == "clr":  # delete temp files
            mpathS = str(_foldD["mpath"])
            fileL = [
                Path(mpathS / ".".join([_cnameS, "pdf"])),
                Path(mpathS / ".".join([_cnameS, "html"])),
                Path(mpathS / ".".join([_cnameS, "rst"])),
                Path(mpathS / ".".join([_cnameS, "tex"])),
                Path(mpathS / ".".join([_cnameS, ".aux"])),
                Path(mpathS / ".".join([_cnameS, ".out"])),
                Path(mpathS / ".".join([_cnameS, ".fls"])),
                Path(mpathS / ".".join([_cnameS, ".fdb_latexmk"])),
            ]
            os.chdir(mpathS)
            tmpS = os.getcwd()
            if tmpS == mpathS:
                for f in fileL:
                    try:
                        os.remove(os.path.join(mpathS, f))
                    except:
                        pass
                time.sleep(1)
        print("INFO  files deleted from tmp folder", flush=True)
        gen_rst(cmdS, doctypeS, stylefileS, calctitleS, startpageS)

    elif doctypeS == "report":
        gen_report()

    else:
        pass
