import sys
from oncemod import cstart
import oncemod.config as om
try:
    from unitc import *
except:
    from oncemod.calcunits import *


__all__ = ["cstart", "ccheck", "cdict", "ctext", "cpdf", "cset"]
__version__ = "0.3.2"
__author__ = 'rhh'


if __name__ == '__main__':

    #print(sys.argv)
    # check if command line is valid
    sysargv = sys.argv
    cstartmod = cstart.ModStart
    if len(sysargv) < 2:
        cstartmod.cmdline()
    elif sysargv[1] == '-h':
        cstartmod.cmdline()
    # initialize file and paths
    cstartmod.gen_paths()
    # find location of units file
    om.impcheck = 'built-in units'
    try:
        from unitc import *
        om.impcheck = 'units in model directory'
    except:
        try:
            sys.path.append(om.projdir)
            from unitc import *
            om.impcheck = 'units in project directory'
        except:
            from oncemod.calcunits import *

    result = cstart.ModStart(sys.argv)
