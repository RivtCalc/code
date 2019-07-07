#!

#print(sys.argv)
try:
    _mfile = cfg.mfile = sys.argv[1].strip()         # model name
    _mpath = cfg.mpath = os.getcwd()                 # model path
    _ppath = cfg.ppath = os.path.split(_mpath)[0]    # project path
    _backfile = _mfile.split('.')[0] +'.bak'
    #print("model file", _mpath, _mfile)
    _f2 = open(_mfile, 'r')                          # make model backup
    _modelbak = _f2.read()
    _f2.close()
    _f3 = open(_backfile,'w')
    _f3.write(_modelbak)
    _f3.close()
    print("< model backup file written >")
except:                                              # run a utility script
    try:
        if sys.argv[1].strip() == '-s':
            print("< run utility script >")
            _spath = os.path.join(cfg.opath, "calscripts")
            shellcmd = str(sys.argv[2])
            _scpath = os.path.join(_spath, shellcmd)
            shellcmd2 = "python " + _scpath 
            #print("shell command: ", shellcmd2)
            os.system(shellcmd2)
            sys.exit(1)
        else:
            calstart.cmdlinehelp()
            sys.exit("model or script not found")    
    except:
        calstart.cmdlinehelp()
        sys.exit("model or script not found")

# output files and folders
_ofolders = ('','figures','scripts','tables','calcs','temp') 
_calcnum = cfg.calcnum =  _mfile.split('_')[0][1:]   
_mbase = cfg.mbase = _mfile.split('.')[0] 
_cfilepdf = cfg.cfilepdf = "c" + _mbase[1:] + ".pdf"
_cfileutf = cfg.cfileutf = "c" + _mbase[1:] + ".txt"
_cfilepy = cfg.cfilepy = _mbase + ".py" 
# input files and folders
_tpath = cfg.tpath = os.path.join(_ppath, "table")
_spath = cfg.spath = os.path.join(_ppath, "dbscrpt")
_cpath = cfg.cpath = os.path.join(_ppath, "dbcalc")
_ipath = cfg.ipath = os.path.join(_ppath, "image")   
_rpath = cfg.rpath = os.path.join(_ppath, "reprt")   
_xpath = cfg.xpath = os.path.join(_ppath, "temp")
# log files and folders
_logfile = cfg.logfile = _calcnum + ".log.txt"          # files in temp   
_logpath = cfg.logpath = os.path.join(_xpath, _logfile)
temppath = os.path.join(cfg.ppath , "temp")
if not os.path.exists(temppath):
    os.makedirs(temppath)
self.logname = ''
self.logname = os.path.join(cfg.ppath , "temp", cfg.logfile)
#print('log name,',self.logname)
# temp files and folders
_texfile = cfg.texfile = _mbase + ".tex"
_texmak1 = cfg.texfile2 = os.path.join(_xpath, _texfile)
_rstfile = cfg.rstfile = os.path.join(_xpath, _mbase + '.rst')     
_auxfile =  os.path.join(_xpath, _mbase + '.aux')
_outfile =  os.path.join(_xpath, _mbase + '.out')
_texmak2 =  os.path.join(_xpath, _mbase + '.fls')
_texmak3 =  os.path.join(_xpath, _mbase + '.fdb_latexmk')
_calcfiles = (_cfileutf, _cfilepdf, _cfilepy, _texfile)
_cleanlist = (_rstfile, _auxfile, _outfile, _texmak2, _texmak3)
