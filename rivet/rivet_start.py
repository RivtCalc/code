#! python
"""rivet package

**r-i-v-e-t** is the language component of **on-c-e** (OpenN Calculation
Environment), a framework for producing engineering calculation documents.
**r-i-v-e-t** is intended to improve construction productivity by producing
design documents that are easier to review and resuse. For an overview of
**on-c-e** see http://on-c-e.github.io.

A **r-i-v-e-t** file is a Python file or files that contain
design calculations using the *rivet* package. Design files
have names of the form *ddcc_designfilename.py* where dd and cc are two digit
numbers identifying the division and calculation number respectively.

Calcs and supporting files for a project are contained in a project folder
structure with names as follows:

Project Name (chosen by user)
    |- designs
        |- figures
        |- scripts
        |- tables
    |- calcs
        |- txt
        |- html
        |- pdf
        |- temp

Design input files and their required supporting files are stored in the
design folder and it's respective subfolders. 

The *rivet* package processes and outputs formatted calculations in utf8 text,
html, and PDF if specified (and LaTeX is installed). Output is saved in the
respective calcs folder. Output is also sent to std out (terminal) for
interactive development. The options for output in interactive development
depend on the editor or IDE used (e.g. VS Code, Pyzo, Komodo etc.). The design
file can be processed from command line (in the design folder) as follows.

.. code:: python

            python ddcc_designfilename.py


Program and documentation are here: http://r-i-v-e-t.github.io.  
"""

import sys
import os
import sympy as sy
import matplotlib.pyplot as pl
from rivet import rivet_report as reprt
from rivet import rivet_config as cfg
from rivet import rivet_check as chk
from numpy import *
from pandas import *
from rivet_units import *
from rivet_config import *
from rivet_utf import *
from rivet_html import *
from rivet_pdf import *


__version__ = "0.9.1"
__author__ = "rholland"

if sys.version_info < (3,7):
    sys.exit('Minimum required Python version for rivet is 3.7')

def _filesummary():
    """file name summary table

    """
    filesum1 = ("File and Path Summary\n"
                "====================="
                "\nproject path :\n    {}\n"    
                "\nmodel file :\n    {}\n"
                "\npython file :\n    {}\n"
                "\nutf and pdf calcs :\n    {} \n"
                "\nlog file :\n    {}").format(cfg.ppath.strip(), cfg.mfile,
                                        ".../script/" + cfg.cfilepy, 
                                        ".../calc/" + cfg.cfileutf, 
                                        ".../temp/" + cfg.logfile)
    chk.logwrite(filesum1, 1)

def _variablesummary():
    """variable summary table
    
    """
    
    print("Variable Summary")
    print("================")
    print(cfg.varevaled)

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
    return mdict                                    #6 ret

def _genxmodel(mfile, mpath):
    """ expanded [i] and [t] tags and rewrite model
            [i]  p0   |    p1      |   p2       |   p4       |  p5         
                'txt'   text file   ('literal')  ('b'),('i')   (indent)
                'mod'   model file     ('e')      
                'csv'   csv file      ('wrap')

            [v] p0   |  p1    |    p2     |    p3      
                var    expr     statemnt     descrip 
    
            [e] p0  |  p1   |  p2    |   p3    |  p4 | p5   |  p6  |  p7       
                var    expr   statemt  descrip  dec1   dec2   unit   eqnum
                
            [t] p0    |  p1        |  p2    |  p3   |  p4   |  p5    |  p6  | p7   
                'txt'    text file   'lit'    desc
                'csv'    text file            desc

    """
    
# print(sys.argv)
try:
    _rivpath = os.path.abspath(__file__)
    _rivdir = os.path.dirname(_rivpath)
    _dfile = sys.argv[0].strip()                     # design file name
    _prjpath = _rivpath.split(_rivdir)[0]            # project path
    _designbak = _dfile.split('.')[0] +'.bak'
    #print("model file", _mpath, _mfile)
    with open(_dfile, 'r') as _f2:                   # write design backup
         _designbak = _f2.read()
    with open(_backfile,'w') as _f3:
        _f3.write(_designbak)
    print("< design backup file written >")
except:                                              
    sys.exit("model or script not found")
    
    
    
    ppath = os.path.split(mpath)[0]                        # project path
    #print('model path', mpath)
    #print('project path', ppath)
    tpath = os.path.join(ppath, 'dbtable')                 # table path
    try:                                                   # set calc number                                                                                        
       cnum = int(mfile[1:5])
       calcnum = '[' + str(cnum) + ']'
       divcnum = str(calcnum)[0:2]
       modnum  = str(calcnum)[2:4]
    except:
       calcnum = '[0101]'
       divnum  = '01'
       modnum  = '01'        
    #mtags = ['[v]', '[e]', '[t]')
    blockflag = 0
    vblock = ""
    eblock = ""
    os.chdir(mpath)
    with open(mfile, 'r') as modfile1:                      # read model lines
       model1 = modfile1.readlines()
    for aline in model1:                                    # value blocks        
        if blockflag:
            vblock += aline
            if len(aline.strip()) == 0:
                blockflag = 0
            continue
        if aline[0:5].strip == '[v]':
            vblock += aline
            blockflag = 1        
    blockflag = 0
    for aline in model1:                                    # equation blocks        
        if blockflag:
            eblock += aline
            if len(aline.strip()) == 0:
                blockflag = 0
            continue
        elif aline[0:5].strip == '[e]':
            eblock += aline
            blockflag = 1
        else:
            pass
    with open(mfile, 'w') as modfile2:                      # write new model
        for aline in model1:
            if blockflag:                                   # write v or eq
                if len(aline.strip()) == 0:
                    blockflag = 0
                modfile2.write(aline)
                continue
            
            mtag1 = aline[0:5].strip()
            if mtag1 != '[i]' and mtag1 != '[t]':           # write lines
                modfile2.write(aline)
                continue
            elif mtag1 == '[i]':
                alinev = aline.split('|')
                if 'txt' in alinev[0]:                      # find [i] txt
                    newaline = "  #" + aline
                    modfile2.write(newaline)                # convert comment
                    textfile = alinev[1].strip()
                    textpath = os.path.join(tpath, textfile)
                    with open(textpath,'r') as text1:       # open text file
                        text1v = text1.readlines()
                    if alinev[2].strip()[0:3] == 'lit':
                        modfile2.write('\n  ::') 
                        modfile2.write('\n  ` \n') 
                        for bline1 in text1v:               # insert lit text
                            bline2 = "  |" + bline1
                            modfile2.write(bline2) 
                        modfile2.write('  `\n')                     
                    else:
                        modfile2.write('\n') 
                        for bline1 in text1v:               # insert text
                            bline2 = "  " + bline1
                            modfile2.write(bline2) 
                    continue
                elif 'csv' in alinev[0]:                    # find [i] csv
                    newaline = "  #" + aline
                    modfile2.write(newaline)                # convert comment
                    csvfile = alinev[1].strip()
                    csvpath = os.path.join(tpath, csvfile)
                    rsttab = csv2rst._run(csvpath,(0,0,0))
                    rsttabv = rsttab.split("\n")                        
                    rsttab2 ="\n"
                    for _i in rsttabv:
                        rsttab2 += "  " + _i + "\n"
                    modfile2.write(rsttab2)                 # insert table
                    continue
                elif 'mod' in alinev[0]:                    # find [i] model
                    newaline = "# " + aline                 # convert comment
                    modfile2.write(newaline)                
                    if alinev[2].strip() != 'e':            # [v] tag
                        vtitle = "[s] Values from model " + calcnum +"\n\n"                        
                        modfile2.write(vtitle)
                        modfile2.write(vblock)
                    elif alinev[2].strip() == 'e':          # [v] and [e] tags
                        etitle = ("[s] Values and equations from model " +
                                        calcnum + "\n\n")                        
                        modfile2.write(etitle)
                        modfile2.write(vblock)                        
                        modfile2.write(eblock)
                else:
                    modfile2.write(aline)
            elif mtag1 == '[t]':
                alinev = aline.split('|')
                if 'txt' in alinev[1]:                      # find [t] txt
                    newaline = "  #" + aline
                    modfile2.write(newaline)                # convert comment
                    textfile = alinev[2].strip()
                    textpath = os.path.join(tpath, textfile)
                    with open(textpath,'r') as text1:       # open text file
                        text1v = text1.readlines()
                    modfile2.write('\n  .. table:: ' +
                                   alinev[0][5:].strip()) 
                    #modfile2.write('\n     :widths: auto') 
                    #modfile2.write('\n     :align: center') 
                    modfile2.write('\n  `') 
                    if alinev[2].strip()[0:3] == 'lit':
                        for bline1 in text1v:               # insert lit text
                            bline2 = "    |" + bline1
                            modfile2.write(bline2) 
                        modfile2.write('  `\n')                     
                    else:
                        modfile2.write('\n') 
                        for bline1 in text1v:               # insert text
                            bline2 = "    " + bline1
                            modfile2.write(bline2) 
                    continue
                elif 'csv' in alinev[1]:                    # find [t] csv
                    newaline = "  #" + aline
                    modfile2.write(newaline)                # convert comment
                    modfile2.write('\n  .. table:: ' +
                                   alinev[0][5:].strip()) 
                    #modfile2.write('\n     :widths: auto') 
                    #modfile2.write('\n     :align: center') 
                    modfile2.write('\n  `') 
                    csvfile = alinev[2].strip()
                    csvpath = os.path.join(tpath, csvfile)
                    rsttab = csv2rst._run(csvpath,(0,0,0))
                    rsttabv = rsttab.split("\n")                        
                    rsttab2 ="\n"
                    for _i in rsttabv:
                        rsttab2 += "    " + _i + "\n"
                    modfile2.write(rsttab2)                 # insert table
                    modfile2.write('  `\n')                     
                    continue
                else:
                    modfile2.write(aline)
            else:
                modfile2.write(aline)                   # write orig line

    print("< model file expanded and rewritten \n")

cfg.sysargv = sys.argv                               # read command line


# run rivet
_chk = chk.RivetCheck()
_logwrite = _chk.logstart()                          # start log
_chk.logwrite("< begin model processing >", 1)
_filesummary()                                      # write file summary
with open(_mfile, 'r') as f1:
    readlines1 = f1.readlines()
    calstart._paramline(readlines1[0])              # write config flags 
os.chdir(_ppath)                                    # set project path
sys.path.append(_ppath)
_genxmodel(_mfile, _mpath)                          # expand model file
mdict1 = _gencalc()                                 # run calc   

# on return clean up and echo result summaries
vbos = cfg.verboseflag
if cfg.cleanflag:                                   # check noclean flag
    _el.logwrite("<cleanflag setting = " + str(cfg.cleanflag) + ">", vbos)
    os.chdir(_tpath)
    for _i4 in _cleanlist:                            
        try:
            os.remove(_i4)
        except OSError:
            pass
    os.chdir(_ppath)
if cfg.echoflag:                                    # check echo calc flag 
    _el.logwrite("<echoflag setting = " + str(cfg.echoflag) +">", vbos)
    try:
        with open(_cfile, 'r') as file2:
            for il2 in file2.readlines():
                print(il2.strip('\n'))
    except:
        _el.logwrite("< utf calc file could not be opened >", vbos)    
if cfg.openflagpdf:                                 # check open PDF flag 
    try:
        pdffilex = os.path.join(_ppath, _cpath, _cfilepdf)
        os.system(pdffilex)
    except:
        _el.logwrite("< pdf calc file could not be opened >", vbos)

if cfg.openflagutf:                                 # check open UTF flag 
    try:
        utffilex = os.path.join(_ppath, _cpath, _cfileutf)
        os.system(utffilex)
    except:
        _el.logwrite("< txt calc file could not be opened >", vbos)

calstart._variablesummary()                         # echo calc results
_el.logwrite("< end of once program >", 1)
_el.logclose()                                      # close log
                                                    # end of program
