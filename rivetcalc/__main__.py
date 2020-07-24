# command line help

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
import rivetcalc.rc_lib as rc

__version__ = "0.9.5"
__author__ = "rholland@structurelabs.com"
if sys.version_info < (3, 7):
    sys.exit("RivetCalc requires Python version 3.7 or later")     

def _cmdlinehelp():
    """[summary]

    Returns:
        [type] -- [description]
    """
    print()
    print("Run rivet at the command line in the design folder with:")
    print("     python  ddcc_ userdescrip.py")
    print("where ddcc_ userdescrip.py is a design file in the folder")
    print("and **ddcc** is the model number")
    print()
    print("Specified output is written to the respective calc folder:")
    print("     ddcc_userdescrip.txt")
    print("     ddcc_userdescrip.html")
    print("     ddcc_userdescrip.pdf")
    print("Logs and other intermediate files are written to the temp subfolder.")
    print()
    print("Program and documentation are here: http://rivetcalc.github.io.")
    sys.exit()

if __name__ == "__main__":
    try:
        _calcfileS = sys.argv[1]
        _cwdS = os.getcwd()
        _cfull = Path(_calcfileS)
        _cfile    = Path(_cfull).name                        # calc file name
        _cname    = _cfile.split(".py")[0]                   # calc file basename
        print(_cname)
        print(os.getcwd())
        __import__(_cname)
    except Exception as _e:
        print(_e)
        sys.exit()      
else:
    _cwdS = os.getcwd()
    print("****dir", _cwdS)
    sys.exit()

    """
    def _paramlines(dline1):
     set calc level parameter flags

        #| width:nn | pdf | noclean | margins:T:B:L:R | verbose |
    cfg.pdfflag = 0
    cfg.cleanflag = 1
    cfg.projectflag = 0
    cfg.echoflag = 0
    cfg.calcwidth = 80
    cfg.pdfmargins = "1.0in,0.75in,0.9in,1.0in"
    if mline1[0:2] == "#|":
        mline2 = mline1[2:].strip("\n").split(",")
        mline2 = [x.strip(" ") for x in mline2]
        # print('mline2', mline2)
        if "pdf" in mline2:
            cfg.pdfflag = 1
        if "noclean" in mline2:
            cfg.cleanflag = 0
        if "verbose" in mline2:
            cfg.verboseflag = 1
        if "stoc" in mline2:
            cfg.stocflag = 1
        if "width" in mline2:
            pass
        for param in mline2:
            if param.strip()[0:5] == "title":
                cfg.calctitle = param.strip()[6:]
        for param in mline2:
            if param.strip()[0:7] == "margins":
                cfg.pdfmargins = param.strip()[6:]
    else:
        pass


    vbos = cfg.verboseflag  # set verbose echo flag
    _dt = datetime.datetime
    with open(os.path.join(cfg.cpath, cfg.cfileutf), "w") as f2:
        f2.write(str(_dt.now()) + "      once version: " + __version__)
    _mdict = ModDict()  # 1 read model
    _mdict._build_mdict()  # 2 build dictionary
    mdict = {}
    mdict = _mdict.get_mdict()
    newmod = CalcUTF(mdict)  # 4 generate UTF calc
    newmod._gen_utf()
    newmod._write_py()  # 4 write Python script
    _el.logwrite("< python script written >", vbos)
    _el.logwrite("< pdfflag setting = " + str(cfg.pdfflag) + " >", vbos)
    if int(
        cfg.pdfflag
    ):  # 5 check for PDF parameter                                       # generate reST file
        rstout1 = CalcRST(mdict)
        rstout1.gen_rst()
        pdfout1 = CalcPDF()  # 5 generate TeX file
        pdfout1.gen_tex()
        pdfout1.reprt_list()  # 5 update reportmerge file
        _el.logwrite("< reportmerge.txt file updated >", 1)
        os.chdir(once.__path__[0])  # 5 check LaTeX install
        f4 = open("once.sty")
        f4.close()
        os.chdir(cfg.ppath)
        _el.logwrite("< style file found >", vbos)
        os.system("latex --version")
        _el.logwrite("< Tex Live installation found>", vbos)
        pdfout1.gen_pdf()  # 5 generate PDF calc
    os.chdir(cfg.ppath)
    return mdict  # 6 ret

    # on return clean up and echo result summaries
    vbos = cfg.verboseflag
    if cfg.cleanflag:  # check noclean flag
        _el.logwrite("<cleanflag setting = " + str(cfg.cleanflag) + ">", vbos)
        os.chdir(_tpath)
        for _i4 in _cleanlist:
            try:
                os.remove(_i4)
            except OSError:
                pass
        os.chdir(_ppath)
    if cfg.echoflag:  # check echo calc flag
        _el.logwrite("<echoflag setting = " + str(cfg.echoflag) + ">", vbos)
        try:
            with open(_cfile, "r") as file2:
                for il2 in file2.readlines():
                    print(il2.strip("\n"))
        except:
            _el.logwrite("< utf calc file could not be opened >", vbos)
    if cfg.openflagpdf:  # check open PDF flag
        try:
            pdffilex = os.path.join(_ppath, _cpath, _cfilepdf)
            os.system(pdffilex)
        except:
            _el.logwrite("< pdf calc file could not be opened >", vbos)

    if cfg.openflagutf:  # check open UTF flag
        try:
            utffilex = os.path.join(_ppath, _cpath, _cfileutf)
            os.system(utffilex)
        except:
            _el.logwrite("< txt calc file could not be opened >", vbos)

    calstart._variablesummary()  # echo calc results
    _el.logwrite("< end of once program >", 1)
    _el.logclose()  # close log
    # end of program
    """