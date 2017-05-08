# on-c-e configuration file - modified by the program - do not change

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
defaultdec = '3,3'  # default decimal places
calcwidth = 80      # UTF line width
varevaled = ""      # list of model variables
calctitle = '\n\nModel Title' # default model title
pagemargin = '1.0in,0.75in,0.9in,1.0in'  # pdf page margins
