#! python
"""rivet_lib
    Processes the r-i-v-e-t design file to a calc and sets files and paths

    The language includes five types of f-strings where each type of string is
    evaluated by a function. The first line of each f-string can be a settings
    string.

    r__() : string of python code 
    i__() : string inserts text and images
    v__() : string defines calculation values
    e__() : string defines calculation equations
    t__() : string inserts tables and plots
    
"""

import sys
import os
import inspect
import __main__ as main
from pathlib import Path

from numpy import *
import pandas as pd
import sympy as sy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from IPython.display import Image, Math, Latex, HTML, display

import rivet.rivet_check as _chk
import rivet.rivet_utf as _utf
#import rivet.rivet_pdf as _pdf
#import rivet.rivet_rst as _rst
#import rivet.rivet_units as _units

# import rivet.rivet_report as reprt
# from rivet.rivet_units import *
# from rivet.rivet_config import *
# from rivet.rivet_html import *
# from rivet.rivet_pdf import *


__version__ = "0.9.1"
__author__ = "rholland"
if sys.version_info < (3, 7):
    sys.exit("rivet requires Python version 3.7 or later")

# set up folders, files and dictionaries
rivet_dict = {}
equation_dict = {}

ad_init = {
"adpath" : main._set["path"],
"adfile" : main._set["file"],
"rivetpath" : os.path.dirname("rivet.rivet_lib.py"),
"projpath" : os.pardir,
"reptpath" : os.path.join(os.pardir, "reports")
}
ad_fold = {
"adbase": ad_init["adfile"].split(".")[0],
"spath": os.path.join(ad_init["adpath"], "scripts"),
"tpath": os.path.join(ad_init["adpath"], "table"),
"upath": os.path.join(ad_init["adpath"], "txt"),
"rpath": os.path.join(ad_init["reptpath"], "pdf"),
"xpath": os.path.join(ad_init["reptpath"], "temp"),
"fpath": os.path.join(ad_init["reptpath"], "figures"),
"hpath": os.path.join(ad_init["reptpath"], "html"),
}    
ad_file = {    
"ctxt":  ".".join((ad_fold["adbase"], "txt")),
"cpdf":  ".".join((ad_fold["adbase"], "pdf")),
"chtml":  ".".join((ad_fold["adbase"], "html")),
"trst":  ".".join((ad_fold["adbase"], "rst")),
"tlog":  ".".join((ad_fold["adbase"], "log")),
"ttex1":  ".".join((ad_fold["adbase"], "tex")),
"auxfile": ".".join((ad_fold["adbase"], ".aux")),
"outfile":  ".".join((ad_fold["adbase"], ".out")),
"texmak2":  ".".join((ad_fold["adbase"], ".fls")),
"texmak3":  ".".join((ad_fold["adbase"], ".fdb_latexmk")),
"bakfile": ".".join((ad_fold["adbase"], ".bak"))
}

ad_par = {
    "clean":  (ad_file["auxfile"],
             ad_file["outfile"]),
    "pdf": (0,"margins"), 
    "title" : "Model Title"    
}

_adfile = ad_init["adfile"]
_adpath = ad_init["adpath"]
_adfull = os.path.join(_adpath,_adfile)
_adbak = os.path.join(_adpath,ad_file["bakfile"])
_calcnum = _adfile[1:5]
_calcwidth = 80
with open(_adfull, "r") as f2:
    adbak = f2.read()
with open(_adbak, "w") as f3:
    f3.write(adbak)
print("\n\npath: ", _adpath, ";", _adfile)
print("checks: folders checked ; ad file backup written", "\n\n")
# start checks and logs
#_chk1 = chk.CheckRivet(_tlog)
#_chk1.logstart()
#_chk1.logwrite("< begin model processing >", 1

def _string_settings(first_line):
    """prarse design string settings line

    Method called for each design string. 
    
    """
    exec_flg = -1
    sect_num = -1
    section_flg = -1
    source_flg = -1
    design_descrip = " " 
    par1 = first_line
    #print(par1)
    section_flg = par1.find("]")
    if section_flg > -1:
        design_descrip = par1[section_flg + 1:].strip()
        sect_num = par1[section_flg-2:section_flg]
        sect_num = sect_num.strip("]").strip("[")
    if "[h]" in par1:
        exec_flg = 2
        design_descrip = i[0].replace("[h]","").strip()                
    elif "[x]" in par1:
        exec_flg = 1
        design_descrip = i[0].replace("[x]","").strip()
    else:
        exec_flg = 0

    #print(exec_flg) 
    return [exec_flg, sect_num, design_descrip]

def _write_utf(pline, pp, indent):
    
    """ Write model text to utf-8 encoded file.
    
    Args:
        mentry (string): text 
        pp (int): pretty print flag
        indent (int): indent flag
        
    """
 
    sect_num = sets[1]
    descrip = sets[2]
    print('=' * _calcwidth)
    _write_utf('=' * _calcwidth, 0, 0)
    descrip1 = " " +  descrip + (_calcnum + "-" +
        sect_num).rjust(_calcwidth - len(descrip) - 2)
    print(descrip1)
    _write_utf(descrip1, 1, 0)
    print('=' * _calcwidth)
    _write_utf('=' * _calcwidth, 0, 0)
    
    f1 = open(ad_file["ctxt"], 'a')
    if pp: pline = sy.pretty(pline, use_unicode=True, num_columns=80)
    if indent: pline = " "*4 + pline
    print(pline, file = f1)
    f1.close()

    if txt[0].strip() == '|' : return
    elif txt[0].strip() == "::" : return                        
    elif txt[0].strip() == '`' : return
    elif txt[0][2:4] == ".." : return                        
    elif txt[0][0] == '|' : self._write_utf(txt[0], 1, 0) 
    elif txt[0][2] == "\\" : self._write_utf(txt[0], 1, 0)                
    else: self._write_utf(txt[0], 1, 0)


def _write_py(self):
    """ write python code to file from dictionary
 
        write imports, terms, equations to Python importable file
        the following libraries are imported when the file is imported:
        os, sys
        sympy
        numpy and numpy.linalg
        unum and units
        
        [v]   p0  |  p1   |    p2    |    p3              
                var    expr   statemnt    descrip 

        [e]   p0  |  p1    |    p2   |    p3      |  p4   |  p5   |  p6       
                var     expr    statemnt    descrip     dec1    dec2     units 
        
        [t]   p0 |  p1  |  p2  |  p3  |  p4    |   p5   | p6   | p7  | p8
                var  expr  state1  desc   range1   range2   dec1   un1   un2
        
        [s]   p0          |    p1          |       p2    |   p3           
                left string    calc number     sect num      toc flag

    """
    pyfile1 = open(self.cfilepypath, 'w')
    str1 =  ('"""\nThis file contains Python equations from the '
            'on-c-e model \n\n  '+ self.mfile + '\n'
            '\nFor interactive analysis open the file\n'
            'in an IDE executable shell e.g. Pyzo,\n'
            'Spyder, Jupyter Notebook or Komodo IDE \n'
            '""" \n')
        
    str2 =  ('import os\n'
            'import sys\n'
            'from sympy import *\n'
            'from numpy import *\n'
            'import numpy.linalg as LA\n'
            'import importlib.util\n'
            'import once.config as cfg\n')
                            
#        str2a = ('pypath = os.path.dirname(sys.executable)\n'
#                'oncedir = os.path.join(pypath,"Lib","site-packages","once")\n'
#                'cfg.opath = oncedir\n'
#                'from once.calunit import *\n')

    vlist1 = []
    vlist2 = []
    str3a = str(os.getcwd()).replace("\\", "\\\\")
    str3 = "sys.path.append('" + str3a + "')"
    importstr = str1 + str2  + str3
    pyfile1.write(importstr + 2*"\n")
    _vardef =[]
    for k1 in self.odict:               # write values and equations
        if k1[0:2] == '_e' or k1[0:2] == '_v':
            try:
                exec(self.odict[k1][2].strip())
                _vardef.append(self.odict[k1][2].strip() + "  #- " +
                                self.odict[k1][3].strip())
                vlist1.append(self.odict[k1][0].strip())
                vlist2.append(self.odict[k1][3].strip())
            except:
                pass
        if k1[0:2] == '_s':             # write section headings
            _vardef.append('#')
            _vardef.append('# section: '+self.odict[k1][0].strip())
    for il in _vardef:
        pyfile1.write(str(il) + '\n\n')
    vlen = len(vlist1)
    str4 = '[ '
    for ix in range(0,vlen):
        try: 
            for jx in range(3*ix, 3*ix+3):
                str4 += "'" + str(vlist1[jx]) + "', "
            str4 += '\n'
        except:
            pass
    str4 += ']'
    
    str4a = '[ '
    for ix in range(0,vlen):
        try: 
            for jx in range(3*ix, 3*ix+3):
                str4a += "'" + str(vlist2[jx]) + "', "
            str4a += '\n'
        except:
            pass
    str4a += ']'

    pyfile1.write('#\n# variables\nvlist1 = ' + str4 + '\n')
    pyfile1.write('#\n# variable definitions\nvlist2 = ' + str4a + '\n')

    str5 = ('\ndef vlist(vlistx = vlist1, vlisty= vlist2):\n'
            '   """Utility function for interactively listing once\n'
            '      variable values. Variables are stored in vlist1 and'
            '      definitions in vlist2. Type vlist()\n'
            '      to list updated variable summary after executing\n'
            '      calc Python script\n'
            '   """\n\n'
            '   for lsti in zip(vlistx, vlisty):\n'
            '       item1 = eval(str(lsti[0]))\n'
            '       def1 = lsti[1]\n'
            '       cncat1 = str(lsti[0]) + " = " + str(item1) + " "*30\n'
            '       print(cncat1[:25] + "# " + def1)\n\n'
            'if __name__ == "__main__":\n'
            '       vlist()'
            '       \n\n')
    
    pyfile1.write(str5 + "\n")
    pyfile1.close()
    
    for lsti in zip(vlist1, vlist2):
        #print(lsti)
        item1 = eval(str(lsti[0]))
        def1 = lsti[1]
        cncat1 = str(lsti[0]) + " = " + str(item1) + " "*40
        cfg.varevaled += cncat1[:30] + "# " + def1 + "\n"


def r__(fstr):
    """run python code

    """
    fstr1 = fstr.split("\n", 1)
    fstr2 = fstr1[1].splitlines()
    str_set = _string_settings(fstr1[0])
    if str_set[0] == 2:
        return
    if str_set[0] == 0:
        if int(str_set[1]) > -1:
            _prt_sect(str_set)
        for i in fstr2:
            exec(i.strip())

    rivet_dict.update(locals())

def i__(fstr):
    """evaluate insert string
    
    """
    global eqnum
    fstr1 = fstr.split("\n", 1)
    fstr2 = fstr1[1].splitlines()
    str_set = _string_settings(fstr1[0])
    if str_set[0] == 2:
        return
    if str_set[0] == 0:
        if int(str_set[1]) > -1:
            _prt_sect(str_set)
        for i in fstr2:
            print(i.strip())

    rivet_dict.update(locals())

def v__(fstr):
    """evaluate value string

    """
    global eqnum, sectnum
    fstr1 = fstr.split("\n", 1)
    fstr2 = fstr1[1].splitlines()
    str_set = _string_settings(fstr1[0])
    
    if str_set[0] == 2:
        return
    if str_set[0] == 1:
        vcalc = _utf.Vexec_u(fstr2, rivet_dict)
        vdict1, vcalc1 = vcalc.vutf()
        rivet_dict.update(vdict1)
        return
    if str_set[0] == 0:
        vcalc = _utf.Vxec_u(fstr2, rivet_dict)
        vdict1, vcalc1 = vcalc.vutf()
        rivet_dict.update(vdict1)
        if int(str_set[1]) > -1:
            _prt_sect(str_set)            
        for i in vcalc1:
            if "=" in i:
                print(" "*4 + i)
            else:
                print(i)

def e__(fstr):
    """evaluate equation string

    """
    global eqnum, sectnum
    fstr1 = fstr.split("\n", 1)
    fstr2 = fstr1[1].splitlines()
    str_set = _string_settings(fstr1[0])
    #print('equation', str_set)
    
    if str_set[0] == 2:
        return
    if str_set[0] == 1:
        ecalc = _utf.Exec_u(fstr2, rivet_dict)
        edict1, ecalc1 = ecalc.eutf()
        rivet_dict.update(edict1)
        return
    if str_set[0] == 0:
        ecalc = _utf.Exec_u(fstr2, rivet_dict)
        edict1, ecalc1 = ecalc.eutf()
        rivet_dict.update(edict1)
        if int(str_set[1]) > -1:
            _prt_sect(str_set)
        for i in ecalc1:
            if "=" in i:
                print(" "*4 + i)
            else:
                print(i)

def t__(fstr):
    """evaluate table string
    
    """

    global eqnum, sectnum
    settings = _string_settings(fstr[0])

    rivet_dict.update(locals())


def _gencalc():
    """ execute program
        0. insert [i] data into model (see _genxmodel())
        1. read the expanded model 
        2. build the operations ordered dictionary
        3. execute the dictionary and write the utf-8 calc and Python file
        4. if the pdf flag is set re-execute xmodel and write the PDF calc
        5. write variable summary to stdout
    
    """
    vbos = cfg.verboseflag                          # set verbose echo flag
    _el = ModCheck()
    _dt = datetime.datetime
    with open(os.path.join(cfg.cpath, cfg.cfileutf),'w') as f2:
        f2.write(str(_dt.now()) + "      once version: " + __version__ )
    _mdict = ModDict()                              #1 read model                              
    _mdict._build_mdict()                           #2 build dictionary
    mdict = {}
    mdict = _mdict.get_mdict()
    newmod = CalcUTF(mdict)                         #4 generate UTF calc
    newmod._gen_utf()                                                                    
    newmod._write_py()                              #4 write Python script            
    _el.logwrite("< python script written >", vbos)                          
    _el.logwrite("< pdfflag setting = " + str(cfg.pdfflag) +" >", vbos)        
    if int(cfg.pdfflag):                            #5 check for PDF parameter                                       # generate reST file
        rstout1 = CalcRST(mdict)                          
        rstout1.gen_rst()                           
        pdfout1 = CalcPDF()                         #5 generate TeX file                 
        pdfout1.gen_tex()
        pdfout1.reprt_list()                        #5 update reportmerge file
        _el.logwrite("< reportmerge.txt file updated >", 1)        
        os.chdir(once.__path__[0])                  #5 check LaTeX install
        f4 = open('once.sty')
        f4.close()
        os.chdir(cfg.ppath)
        _el.logwrite("< style file found >", vbos)
        os.system('latex --version')                
        _el.logwrite("< Tex Live installation found>", vbos)
        pdfout1.gen_pdf()                           #5 generate PDF calc
    os.chdir(cfg.ppath)
    return mdict         

