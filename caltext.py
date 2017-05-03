#! python
from __future__ import division
from __future__ import print_function
import codecs
import datetime
import sys
import os
import pprint as ppr
from numpy import *
import numpy.linalg as LA
from sympy import *
from sympy import var as varsym
from sympy import printing
from once.calunit import *
from once.calcheck import ModCheck
from once import config as cfg

__version__ = "0.9.0"
__author__ = 'rholland@structurelabs.com'


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
            _c               - 1 - control line
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
        self._write_utf(str(_dt.now()) + "      on-c-e version: " + __version__
                        , 0, 0)

        if cfg.stocflag:
            _sects1 = []
            for _dkey in self.odict:
                if _dkey[0:2] == '_s':
                    _sval1 = self.odict[_dkey]
                    _sects1.append(str(_sval1[2]) + ' ' + str(_sval1[0]))
            self._write_utf('\n    Calc Sections', 0, 1)
            self._write_utf('    =============', 0, 1)
            for _sect1 in _sects1:
                self._write_utf('    '+ _sect1, 0, 1)

            self._write_utf('\n', 0, 0)

        for _i in self.odict:
            self.xtraline = True
            mtag = _i[0:2]
            mvals = self.odict[_i]
            #print('rmtag', mtag, _i, self.odict[_i])
            if self.odict[_i][0].strip() == '#- stop':
                sys.exit(1)
            if mtag ==   '_r':                # execute dictionary line by line
                self._prt_run(self.odict[_i])
            elif mtag == '_i':
                self._prt_ins(self.odict[_i])
            elif mtag == '_v':
                self._prt_val2(self.odict[_i])
            elif mtag == '_e':
                self._prt_eq(self.odict[_i])
            elif mtag == '_t':
                self._prt_table(self.odict[_i])
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
                pass
            if mtag == '_c': 
                continue
            if mtag == '_~': 
                self._prt_blnk()
                continue
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
        """ return model dictionary
        
        """
        return self.odict
    
    def _prt_blnk(self):
        """Insert blank line.

        """
        self._write_utf(' ', 0, 0)

    def _prt_txt(self, txt):
        """Print pass-through text.
        
        ::

            arguments:
                txt (string): text that is not part of an operation

        """

        if txt[0][0] == '|' : self._write_utf(txt[0], 1, 0) 
        elif txt[0][0] == '`' : self._write_utf(" ", 1, 0)
        elif txt[0][2] == "\\" : self._write_utf(txt[0], 1, 0)                
        elif txt[0][2] == "::" : self._write_utf(txt[0], 1, 0)                        
        else: self._write_utf(txt[0], 1, 0)
        
    def _write_utf(self, mentry, pp, indent):
        """Write model text to utf-8 encoded file.
        
        ::

           arguments:
                mentry (string): text 
                pp (int): pretty print flag
                indent (int): indent flag
            
        """
        if indent: mentry = " "*4 + mentry
        if pp: mentry = pretty(mentry, use_unicode=True, num_columns=92)
        print(mentry, file=self.cfile)
        
    def _prt_run(self, dval):
        """Process run operations.
        ::

            options: script, os
            scripts are stored in resource subfolder
        """
        dval = self.fidict[refnum1[1]]
        #print('dval', dval)
        option = dval[0].strip()
        fpath = dval[1].strip()
        fp = os.path.abspath(fpath)
        var1 = dval[2].strip()
        var2 = dval[3].strip()
        var3 = dval[4]  # variable with edit lines
        if option == 'script':   # execute script in model namespace
            with open(fp, 'r') as f1:
                fr = f1.read()
            exec(fr, globals())
            link1 = "< ran python script : " + str(fpath) + " >"
            self.ew.errwrite(link1, 1)
            self.ew.errwrite("file: " + str(fp) + " executed", 0)
        elif option == 'os':     # execute operating system command
            os.system(fpath)
            link1 = "< execute command: " + str(fp) + " >"
            self.ew.errwrite(link1, 0)
            self.ew.errwrite('', 0)
        else:
            pass

    def _prt_ins(self, dval):
        """Insert file data into or from UTF calc        
       
        ::       
            
            [i]      p0    |   p1     |   p2      |   p3   |   p4         
                    'fig'     file       caption     size     location
                    'text'    file       reference        
                    'lit'     file       reference
                    'csv'     file       
                    'mod'     file      
                    'func'    file       var name   reference 
                    'read'    file       var name   vector or table
                    'write'   file       var name
                    'app'     file       var name
    
            only the first three letters of p0 are read
            
        """
                            
        option = dval[0].strip()[0:3]
        fname1 = dval[1].strip()
        caption1 = dval[2].strip()


        if option == 'fig':
            self._write_utf("figure | " + fname1 + " | " + caption1, 0, 1)

        """
        if option == 'text':
             # insert file from text into model, do not process
            with open(fpath, 'r') as f1:
                txstrng = f1.readlines()
            if var1.strip() != '':
                instxt = eval('txstrng[' + var1.strip() + ']')
                instxt = ''.join(instxt)
            else:
                instxt = ''.join(txstrng)

            self._write_utf(instxt, 0)

            link1 = "< text inserted from file: " + str(fpath) + " >"
            self.ew.errwrite(link1, 1)
            self.ew.errwrite('', 0)

        elif option == 'write':
            # write data to file, replace if exists
            sep1 = var2
            if sep1 == '':
                sep1 = ','
            elif sep1 == '*':
                sep1 = " "

            format1 = var3
            if format1 == '':
                format1 = '%s'

            file1 = open(fp, 'w')
            var11 = array(var1)
            var11.tofile(file1, sep=sep1, format=format1)
            file1.close()
            link1 = "< write variable " + var1 + " to file: " \
                    + str(fp) + ">"
            self.ew.errwrite(link1, 0)

        elif option == 'w+':
            # append data to file
            sep1 = var2
            if sep1 == '':
                sep1 = ','
            elif sep1 == '*':
                sep1 = " "

            format1 = var3
            if format1 == '':
                format1 = '%s'

            file1 = open(fp, 'a')
            var11 = array(var1)
            var11.tofile(file1, sep=sep1, format=format1)
            file1.close()
            link1 = "< append variable " + var1 + " to file: " \
                    + str(fp) + ">"
            self.ew.errwrite(link1, 0)

        elif option == 'figure':
            # insert figure reference in utf-8 document
            self.fignum += 1
            link1 = "< insert figure " + str(self.fignum) + '. ' \
                    + " file: " + str(fpath) + '>'
            self.ew.errwrite(link1, 0)
            link2 = "Figure " + str(self.fignum) + '. ' + var1 \
                    + " <file: " + str(fpath) + " >"
            self._write_utf(link2, 1)
            self._write_utf(" ", 0)

        elif option == 'model':
            # this option is handled in ModDicts.__init__
            # comodels are always processed first, regardless of location
            pass

        # absolute path specified for the following options
        elif option == 'read':
            self._prt_read(dval)

        else:
            pass
        """
        
    def _prt_val1(self, dval):
        """Print term description.
        ::

            key: _y + line number        
            _y :  p0                | p1
                 description    eqnum       
        
        """
        #print('dval_v1', dval)
        self._write_utf((dval[0] + " " + dval[1]).rjust(self.widthc-1), 0, 0)
        self._write_utf(" ", 0, 0)

    def _prt_val2(self, dval):
        """Print terms.
        ::

            key: _v + line number   
            _v :   p0  |   p1  |  p2      |    p3            
                 var     expr     statemnt   descrip            
        
        """
        #print('dval_v2', dval)        
        exec(dval[2])
        val1 = eval(dval[1])
        var1 = dval[2].split('=')[0].strip()
        state = var1 + ' = ' + str(val1)
        ptype = type(val1)
        if ptype == ndarray or ptype == list or ptype == tuple:
            state = var1 + ' = ' + '\n' + str(val1)
        shift = int(self.widthc / 2.5)
        ref = dval[3].strip().ljust(shift)
        if ptype == ndarray or ptype == list or ptype == tuple:
            self._write_utf(" "*2 + ref + " | " + state,  0, 0)
        else:
            self._write_utf(" "*2 + ref + " | " + state,  1, 0)

    def _prt_eq(self, dval):
        """print equations.
        ::
            
            key : _e + line number  
            value:  p0  |  p1     |  p2   |   p3    |  p4  | p5   |  p6  |  p7       
                     var   expr    state    descrip   dec1  dec2   unit   eqnum
        
        """   
        try:                                    # set decimal format
            eformat, rformat = str(dval[4]).strip(), str(dval[5]).strip()
            exec("set_printoptions(precision=" + eformat.strip() + ")")
            exec("Unum.VALUE_FORMAT = '%." + eformat.strip() + "f'")
        except:
            rformat = '3'
            eformat = '3'
            set_printoptions(precision=3)
            Unum.VALUE_FORMAT = "%.3f"
        cunit = dval[6].strip()
        var0  =  dval[0].strip()
        #print('dval_e', dval
        for k1 in self.odict:                   # evaluate values and equations
            if k1[0:2] in ['_v','_e']:
                    try: exec(self.odict[k1][2].strip())
                    except: pass       
        tmp = int(self.widthc-2) * '-'          # print horizontal line
        self._write_utf(" ", 0, 0)
        self._write_utf((u'\u250C' + tmp + u'\u2510').rjust(self.widthc), 1, 0)
        self._write_utf((dval[3] + "  " + dval[7]).rjust(self.widthc-1), 0, 0)
        self._write_utf(" ", 0, 0)
        for _j in self.odict:                   # print symbolic form
            if _j[0:2] in ['_v','_e']:
                #print(str(self.odict[_j][0]))
                varsym(str(self.odict[_j][0]))
        try:
            symeq = sympify(dval[1].strip())    # try sympy processing
            self._write_utf(symeq, 1, 0)
            self._write_utf(" ", 0, 0)
            self._write_utf(" ", 0, 0)
        except:
            self._write_utf(dval[1], 1, 0)      # otherwise write ASCII form
            self._write_utf(" ", 0, 0)
        try:                                    # substitute values                            
            symat = symeq.atoms(Symbol)
            for _n2 in symat:
                evlen = len((eval(_n2.__str__())).__str__())  # get var length
                new_var = str(_n2).rjust(evlen, '~')
                new_var = new_var.replace('_','|')
                symeq1 = symeq.subs(_n2, symbols(new_var))
            out2 = pretty(symeq1, wrap_line=False)
            #print('out2a\n', out2)
            symat1 = symeq1.atoms(Symbol)       # adjust character length
            for _n1 in symat1:                   
                orig_var = str(_n1).replace('~', '')
                orig_var = orig_var.replace('|', '_')
                try:
                    expr = eval((self.odict[orig_var][1]).split("=")[1])
                    if type(expr) == float:
                        form = '{:.' + eformat +'f}'
                        symeval1 = form.format(eval(str(expr)))
                    else:
                        symeval1 = eval(orig_var.__str__()).__str__()
                except:
                    symeval1 = eval(orig_var.__str__()).__str__()
                out2 = out2.replace(_n1.__str__(), symeval1)
            #print('out2b\n', out2)
            out3 = out2                             # clean up unicode 
            out3.replace('*', '\\u22C5') 
            #print('out3a\n', out3)
            _cnt = 0
            for _m in out3:
                if _m == '-':
                    _cnt += 1
                    continue
                else:
                    if _cnt > 1:
                        out3 = out3.replace('-'*_cnt, u'\u2014'*_cnt)
                    _cnt = 0
            #print('out3b \n', out3)
            self._write_utf(out3, 1, 0)               # print substituted form
            self._write_utf(" ", 0, 0)
        except:
            pass
        for j2 in self.odict:                         # restore units
            try:
                statex = self.odict[j2][2].strip()
                exec(statex)
            except:
                pass
        typev = type(eval(var0))                # print result right justified
        if typev == ndarray:
            tmp1 = eval(var0)
            self._write_utf((var0 + " = "), 1, 0)
            self._write_utf(' ', 0, 0)
            self._write_utf(tmp1, 0, 0)
        elif typev == list or typev == tuple:
            tmp1 = eval(var0)
            self._write_utf((var0 + " = "), 1)
            self._write_utf(' ', 0)
            plist1 = ppr.pformat(tmp1, width=40)
            self._write_utf(plist1, 0, 0)
        elif typev == Unum:
            exec("Unum.VALUE_FORMAT = '%." + rformat.strip() + "f'")
            if len(cunit) > 0:
                tmp = eval(var0).asU(eval(cunit))
            else:
                tmp = eval(var0)
            tmp1 = tmp.strUnit()
            tmp2 = tmp.asNumber()
            chkunit = str(tmp).split()
            #print('chkunit', tmp, chkunit)
            if len(chkunit) < 2: tmp1 = ''
            resultform = "{:,."+ rformat + "f}"
            result1 = resultform.format(tmp2)
            tmp3 = result1 + ' '  + tmp1
            self._write_utf((var0 + " = " + tmp3).rjust(self.widthc-1), 1, 0)
        else:
            if type(eval(var0)) == float or type(eval(var0)) == float64:
                resultform = "{:,."+rformat + "f}"
                result1 = resultform.format(eval(var0))
                self._write_utf((var0 +"="+
                                 str(result1)).rjust(self.widthc-1), 1, 0)
            else:
                    self._write_utf((var0 +"="+
                                     str(eval(var0))).rjust(self.widthc-1), 1, 0)
        tmp = int(self.widthc-2) * '-'           # print horizontal line
        self._write_utf((u'\u2514' + tmp + u'\u2518').rjust(self.widthc), 1, 0)
        self._write_utf(" ", 0, 0)

    def _prt_table(self, dval):
        """print arrays

        Dictionary:
        arrays: [[a], statement, expr, range1, range2,
                    ref, decimals, unit1, unit2, modnum, eqnum]
        
        """
        try:
            eformat, rformat = dval[6].split(',')
            exec("set_printoptions(precision=" + eformat.strip() + ")")
            exec("Unum.VALUE_FORMAT = '%." + eformat.strip() + "f'")
        except:
            rformat = '3'
            eformat = '3'
            set_printoptions(precision=3)
            Unum.VALUE_FORMAT = "%.3f"

        #print('array dval', dval)
        # table heading
        tmp = int(self.widthc-2) * '-'
        self._write_utf((u'\u250C' + tmp + u'\u2510').rjust(self.widthc), 0, 0)
        tleft = 'Table'
        self._write_utf((tleft + '  ' + dval[10]).rjust(self.widthc), 0, 0)
        self._write_utf(dval[5].strip().rjust(self.widthc-1), 0, 0)
        self._write_utf(' ', 0, 0)
        vect = dval[1:]
        # symbolic forms
        for _j in self.symb:
            if str(_j)[0] != '_':
                varsym(str(_j))
        # range variables
        try:
            var1 = vect[2].strip()
            var2 = vect[3].strip()
        except:
            pass
        # equation
        try:
            var0 = vect[0].split('=')[0].strip()
            var0s = varsym(var0)
            symeq = vect[0].split('=')[1].strip()
            symeq1 = sympify(symeq)
        except:
            pass
        # evaluate equation and array variables - keep units
        for k1 in self.odict:
            if k1[0] != '_' or k1[0:2] == '_a':
                    try: exec(self.odict[k1][3].strip())
                    except: pass
                    try: exec(self.odict[k1][4].strip())
                    except: pass
                    try: exec(self.odict[k1][1].strip())
                    except: pass
            #print(k1, eval(k1))
        # write explicit table
        if len(str(vect[2])) == 0 and len(str(vect[3])) == 0:
            ops = [' - ',' + ',' * ',' / ']
            _z1 = vect[0].split('=')[0].strip()
            cmd_str1 = _z1 + ' = array(' + vect[1] +')'
            exec(cmd_str1)

            cunit = dval[7]
            print('cunit', cunit)
            _rc = eval(_z1).tolist()

            # evaluate variables with units
            for inx in ndindex(eval(_z1).shape):
                print(21, type(_rc[inx[0]][inx[1]]),_rc[inx[0]][inx[1]] )
                try:
                    _fltn2a = _rc[inx[0]][inx[1]]
                    _fltn2b = _fltn2a.asU(eval(cunit))
                    _fltn2c = _fltn2b.asNumber()
                    _rc[inx[0]][inx[1]] = str(_fltn2c)
                except:
                    pass
            # evaluate numbers
            for inx in ndindex(eval(_z1).shape):
                try:
                    _fltn1 = float(_rc[inx[0]][inx[1]])
                    _rc[inx[0]][inx[1]] = _fltn1
                except:
                    pass
            # evaluate expressions
            for inx in ndindex(eval(_z1).shape):
                for _k in ops:
                    if _k in str(_rc[inx[0]][inx[1]]) :
                        _fltn2 = _rc[inx[0]][inx[1]]
                        _rc[inx[0]][inx[1]] = eval(_fltn2)
                        break
            # print table
            table2 = tabulate
            fltf = "." + eformat.strip() + "f"
            ptable = table2.tabulate(_rc[1:], _rc[0], 'rst', floatfmt=fltf)
            nstr = pretty(ptable, use_unicode=True, num_columns=92)
            self._write_utf(nstr, 1, 0)
            tmp = int(self.widthc-1) * '-'
            self._write_utf((u'\u2514' + tmp + u'\u2518').rjust(self.widthc), 0, 0)
            return
        # evaluate equation and array variables - strip units
        for k1 in self.odict:
            if k1[0] != '_' or k1[0:2] == '_a':
                    try: exec(self.odict[k1][3].strip())
                    except: pass
                    try: exec(self.odict[k1][4].strip())
                    except: pass
                    try: exec(self.odict[k1][1].strip())
                    except: pass
                    try:
                        state = self.odict[k1][1].strip()
                        varx = state.split('=')
                        state2 = varx[0].strip()+'='+varx[0].strip() + '.asNumber()'
                        exec(state2)
                        #print('j1', k1)
                    except:
                        pass
            #print(k1, eval(k1))
        # imported table
        if len(str(vect[1])) == 0:
            _a = eval(vect[0])
            # print table
            table2 = tabulate
            flt1 = "." + eformat.strip() + "f"
            ptable = table2.tabulate(_a[1:], _a[0], 'rst', floatfmt=flt1)
            nstr = pretty(ptable, use_unicode=True, num_columns=92)
            self._write_utf(nstr, 1)
            tmp = int(self.widthc-1) * '-'
            self._write_utf((u'\u2514' + tmp + u'\u2518').rjust(self.widthc), 0)
        # single row vector - 1D table
        elif len(str(vect[3])) == 0 and len(str(vect[0])) != 0:
            out1  =  var0s
            out1a =  symeq1
            out2  =  var1
            self._write_utf(" ",   0)
            self._write_utf("Variables: ",   0)
            self._write_utf("----------",    0)
            self._write_utf(' ', 0)
            self._write_utf(out2,  1)
            self._write_utf(' ',   0)
            self._write_utf(out1a, 1)
            self._write_utf(' ',   0)
            # process range variable 1
            rnge1 = vect[2]
            exec(rnge1.strip())
            rnge1a = rnge1.split('=')
            rlist = [vect[6].strip() + ' = ' +
                     str(_r) for _r in eval(rnge1a[1])]
            #print('rlist', rlist)
            #process equation
            equa1 = vect[0].strip()
            #print('equa1', equa1)
            exec(equa1)
            var2 = equa1.split('=')[0]
            etype = equa1.split('=')[1]
            elist1 = eval(var2)
            if etype.strip()[:1] == '[':
                # data is in list form
                elist2 = []
                alist1 = eval(equa1.split('=')[1])
                for _v in alist1:
                    try: elist2.append(list(_v))
                    except: elist2.append(_v)
            else:
                try: elist2 = elist1.tolist()
                except: elist2 = elist1
                elist2 = [elist2]
            #print('elist', elist2)
            # create table
            table1 = tabulate
            ptable = table1.tabulate(elist2, rlist, 'rst',
                                floatfmt="."+ eformat +"f")
            self._write_utf(ptable, 1)
            tmp = int(self.widthc-2) * '-'
            self._write_utf((u'\u2514' + tmp + u'\u2518').rjust(self.widthc), 0)
        # 2D table
        elif len(str(vect[3])) != 0 and len(str(vect[0])) != 0:
            out1  =  var0s
            out1a =  symeq1
            out2  =  var1
            out3  =  var2
            self._write_utf(" ",   0)
            self._write_utf("Variables: ",   0)
            self._write_utf("----------",    0)
            self._write_utf(" ", 0)
            self._write_utf(out2,  1)
            self._write_utf(' ',   0)
            self._write_utf(out3,  1)
            self._write_utf(" ",   0)
            self._write_utf(out1a, 1)
            self._write_utf(' ',   0)
            rnge1 = vect[2]                 # process range variable 1
            exec(rnge1.strip())
            rnge1a = rnge1.split('=')
            rlist = [vect[6].strip() + ' = ' +
                     str(_r) for _r in eval(rnge1a[1])]
            rnge2 = vect[3]                 # process range variable 2
            exec(rnge2.strip())
            rnge2a = rnge2.split('=')
            clist = [str(_r).strip() for _r in eval(rnge2a[1])]
            rlist.insert(0, vect[7].strip())
            equa1 = vect[0].strip()          # process equation
            exec(equa1)
            etype = equa1.split('=')[1]
            if etype.strip()[:1] == '[':
                # data is in list form
                #alist = []
                alist = eval(equa1.split('=')[1])
                #for _v in alist1:
                #    for _x in _v:
                #        print('_x', type(_x), _x)
                #       alist.append(list(_x))
            else:
                # data is in equation form
                equa1a = vect[0].strip().split('=')
                equa2 = equa1a[1]
                rngx = rnge1a[1]
                rngy = rnge2a[1]
                ascii1 = rnge1a[0].strip()
                ascii2 = rnge2a[0].strip()
                # format table
                alist = []
                for _y12 in eval(rngy):
                    alistr = []
                    for _x12 in eval(rngx):
                        eq2a = equa2.replace(ascii1, str(_x12))
                        eq2b = eq2a.replace(ascii2, str(_y12))
                        el = eval(eq2b)
                        alistr.append(el)
                    alist.append(alistr)
            for _n, _p in enumerate(alist):
                _p.insert(0, clist[_n])
            # print table
            table2 = tabulate
            flt1 = "." + eformat.strip() + "f"
            ptable = table2.tabulate(alist, rlist, 'rst', floatfmt=flt1)
            nstr = pretty(ptable, use_unicode=True, num_columns=92)
            self._write_utf(nstr, 1)
            tmp = int(self.widthc-1) * '-'
            self._write_utf((u'\u2514' + tmp + u'\u2518').rjust(self.widthc), 0)

    def _prt_sect(self, dval):
        """Print sections to UTF-8.
        ::

            key : value            
            _s :    p0         |       p1      |   p2       
                  left string    calc number     sect num   
        
        """
        self._write_utf('='*self.widthc, 0, 0)
        self._write_utf(" " + dval[0] + ((dval[1])+dval[2]).rjust(self.widthc -
                                               len(dval[0])-2), 1, 0)
        self._write_utf('='*self.widthc, 0, 0)


    def _prt_func(self, dval):
        """Print functions to UTF-8.
        ::

            arguments:
                dval (dictionary value): [[f], function call, var, ref, eqn number
        
        """
        # convert symbols to numbers - retain units
        for k1 in self.odict:
            if k1[0] != '_':
                try:
                    exec(self.odict[k1][1].strip())
                except:
                    pass
            if k1[0:2] == '_a':
                #print('ek1-2', k1, self.odict[k1])
                try:
                    exec(self.odict[k1][3].strip())
                    exec(self.odict[k1][4].strip())
                    exec(self.odict[k1][1].strip())
                except:
                    pass
        # print reference line
        tmp = int(self.widthc-2) * '-'
        self._write_utf((u'\u250C' + tmp + u'\u2510').rjust(self.widthc-1), 0)
        funcdescrip = dval[3].split(']')[1]
        strend = funcdescrip.strip() + ' ' + dval[4].strip()
        self._write_utf(strend.rjust(self.widthc - 1), 0)
        # evaluate function
        self._write_utf(" ", 0)
        self._write_utf('return variable: ' + dval[2].strip(), 0)
        self._write_utf(" ", 1)
        self._write_utf('function call: ' + dval[1].strip(), 0)
        funcname = dval[1].split('(')[0]
        docs1 = eval(funcname + '.__doc__')
        self._write_utf(' ', 0)
        self._write_utf('function doc:', 0)
        self._write_utf(docs1, 0)
        self._write_utf(' ', 0)
        #print(dval[1].strip())
        return1 = eval(dval[1].strip())
        if return1 is None:
            self._write_utf('function evaluates to None', 0)
        else:
            self._write_utf('function return: ', 0)
            self._write_utf(return1, 0)
        # add function variable to dict
        return2 = (return1.__repr__()).replace('\n', '')
        self.odict[dval[2]] = ['[z]', str(dval[2])+'='+return2]
        #print(self.odict[dval[2]])
        tmp = int(self.widthc-2) * '-'
        self._write_utf((u'\u2514' + tmp + u'\u2518').rjust(self.widthc), 0)
        self._write_utf(" ", 0)

    def _write_py(self):
        """write python code to file from dictionary
        ::

         write imports, terms, equations to Python importable file
         the following libraries are imported when the file is imported:
            os, sys
            sympy
            numpy and numpy.linalg
            unum and units
            
            [v]   p0  |  p1   |    p2    |    p3              
                  var    expr   statemnt    descrip 
    
            [e]   p0  |  p1    |    p2   |    p3      |  p4   |  p5   |  p6       
                 var     expr    statemnt    descrip     dec1    dec2     units 
            
            [t]   p0 |  p1  |  p2  |  p3  |  p4    |   p5   | p6   | p7  | p8
                  var  expr  state1  desc   range1   range2   dec1   un1   un2
            
            [s]   p0          |    p1          |       p2    |   p3           
                  left string    calc number     sect num      toc flag

        """
        pyfile1 = open(self.cfilepypath, 'w')
        str1 =  ('"""\nThis file contains Python equations from the '
                'on-c-e model \n\n  '+ self.mfile + '\n'
                '\nFor interactive analysis open the file\n'
                'in an interactive e.g. \n'
                'Spyder, Jupyter Notebook or Komodo IDE \n'
                '""" \n')
         
        str2 =  ('import os\n'
                'import sys\n'
                'from sympy import *\n'
                'from numpy import *\n'
                'import numpy.linalg as LA\n'
                'import importlib.util\n'
                'import once.config as cfg\n')
                                
        str2a = ('pypath = os.path.dirname(sys.executable)\n'
                'oncedir = os.path.join(pypath,"Lib","site-packages","once")\n'
                'cfg.opath = oncedir\n'
                'from once.calunit import *\n')

        vlist1 = []
        vlist2 = []
        str3a = str(os.getcwd()).replace("\\", "\\\\")
        str3 = "sys.path.append('" + str3a + "')"
        importstr = str1 + str2 + str2a + str3
        pyfile1.write(importstr + 2*"\n")
        pyfile1.write("# begin equations" + "\n")
        _vardef =[]
        for k1 in self.odict:               # write values and equations
            if k1[0:2] == '_e' or k1[0:2] == '_v':
                try:
                    exec(self.odict[k1][2].strip())
                    _vardef.append(self.odict[k1][2].strip() + "  #- " +
                                   self.odict[k1][3].strip())
                    vlist1.append(self.odict[k1][0].strip())
                    vlist2.append(self.odict[k1][3].strip())
                except:
                    pass
            if k1[0:2] == '_s':             # write section headings
                _vardef.append('#')
                _vardef.append('# section: '+self.odict[k1][0].strip())
        for il in _vardef:
            pyfile1.write(str(il) + '\n\n')
        vlen = len(vlist1)
        str4 = '[ '
        for ix in range(0,vlen):
            try: 
                for jx in range(3*ix, 3*ix+3):
                    str4 += "'" + str(vlist1[jx]) + "', "
                str4 += '\n'
            except:
                pass
        str4 += ']'
        
        str4a = '[ '
        for ix in range(0,vlen):
            try: 
                for jx in range(3*ix, 3*ix+3):
                    str4a += "'" + str(vlist2[jx]) + "', "
                str4a += '\n'
            except:
                pass
        str4a += ']'

        pyfile1.write('#\n# variables\nvlist1 = ' + str4 + '\n')
        pyfile1.write('#\n# variable definitions\nvlist2 = ' + str4a + '\n')

        str5 = ('\ndef vlist(vlistx = vlist1, vlisty= vlist2):\n'
                '   """Utility function for interactively listing once\n'
                '      variable values. Variables are stored in vlist1 and'
                '      definitions in vlist2. Type vlist()\n'
                '      to list updated variable summary after executing\n'
                '      calc Python script\n'
                '   """\n\n'
                '   for lsti in zip(vlistx, vlisty):\n'
                '       item1 = eval(str(lsti[0]))\n'
                '       def1 = lsti[1]\n'
                '       cncat1 = str(lsti[0]) + " = " + str(item1) + " "*30\n'
                '       print(cncat1[:25] + "# " + def1)\n\n'
                'if __name__ == "__main__":\n'
                '       vlist()'
                '       \n\n')
        
        pyfile1.write(str5 + "\n")
        pyfile1.close()
        
        for lsti in zip(vlist1, vlist2):
            item1 = eval(str(lsti[0]))
            def1 = lsti[1]
            cncat1 = str(lsti[0]) + " = " + str(item1) + " "*40
            cfg.varevaled += cncat1[:30] + "# " + def1 + "\n"
        
        
