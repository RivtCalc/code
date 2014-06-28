""" This module turns the oncepy package into a program module

The module also determines whether the file is a model or
project file and sets the working directory.

Start program with python -m oncepy modelname
"""

import os
import sys
from oncepy import cstart
from oncepy import cproj
import oncepy.oconfig as cfg


__all__ = ["cstart", "ccheck", "cdict", "ctext", "cpdf", "cproj"]
__version__ = "0.4.0"
__author__ = 'rholland'

if __name__ == '__main__':
    #print(sys.argv)
    sysargv = sys.argv
    cfg.sysargv = sys.argv
    startmod = cstart.ModStart
    startproj = cproj.ProjStart

    # check if command line is valid
    if len(sysargv) < 2:
        startmod._cmdline()
    elif sysargv[1] == '-h':
        startmod._cmdline()

    # set unit file source
    mfile = os.getcwdb()
    try:
        from unitc import *
        cfg.unitfile = 'model folder'
    except ImportError:
        try:
            os.chdir(os.pardir)
            from unitc import *
            cfg.unitfile = 'project folder'
            os.chdir(mfile)
        except ImportError:
            from oncepy.unitc import *
            cfg.unitfile = 'built-in'

    # set PDF style file source
    try:
        f1 = open('once.sty')
        cfg.stylefile = 'model folder'
    except IOError:
        try:
            os.chdir(os.pardir)
            f1 = open('once.sty')
            cfg.stylefile = 'project folder'
            os.chdir(mfile)
        except IOError:
            f1 = open('once.sty')
            cfg.unitfile = 'built-in'

    # check if the file is a model or project file
    mfile = ''
    pfile = ''
    f1 = open(sysargv[1], 'r')
    readlines1 = f1.readlines()
    f1.close()
    for i1 in readlines1:
        # check for [p] tag
        if len(i1.strip()) > 0:
            #print(i1)
            if i1.split()[0].strip()[0:3] == '[p]':
                cfg.pfile = sysargv[1]
                cfg.ppath = os.getcwd()
                print("project operations not complete")
                #startproj()
                continue

    # if no [p] tag then run model
    cfg.mfile = sysargv[1]
    cfg.mpath = os.getcwd()
    startmod()
