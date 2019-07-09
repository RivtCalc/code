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

import rivet.rivet_report as reprt
import rivet.rivet_config as cfg
import rivet.rivet_check as chk
from rivet.rivet_units import *
from rivet.rivet_config import *
from rivet.rivet_utf import *
from rivet.rivet_html import *
#from rivet.rivet_pdf import *

__version__ = "0.9.1"
__author__ = "rholland"

if sys.version_info < (3,7):
    sys.exit('rivet requires Python version 3.7 or later')

display(HTML(
'<style>.prompt{width: 0px; min-width: 0px; visibility: collapse}</style>'))

var_rivet_dict = {}

def startlog():
    tlog1 = os.path.join(cfg.xpath, cfg.tlog)
    chk1 = chk.CheckRivet(tlog1)
    chk1.logstart()                                    
    chk1.logwrite("< begin model processing >", 1)
    return chk1



def r__(fstr):
    fstr1 = fstr.split('\n',1)
    fstr2 = fstr1[1].splitlines()
    for i in fstr2: exec(i.strip())
    return var_rivet_dict.update(locals())

def i__(fstr):
    print(fstr)

def v__(fstr):
    for i in fstr.split('\n'):
        if len(i.strip()) > 0:
            print(i)
            if '=' in i:
                exec(i.strip())
    
    return var_rivet_dict.update(locals())

def e__(fstr):    
    for j in fstr.split('\n'):
        if len(j.strip()) > 0:
                if '=' in j:
                        k = j.split('=')[1]        
                        nstr3 = str(j) + " = " + str(eval(k)) 
                        print(nstr3)
                        exec(j.strip(), globals())
                else:
                        print(j)
    return var_rivet_dict.update(locals())

def t__(fstr):
    return var_rivet_dict.update(locals())
    

def __s(fstr):
    pass









