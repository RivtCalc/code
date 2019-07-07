class CalcUTF(object):
    """Return UTF-8 calcs
    ::

        Arguments:
            odict (ordered dict) : model dictionary
        
        Files written:
            cfile     : UTF-8 calc file name
            cfilepy   : Python model file name

        Operation keys, number of parameters and associated tags:
            _r + line number - 6 - [r] run 
            _i + line number - 6 - [i] insert
            _v + line number - 4 - [v] value            
            _e + line number - 7 - [e] equation
            _t + line number - 9 - [t] table
            _s + line number - 3 - [s] sections
            _~ + line number - 1 - blank line
            _x + line number - 2 - pass-through text
            _y + line number - 2 - value heading
            _#               - 1 - control line
            _lt              - 2 - license text [licensetext]
    
            [r]    p0   |   p1     |   p2    |   p3   |    p4   |   p5    
                  'os'     command     arg1      arg2      arg3     arg4 
                  'py'     script      arg1      arg2      arg3     arg4         

            [i]    p0   |   p1         |  p2      |   p4      |   p5         
                  'fig'     fig file     caption      size      location
                  'tex'     text file               descrip      (text)
                  'mod'     model file              descrip      (text)
                  'fun'     funct file   var name   descrip      (text)
                  'rea'     file         var name   descrip      (text)
                  'wri'     file         var name   descrip      (text)
                  'app'     file         var name   descrip      (text)
            
            [v]   p0  |  p1   |    p2    |    p3              
                  var    expr   statemnt    descrip 
    
            [e]   p0  |  p1    |    p2   |    p3      |  p4   |  p5   |  p6       
                 var     expr    statemnt    descrip     dec1    dec2     units 
            
            [t]   p0 |  p1  |  p2  |  p3  |  p4    |   p5   | p6   | p7  | p8
                  var  expr  state1  desc   range1   range2   dec1   un1   un2
            
            [s]   p0          | p1          |       p2    |   p3           
                  left string    calc number     sect num   toc flag
    """

    def __init__(self, odict1):
        """Initialize parameters for UTF calc.
        ::

         Arguments:
            odict1 (dictionary):  model dictionary
        
        """
        # dicts
        self.vbos = cfg.verboseflag
        self.el = ModCheck()
        self.odict = odict1
        # paths and files
        self.mpath = cfg.ppath
        self.mfile = cfg.mfile
        self.cfile = cfg.cfileutf
        self.ppath = cfg.ppath
        self.cpath = cfg.cpath
        self.calfile = os.path.join(self.cpath, self.cfile)
        #print("calcfile path", self.calfile)
        self.cfile = codecs.open(self.calfile, 'w', encoding='utf8')
        self.cfilepy = cfg.cfilepy
        self.cfilepypath = os.path.join(cfg.spath,cfg.cfilepy)
        # parameters
        self.fignum = 0
        self.widthc = cfg.calcwidth
        self.xtraline = False
        
    def _gen_utf(self):
        """Generate utf calc from model dictionary.

        """
        _dt = datetime.datetime
        self._write_utf(str(_dt.now()) + "      on-c-e version: " +
                        __version__, 0, 0)

        if cfg.stocflag:
            _sects1 = []
            for _dkey in self.odict:
                if _dkey[0:2] == '_s':
                    _sval1 = self.odict[_dkey]
                    _sects1.append(str(_sval1[2]) + ' ' + str(_sval1[0]))
            self._write_utf('\n        Calc Sections', 0, 1)
            self._write_utf('    =============', 0, 1)
            for _sect1 in _sects1:
                self._write_utf('    '+ _sect1, 0, 1)

            self._write_utf('\n', 0, 0)

        for _i in self.odict:
            mtag = _i[0:2]
            mvals = self.odict[_i]
            #print('rmtag', mtag, _i, self.odict[_i])
            if mvals[0].strip() == '#- stop':
                sys.exit(1)
            if mtag == '_#':
                self.xtraline = False
                continue
            if mtag == '_~': 
                self._prt_blnk()
                self.xtraline = False
                continue
            if mtag ==   '_r':                # execute dictionary line by line
                self._prt_run(self.odict[_i])
                self.xtraline = False
            elif mtag == '_i':
                self._prt_ins(self.odict[_i])
                self.xtraline = False
            elif mtag == '_v':
                self._prt_val2(self.odict[_i])
                self.xtraline = False
            elif mtag == '_e':
                #print('_e', self.odict[_i])
                self._prt_eq(self.odict[_i])
                self.xtraline = True
            elif mtag == '_t':
                self._prt_table(self.odict[_i])
                self.xtraline = True
            elif mtag == '_s':
                self._prt_sect(self.odict[_i])
                self.xtraline = False
            elif mtag == '_x':
                self._prt_txt(self.odict[_i])
                self.xtraline = False
            elif mtag == '_y':
                self._prt_val1(self.odict[_i])
                self.xtraline = False
            else:
                pASs
            if self.xtraline:
                self._prt_blnk()   
        for _i2 in self.odict:                  # add calc license
            if _i2 == '_lt':
                self._write_utf(self.odict[_i2],0)
        self._write_utf('\n[end of calc]', 0, 0)     # end calc
        self.cfile.close()                      # close calc file
        self.el.logwrite("< UTF calc written >", self.vbos)  
        #for _i in self.odict: print(i, self.odict[i])

    def get_odict(self):
        """Return model dictionary
        
        """
        return self.odict