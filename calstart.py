#! python
import subprocess
import datetime
import locale
import os
import sys
import subprocess
import once
import once.config as cfg
from once.caldict import *
from once.caltext import *
from once.calcheck import ModCheck
from once.calpdf import *
from sympy.core.cache import *
#from once.calproj import *

__version__ = "0.9.0"
__author__ = 'rholland'
#locale.setlocale(locale.LC_ALL, '')

def cmdlinehelp():
    """command line help"""
    print()
    print("To run on-c-e at the command line in the model folder, type:")
    print("     python -m once mrrcc_modelname.txt")
    print("where mrrcc_modelname.txt is a model file in the folder")
    print("and **rrcc** is the model number")
    print()
    print("If the model file is omitted or not found in the folder")
    print("the program prints this prompt")
    print()    
    print("If the model is found, calcs are written to the calc folder:")    
    print("     crrcc_modelname.txt (UTF-8 calc)")
    print("     crrcc_modelname.py (interactive Python inputs)")
    print("     crrcc_modelname.calc.pdf(optional)")
    print("where rrcc is the calculation (or model) number.")
    print("The program also writes table, log and other intermediate files")
    print("to the table and temp subfolder")
    print()
    print("To run a built-in example file from the model  folder, type:")
    print("     python -m once -test")
    print("which writes m0000_testmodel.txt to the model folder and runs it.")
    print()
    print("-Links-")
    print("Project overview:        http://structurelabs.com/on-c-e")
    print("Source code and docs:    http://on-c-e.github.io/")
    print("Forum:                   http://on-c-e.net")
    print("Database:                once.pyproject@gmail.com")

def _filesummary():
    """file name summary table
    ::

        log the file name summary

    """

    _el = ModCheck()
    filesum1 = ("File and Path Summary\n"
                "====================="
                "\nproject path :\n    {}\n"    
                "\nmodel file :\n    {}\n"
                "\nipython file :\n    {}\n"
                "\nutf and pdf calcs :\n    {} \n"
                "\nlog file :\n    {}").format(cfg.ppath.strip(), cfg.mfile,
                                        ".../script/" + cfg.cfilepy, 
                                        ".../calc/" + cfg.cfileutf, 
                                        ".../temp/" + cfg.logfile)
    _el.logwrite(filesum1, 1)

def _variablesummary():
    """variable summary
    ::

        write variable summary to output

    """
    
    print("Variable Summary")
    print("================")
    print(cfg.varevaled)

def _paramline(mline1):
    """set calc level parameter flags
    ::
    
       first line of model may include the following flags
       #- pdf, echo, project, openpdf, opentxt, name:calcname,
          width:nn, margins:top:bottom:left:right, verbose, noclean 
    """
    
    cfg.pdfflag = 0
    cfg.cleanflag = 1
    cfg.projectflag = 0
    cfg.openflag = 0
    cfg.echoflag = 0
    cfg.calcwidth = 80
    cfg.pdfmargins = [.5,1,]
    if mline1[0:2] == "#-":
        mline2 = mline1[2:].strip('\n').split(',')
        mline2 = [x.strip(' ') for x in mline2]
        #print('mline2', mline2)
        if 'pdf'     in mline2: cfg.pdfflag = 1
        if 'noclean' in mline2: cfg.cleanflag = 0
        if 'echo'    in mline2: cfg.echoflag = 1
        if 'project' in mline2: cfg.projectflag = 1
        if 'openpdf' in mline2: cfg.openflagpdf = 1
        if 'opentxt' in mline2: cfg.openflagutf = 1
        if 'verbose' in mline2: cfg.verboseflag = 1
        if 'stoc'    in mline2: cfg.stocflag = 1
        if 'width'   in mline2: pass
        for _y in mline2:
            if _y.strip()[0:5] == 'title':
                cfg.calctitle = _y.strip()[6:] 
        if 'margins' in mline2:
            if _y.strip()[0:7] == 'margins':
                cfg.calctitle = _y.strip()[6:] 

    else:
        pass
    
def _gencalc():
    """ execute program
    ::
        1. read the main model
        2. read sub-models if included
        3. build the operations ordered dictionary
        4. if there are sub-models include their [v], [e], [t] 
        5. execute the dictionary and write the utf-8 calc and Python file
        6. if the pdf parameter is provided re-execute and write the PDF calc
    """
    vbos = cfg.verboseflag
    _el = ModCheck()
    _dt = datetime.datetime
    with open(os.path.join(cfg.cpath, cfg.cfileutf),'w') as f2:
        f2.write(str(_dt.now()) + "      on-c-e version: " + __version__ )
    _mdict = ModDict()                              
    _mdict._build_mdict()                           #2 generate model dict
    mdict = {}
    mdict = _mdict.get_mdict()
    newmod = CalcUTF(mdict)                         #5 generate UTF calc
    newmod._gen_utf()                                                                    
    newmod._write_py()                              #5 write Python script            
    _el.logwrite("< python script written >", vbos)                          
    _el.logwrite("< pdfflag setting = " + str(cfg.pdfflag) +" >", vbos)        
    if int(cfg.pdfflag):                            #6 check for PDF parameter                                       # generate reST file
        rstout1 = CalcRST(mdict)                          
        rstout1.gen_rst()                           
        pdfout1 = CalcPDF()                         #6 generate TeX file                 
        pdfout1.gen_tex()
        pdfout1.reprt_list()                        #6 update reportmerge file
        _el.logwrite("< reportmerge.txt file updated >", 1)        
        os.chdir(once.__path__[0])                  #6 check LaTeX install
        f4 = open('once.sty')
        f4.close()
        os.chdir(cfg.ppath)
        _el.logwrite("< style file found >", vbos)
        os.system('latex --version')                
        _el.logwrite("< Tex Live installation found>", vbos)
        pdfout1.gen_pdf()                           #6 generate PDF calc
    os.chdir(cfg.ppath)
    return mdict    
        
