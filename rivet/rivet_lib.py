#! python
"""[summary]

Returns:
    [type] -- [description]
"""

import sys
import os
import sympy as sy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from IPython.display import Image, Math, Latex, HTML, display
from numpy import *
from pandas import *

import rivet.rivet_utf as _utf
import rivet.rivet_report as reprt
import rivet.rivet_config as cfg
import rivet.rivet_check as chk
from rivet.rivet_units import *
from rivet.rivet_config import *
from rivet.rivet_html import *
#from rivet.rivet_pdf import *

__version__ = "0.9.1"
__author__ = "rholland"

if sys.version_info < (3,7):
    sys.exit('rivet requires Python version 3.7 or later')

display(HTML(
'<style>.prompt{width: 0px; min-width: 0px; visibility: collapse}</style>'))

var_rivet_dict = {}

#check config file, folders and start logging
tlog1 = os.path.join(cfg.xpath, cfg.tlog)
chk1 = chk.CheckRivet(tlog1)
chk1.logstart()                                    
chk1.logwrite("< begin model processing >", 1)

def r__(_fstr):
    fstr1 = _fstr.split('\n',1)
    fstr2 = fstr1[1].splitlines()
    for i in fstr2: exec(i.strip())
    return var_rivet_dict.update(locals())

def i__(_fstr):
    print(_fstr)

def v__(_fstr):
    vlist = _fstr.split('\n')
    vfunc = _utf.ExecV(vlist)
    if vfunc.process == 's':
        return
    for i in vlist:
            if '=' in i:
                exec(i.strip())
    globals().update(locals())
    vfunc.vprint()
    return var_rivet_dict.update(locals())

def e__(_fstr):    
    for j in _fstr.split('\n'):
        if len(j.strip()) > 0:
                if '=' in j:
                        k = j.split('=')[1]        
                        nstr3 = str(j) + " = " + str(eval(k)) 
                        print(nstr3)
                        exec(j.strip(), globals())
                else:
                        print(j)
    return var_rivet_dict.update(locals())

def t__(_fstr):
    return var_rivet_dict.update(locals())
