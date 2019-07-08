#! python
"""[summary]

Returns:
    [type] -- [description]
"""

import sys
import os
import sympy as sy
import matplotlib.pyplot as pl
import rivet.rivet_report as reprt
import rivet.rivet_config as cfg
import rivet.rivet_check as chk
from numpy import *
from pandas import *
from rivet.rivet_units import *
from rivet.rivet_config import *
from rivet.rivet_utf import *
from rivet.rivet_html import *
from rivet.rivet_pdf import *


__version__ = "0.9.1"
__author__ = "rholland"

if sys.version_info < (3,7):
    sys.exit('Minimum required Python version for rivet is 3.7')



def r__():



def i__():



def v__():



def e__():



def t__():


# start logs and output file summary
tlog1 = os.path.join(cfg.xpath, cfg.tlog)
chk1 = chk.CheckRivet(tlog1)
chk1.logstart()                                     # start log
chk1.logwrite("< begin model processing >", 1)

_fsum1 = _filesummary()                             # write file summary
chk1.logwrite(_fsum1, 1)

""" 
    1. read the expanded model 
    2. build the operations ordered dictionary
    3. execute the dictionary and write the utf-8 and htmml calc
    4. if the pdf flag is set re-execute xmodel and write the PDF calc
    5. write variable summary to stdout

"""






