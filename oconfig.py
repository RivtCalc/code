# this file is read by the program - do not modify
import oncepy

# command line
sysargv = ''

# package directory
packagepath = oncepy.__path__

# full path and project file name
ppath = ''
pfile = ''

# full path and main model name
mpath = ''
mfile = ''

# calculation output type - can be txt, rst or pdf
caltype = 'txt'

# default decimal places
defaultdec = '3'

# source of unitc.py: default is package folder
# file in local folder overrides project folder
unitfile = 'built-in'

# source of once.sty file: default is package folder
# file in local folder overrides project folder
stylefile = 'built-in'
