""" This module makes the oncepy package a program module

It determines whether the file is a model or project file
Start the program from the model directory with
python -m oncepy modelname.txt

"""
from __future__ import division
from __future__ import print_function
import os
import sys
import oncepy
from oncepy import cstart
from oncepy import cproj
from oncepy import ccheck
import oncepy.oconfig as cfg


__all__ = ["cstart", "cdict", "ctext", "crst", "cpdf",
           "cproj", "ccheck"]
__version__ = "0.4.0"
__author__ = 'rholland'

if __name__ == '__main__':

    #read command line arguments
    cfg.sysargv = sys.argv
    startmod = cstart.ModStart
    startproj = cproj.ProjStart

    # check if command line is valid
    if len(cfg.sysargv) < 2:
        startmod.cmdline(__version__)
    elif cfg.sysargv[1] == '-h':
        startmod.cmdline(__version__)

    # set model file path
    _mfile = cfg.mfile = cfg.sysargv[1]
    _mpath = cfg.mpath = os.getcwd()
    os.chdir(_mpath)
    #print(_mpath)

    # start error and event log
    _ew = ccheck.ModCheck()
    _ew.ewrite1()

    # set PDF style file path
    try:
        _f1 = open('once.sty')
        _f1.close()
        cfg.stylefile = 'model folder'
    except IOError as _e:
        try:
            os.chdir(os.pardir)
            _f1 = open('once.sty')
            cfg.stylefile = 'project folder'
            os.chdir(_mpath)
        except IOError as _e:
            os.chdir(oncepy.__path__[0])
            _f1 = open('once.sty')
            cfg.stylefile = 'built-in'
            os.chdir(_mpath)

    # look in file to check for a project
    _f1 = open(cfg.sysargv[1], 'r')
    _readlines1 = _f1.readlines()
    _f1.close()
    for _i1 in _readlines1:
        # check for [p] tag
        if len(_i1.strip()) > 0:
            #print(i1)
            if _i1.split()[0].strip()[0:3] == '[p]':
                cfg.pfile = cfg.sysargv[1]
                cfg.ppath = os.getcwd()
                print("project operations are not ")
                #_startproj()

    # if no [p] tag in file run as model
    startmod()
    # clean up
    if len(cfg.sysargv) > 2 and '-noclean' in cfg.sysargv:
        pass
    else:
            # clean out any auxiliary files
        rstfile = cfg.mfile.replace('.txt', '.rst')
        texfile = cfg.mfile.replace('.txt', '.tex')
        auxfile = cfg.mfile.replace('.txt', '.aux')
        outfile = cfg.mfile.replace('.txt', '.out')
        logfile = cfg.mfile.replace('.txt', '.log')
        texmak1 = cfg.mfile.replace('.txt', '.fls')
        texmak2 = cfg.mfile.replace('.txt', '.fdb_latexmk')

        try:
            os.remove(rstfile)
        except OSError:
            pass
        try:
            os.remove(auxfile)
        except OSError:
            pass
        try:
            os.remove(texfile)
        except OSError:
            pass
        try:
            os.remove(outfile)
        except OSError:
            pass
        try:
            os.remove(logfile)
        except OSError:
            pass
        try:
            os.remove(texmak1)
        except OSError:
            pass
        try:
            os.remove(texmak2)
        except OSError:
            pass

    # check that error log is closed
    _ew.ewclose()

