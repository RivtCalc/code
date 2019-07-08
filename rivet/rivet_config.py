# rivet configuration file - modified by the program - do not change

import os
import sys
import rivet

try:
    dfile = sys.argv[0].strip()                 # design file name
    rivpath = os.path.abspath(rivet.__file__)
    dpath = os.path.abspath(dfile.__file__)     # design file path
    ddir = os.path.dirname(dpath)
    ppath = dpath.split(ddir)[0]                # project path
    cpath = os.path.join(ppath, 'calcs')
    bakfile = dfile.split('.')[0] +'.bak'
    #print("model file", _mpath, _mfile)
    with open(dfile, 'r') as f2:                # back up design file
         designbak = f2.read()
    with open(bakfile,'w') as f3:
        f3.write(designbak)
    print("< design backup file written >")
except:                                              
    sys.exit("model or script not found")

# paths
fpath = os.path.join(dpath, 'figures')
spath = os.path.join(dpath, 'scripts')
tpath = os.path.join(dpath, 'table')

hpath = os.path.join(dpath, 'html')
rpath = os.path.join(dpath, 'pdf')
upath = os.path.join(dpath, 'txt')
xpath = os.path.join(dpath, 'temp')

# file names
dbase = dfile.split('.')[0]
cutf = ".".join(dbase, 'txt')
chtml = ".".join(dbase, 'html')
cpdf = ".".join(dbase, 'pdf')

trst = ".".join(dbase, 'rst')
tlog = ".".join(dbase, 'log')
ttex1 = ".".join(dbase, 'tex')

auxfile =  os.path.join(dbase, '.aux')
outfile =  os.path.join(dbase, '.out')
texmak2 =  os.path.join(dbase, '.fls')
texmak3 =  os.path.join(dbase,'.fdb_latexmk')
cleantemp = (auxfile, outfile, texmak2, texmak3)

# flags
pdfflag = 0         # write PDF 
nocleanflag = 0     # do not clean temporary latex files
verboseflag = 0     # write logging to standard out
stocflag = 0        # write section table of contents

# variables
defaultdec = '3,3'  # default decimal places
calcwidth = 80      # UTF line width
varevaled = ""      # list of model variables
calctitle = '\n\nModel Title' # default model title
pdfmargin = '1.0in,0.75in,0.9in,1.0in'  # pdf page margins





