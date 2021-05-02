"""
***rivtcalc** may be run interactively from an editor or IDE one cell (#%%) or
string function at a time, or from the command line. If run from the command
line:

    python -m rivtcalc rddss_calcfile.py 

and the calc is written to the calc folder. The calc number ddss is used for
document and report organization, where dd is a two digit division number and
ss is a two digit subdivision number. UTF calcs are always printed to to the
terminal when the a calc file or interactive cell is run. If a file output
function (write_text, write_pdf write_html) is specified in the calc, the entire
calc is processed and the calc file is written to the calc folder."""

import os
import sys
import textwrap
import logging
import warnings
import re
import importlib
import numpy as np
from pathlib import Path
from collections import deque
from typing import List, Set, Dict, Tuple, Optional
import rivtcalc.rv_calc as _rc_calc

__version__ = "0.8.1-beta.1"
__author__ = "rholland@structurelabs.com"
if sys.version_info < (3, 7):
    sys.exit("rivtCalc requires Python version 3.7 or later")

_calcfileS = "empty"


def _cmdlinehelp():
    """command line help """
    print()
    print("Run rivtcalc at the command line in the 'calc' folder with:")
    print("     python  -m rivtcalc rddcc_calcfilename.py")
    print("where rddcc_ calcname.py is the model file in the folder")
    print("and **ddcc** is the model number")
    print()
    print("Specified output is written to the 'calcs' or 'docs' folder:")
    print("     rddcc_calcfilename.txt")
    print("     rddcc_calcfilename.html")
    print("     rddcc_calcfilename.pdf")
    print("Logs and other intermediate files are written to the tmp folder.")
    print()
    print("Program and documentation are here: http://rivtcalc.github.io.")
    sys.exit()


if __name__ == "__main__":
    try:
        _calcfileS = sys.argv[1]  # calc file argument
        _cwdS = os.getcwd()  # get calc folder
        _cfull = Path(_calcfileS)  # calc file full path
        _cfileS = Path(_cfull).name  # calc file name
        _cbaseS = _cfileS.split(".py")[0]  # calc file basename
        print("MAIN  current folder: ", _cwdS)
        print("MAIN  calc name: ", _cfileS)
        importlib.import_module(_cbaseS)
    except ImportError as error:
        print("error---------------------------------------------")
        print(error)
    except Exception as exception:
        # Output unexpected Exceptions.
        print("exception-----------------------------------------")
        print(exception)
