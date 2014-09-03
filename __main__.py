""" This module makes the oncepy package folere callable as a program module

The module determines whether the file is a model or project file.
Start the program from the model directory (division) with

    python -m oncepy ddmm.modelname.txt

where dd is the division number and mm is the model number

"""
from __future__ import division
from __future__ import print_function
import locale
import os
import sys
import oncepy
from oncepy.cproj import ProjStart
from oncepy.cstart import ModStart
from oncepy.cdict import ModDicts
from oncepy.ctext import CalcUTF
from oncepy.crst import CalcRST
from oncepy.cpdf import CalcPDF
from oncepy.ccheck import ModCheck
import oncepy.oconfig as cfg
from sympy.core.cache import *

__version__ = "0.4.5"
__author__ = 'rholland'
locale.setlocale(locale.LC_ALL, '')

#------------------------------------------------------------------------------
def _gencalc(fi4):
    """ run program in six steps
        arguments:
        fi4 - list of auxiliary files
    """
    ew = ModCheck()

    # generate calc file
    modinit = ModStart()
    calcf, pyf, sumf = modinit.gen_filenames()      # generate filenames
    dicts = ModDicts()                              # generate dicts
    dicts.build_dicts()
    fidict = dicts.get_fidict()
    mdict = dicts.get_mdict()
    modinit.out_term()                              # echo output if -e or -b

    cfg.caltype = 0                                 # check for PDF calc flag
    with open(cfg.sysargv[1], 'r') as f5:
        readlines2 = f5.readlines()
    for i2 in readlines2:
        # check for #- format tag
        if len(i2.strip()) > 0:
            if i2.split('|')[0].strip() == '#- format':
                cfg.caltype = i2.split('|')[2].strip()

    if float(cfg.caltype) != 0:
        try:                                        # PDF style file source
            f2 = open('once.sty')
            f2.close()
            cfg.stylefile = 'model folder'
            cfg.stylepath = os.getcwd()
        except IOError:
            try:
                os.chdir(os.pardir)
                f3 = open('once.sty')
                f3.close()
                cfg.stylefile = 'project folder'
                cfg.stylepath = os.getcwd()
                os.chdir(cfg.mpath)
            except IOError:
                os.chdir(oncepy.__path__[0])
                f4 = open('once.sty')
                f4.close()
                cfg.stylefile = 'built-in'
                cfg.stylepath = os.getcwd()
                os.chdir(cfg.mpath)

    modinit.file_summary()                          # write file table
    modinit.var_table(mdict)                        # write variable table
    newmod = CalcUTF(mdict, fidict, calcf, pyf, sumf)
    newmod.gen_utf()                                # generate UTF calc
    if float(cfg.caltype) != 0:                     # PDF calc margin
        try:
            pdfmargin = float(cfg.caltype.strip())
        except TypeError:
            pdfmargin = 1.0

        p1 = cfg.stylepath + "/once.sty"
        with open(p1,'r') as f2:
            newlines = []
            for line1 in f2.readlines():
                if line1[:9] == "\geometry":
                    line1 = ("\geometry{hmargin={1.0in,0.75in}"
                             ",vmargin={0.9in," + str(pdfmargin) + "in}}\n")
                newlines.append(line1)
        with open(p1, 'w') as f3:
            for line1 in newlines:
                f3.write(line1)
        # remove auxiliary files

        for i4 in fi4:                          # remove any auxiliary files
            try:
                os.remove(i4)
            except OSError:
                pass

        rstout1 = CalcRST(mdict, fidict)        # generate rst file
        rstout1.gen_rst()
        ew.errwrite("< rst file written >", 0)

        pdfout1 = CalcPDF(cfg.mfile)            # generate PDF file
        pdfout1.gen_tex()
        pdfout1.gen_pdf()
        ew.errwrite("< pdf file written >", 0)

#------------------------------------------------------------------------------
if __name__ == '__main__':                      # start program
    #print(sys.argv)
    cfg.sysargv = sys.argv

    startmod = ModStart
    startproj = ProjStart

    _cleanflag = 1                              # check command line input
    if len(cfg.sysargv) < 2:
        startmod.cmdline(__version__)
    elif cfg.sysargv[1] == '-h':
        startmod.cmdline(__version__)
    if len(cfg.sysargv) > 2 and '-noclean' in cfg.sysargv:
        _cleanflag = 0                          # set clean aux files flag

    _ew = ModCheck()                            # start execution log
    _ew.logstart()


    cfg.mfile = cfg.sysargv[1]                  # set paths
    cfg.mpath = os.getcwd()
    os.chdir(cfg.mpath)
    sys.path.append(cfg.mpath)
    #print(cfg.mfile)
    clear_cache()                               # clear sympy cache

    with open(cfg.sysargv[1], 'r') as _f1:      # check for project tag [p]
        _readlines1 = _f1.readlines()
    for _i1 in _readlines1:
        if len(_i1.strip()) > 0:
            #print(i1)
            if _i1.split()[0].strip()[0:3] == '[p]':
                cfg.pfile = cfg.sysargv[1]
                cfg.ppath = os.getcwd()
                print("project operations are not supported yet")
                break
                #_startproj()

    rstfile = cfg.mfile.replace('.txt', '.rst') # auxiliary files
    texfile = cfg.mfile.replace('.txt', '.tex')
    auxfile = cfg.mfile.replace('.txt', '.aux')
    outfile = cfg.mfile.replace('.txt', '.out')
    logfile = cfg.mfile.replace('.txt', '.log')
    texmak1 = cfg.mfile.replace('.txt', '.fls')
    texmak2 = cfg.mfile.replace('.txt', '.fdb_latexmk')
    fi5 = [rstfile, texfile, auxfile, outfile, logfile,
               texmak1, texmak2]

    _gencalc(fi5)                               # generate calcs

    _ew.errwrite("< calc completed >", 1)
    _ew.logclose()                              # close log

    if _cleanflag:                              # remove auxiliary files
        for i5 in fi5:
            try:
                os.remove(i5)
            except OSError:
                pass
                                                # end of program
