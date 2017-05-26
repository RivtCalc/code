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
script_path = os.path.join(cfg.opath,'scripts')
sys.path.append(script_path)
import csv2rst
__version__ = "0.9.0"
__author__ = 'rholland'
#locale.setlocale(locale.LC_ALL, '')

def cmdlinehelp():
    """command line help
    
    """
    print()
    print("Run once at the command line in the model folder with:")
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
    print("where rrcc is the calculation and model number.")
    print("The program also writes table, log and other intermediate files")
    print("to the table and temp subfolder.")
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

    """
    _el = ModCheck()
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
    _el.logwrite(filesum1, 1)

def _variablesummary():
    """variable summary table
    
    """
    
    print("Variable Summary")
    print("================")
    print(cfg.varevaled)

def _paramline(mline1):
    """set calc level parameter flags
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
    cfg.pdfmargins = '1.0in,0.75in,0.9in,1.0in'
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
        for param in mline2:
            if param.strip()[0:5] == 'title':
                cfg.calctitle = param.strip()[6:] 
        for param in mline2:
            if param.strip()[0:7] == 'margins':
                cfg.pdfmargins = param.strip()[6:] 
    else:
        pass

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
    return mdict                                    #6 return mdict for summary
        
