# on-c-e configuration file is modified by the program - do not change

import os
oncepath = os.path.abspath(__file__)
oncedir = os.path.dirname(oncepath)
opath = oncedir  # once path

# command line
sysargv = ''

# paths
ppath = ''    # project root
mpath = ''    # model folder
tpath = ''    # table folder
spath = ''    # script folder
cpath = ''    # calc folder
ipath = ''    # image folder
xpath = ''    # temp folder
rpath = ''    # report folder
logpath = ''  # log (temp) folder
#kpath = ''    # package folder

# file names
mfile = ''
mbase = ''
cfileutf = ''
cfilepdf = ''
cfilepy = ''
rstfile = ''
texfile = ''
texfile2 = ''
logfile = ''

# default decimal places
defaultdec = '3,3'

# UTF line width
calcwidth = 80

# flags
pdfflag = 0         # write PDF 
echoflag = 0        # echo output to terminal
cleanflag = 0       # do not clean temporary latex files
projectflag = 0     # compile project
openflagpdf = 0     # open calc PDF
openflagutf = 0     # open calc UTF
verboseflag = 0     # write logging to standard out
stocflag = 0        # write section table of contents

# variables
varevaled = ""     # list of model variables
rsectname = "\n\nContents1"    # default table of contents heading

