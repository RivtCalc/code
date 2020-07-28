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

import rivetcalc.rc_lib as rc
import rivetcalc.rc_calc as _rc_calc

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

_modfileS = "empty"
if __name__ == "__main__":
    try:
        _modfileS = sys.argv[1]                          # model file argument
        _cwdS = os.getcwd()
        _cfull = Path(_modfileS)
        _cfileS    = Path(_cfull).name                   # calc file name
        _cname    = _cfileS.split(".py")[0]              # calc file basename
        print("current folder: ", os.getcwd())
        print("model name: ", _cname)
        __import__(_cname)
    except Exception as _e:
        _cmdlinehelp()
        print("model file: ", _modfileS)
        print(_e)
        sys.exit()      
