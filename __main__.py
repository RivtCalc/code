cfg.sysargv = sys.argv                               # read command line
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

_ofolders = ('dbmodel','dbcalc','dbscrpt','dbtable','rprt','temp','image') 
_calcnum = cfg.calcnum =  _mfile.split('_')[0][1:]   # write to config file
_mbase = cfg.mbase = _mfile.split('.')[0] 
_cfilepdf = cfg.cfilepdf = "c" + _mbase[1:] + ".pdf"
_cfileutf = cfg.cfileutf = "c" + _mbase[1:] + ".txt"
_cfilepy = cfg.cfilepy = _mbase + ".py" 
_tpath = cfg.tpath = os.path.join(_ppath, "dbtable")
_spath = cfg.spath = os.path.join(_ppath, "dbscrpt")
_cpath = cfg.cpath = os.path.join(_ppath, "dbcalc")
_ipath = cfg.ipath = os.path.join(_ppath, "image")   
_rpath = cfg.rpath = os.path.join(_ppath, "reprt")   
_xpath = cfg.xpath = os.path.join(_ppath, "temp")
_logfile = cfg.logfile = _calcnum + ".log.txt"          # files in temp   
_logpath = cfg.logpath = os.path.join(_xpath, _logfile)
_texfile = cfg.texfile = _mbase + ".tex"
_texmak1 = cfg.texfile2 = os.path.join(_xpath, _texfile)
_rstfile = cfg.rstfile = os.path.join(_xpath, _mbase + '.rst')     
_auxfile =  os.path.join(_xpath, _mbase + '.aux')
_outfile =  os.path.join(_xpath, _mbase + '.out')
_texmak2 =  os.path.join(_xpath, _mbase + '.fls')
_texmak3 =  os.path.join(_xpath, _mbase + '.fdb_latexmk')
_calcfiles = (_cfileutf, _cfilepdf, _cfilepy, _texfile)
_cleanlist = (_rstfile, _auxfile, _outfile, _texmak2, _texmak3)

_el = ModCheck()
_logwrite = _el.logstart()                          # start log
_el.logwrite("< begin model processing >", 1)
calstart._filesummary()                             # write file summary
with open(_mfile, 'r') as f1:
    readlines1 = f1.readlines()
    calstart._paramline(readlines1[0])              # write config flags 
os.chdir(_ppath)                                    # set project path
sys.path.append(_ppath)
calstart._genxmodel(_mfile, _mpath)                 # expand model file
mdict1 = calstart._gencalc()                        # run calc   
                            # on return clean up and echo result summaries
vbos = cfg.verboseflag
if cfg.cleanflag:                                   # check noclean flag
    _el.logwrite("<cleanflag setting = " + str(cfg.cleanflag) + ">", vbos)
    os.chdir(_tpath)
    for _i4 in _cleanlist:                            
        try:
            os.remove(_i4)
        except OSError:
            pass
    os.chdir(_ppath)
if cfg.echoflag:                                    # check echo calc flag 
    _el.logwrite("<echoflag setting = " + str(cfg.echoflag) +">", vbos)
    try:
        with open(_cfile, 'r') as file2:
            for il2 in file2.readlines():
                print(il2.strip('\n'))
    except:
        _el.logwrite("< utf calc file could not be opened >", vbos)    
if cfg.openflagpdf:                                 # check open PDF flag 
    try:
        pdffilex = os.path.join(_ppath, _cpath, _cfilepdf)
        os.system(pdffilex)
    except:
        _el.logwrite("< pdf calc file could not be opened >", vbos)

if cfg.openflagutf:                                 # check open UTF flag 
    try:
        utffilex = os.path.join(_ppath, _cpath, _cfileutf)
        os.system(utffilex)
    except:
        _el.logwrite("< txt calc file could not be opened >", vbos)

calstart._variablesummary()                         # echo calc results
_el.logwrite("< end of once program >", 1)
_el.logclose()                                      # close log
                                                    # end of program
