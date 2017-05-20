#!

from __future__ import division
from __future__ import print_function
import codecs
import datetime
import sys
import os
import shutil
#import tabulate
import codecs
from numpy import *
import numpy.linalg as LA
from sympy import *
from sympy import var as varsym
from sympy import printing
from sympy.core.alphabets import greeks
import once
import once.config as cfg
from once.calcheck import ModCheck
from once.calpdf import *
from once.calunit import *
try:
    from PIL import Image as PImage
    from PIL import ImageOps as PImageOps
except:
    pass

__version__ = "0.9.0"
__author__ = 'rholland'

class CalcRST(object):
    """Write PDF file.
    ::

        Arguments:
            odict (ordered dict) : model dictionary
        
        Files written:
            _cfilepdf   : PDF calc file name  
            _rstfile    : reST file name     
            _texfile    : tex file name
            _auxfile    : auxiliary file name 
            _outfile    : out file name 
            _texmak2    : fls file name 
            _texmak3    : latexmk file name
    
        Operation keys, number of parameters and associated tags:
            _r + line number - 7 - [r] run 
            _i + line number - 6 - [i] insert
            _v + line number - 4 - [v] value            
            _e + line number - 7 - [e] equation
            _t + line number - 9 - [t] table
            _s + line number - 3 - [s] sectionsm,kl
            _~ + line number - 1 - blank line
            _x + line number - 2 - pass-through text
            _y + line number - 2 - value heading
            _lt              - 2 - license text [licensetext]
            _#              - 1 - control line
    
    
            [r]    p0   |   p1     |   p2    |   p3   |    p4   |   p5    
                  'os'     command     arg1      arg2      arg3     arg4 
                  'py'     script      arg1      arg2      arg3     arg4     
                 
            [i]    p0   |   p1     |  p2      |   p4      |   p5         
                  'fg'     figure     caption    size       location
                  'tx'     text     
                  'md'     model
                  'fn'     function   var name   reference 
                  'rd'     file       var name   vector or table
                  'wr'     file       var name
                        
            [v]   p0  |  p1   |    p2    |    p3              
                  var    expr   statemnt    descrip 
    
            [e]   p0  |  p1    |    p2   |    p3      |  p4   |  p5   |  p6       
                 var     expr    statemnt    descrip     dec1    dec2     units 
            
            [t]   p0 |  p1  |  p2  |  p3  |  p4    |   p5   | p6   | p7  | p8
                  var  expr  state1  desc   range1   range2   dec1   un1   un2
            
            [s]   p0          | p1         |        p2    |   p3           
                  left string    calc number     sect num   toc flag
    """


    def __init__(self, odict1):
        """Initialize parameters for UTF calc.
        ::

         Arguments:
            odict1 (dictionary):  model dictionary
        """
        # dicts and lists
        self.vbos = cfg.verboseflag
        self.el = ModCheck()
        self.odict = odict1
        self.symb = self.odict.keys()
        self.symblist = []

        # paths and files
        self.rfile = cfg.rstfile
        self.figpath = cfg.ipath
        #print('rest file name', cfg.rstfile)        
        self.rf1 = codecs.open(self.rfile, 'w', encoding='utf8')
        # parameters
        self.fignum = 0
        self.widthp = 70
        self.xtraline = False
        self.prfilename = ''
        self.previous = ''
        self.literalflag = 0


    def gen_rst(self):
        """ Parse model dictionary and write rst file.

        """
                
        self.xtraline = True
        for _i in self.odict:               # execute dictionary line by line
            mtag = _i[0:2]
            mvals = self.odict[_i]
            #print('rstmtag', mtag, _i, mvals, mvals[0])
            if mvals[2:9] == '#- page':                 #- add page break
                print(' ', file=self.rf1)
                print(".. raw:: latex", file=self.rf1)
                print(' ', file=self.rf1)
                print('  \\newpage', file=self.rf1)
                print(' ', file=self.rf1)
                self.el.logwrite("pdf new page", self.vbos)
            if mvals[2:4] == '#-':
                if isinstance(str(mvals.strip())[-1], int):       # add spaces
                    _numspace = eval(mvals.strip()[-1])
                    for _i in range(_numspace):
                        self._rst_blank()
            if mtag ==   '_r':                
                self._rst_run(self.odict[_i])
            elif mtag == '_i':
                self._rst_ins(self.odict[_i])
            elif mtag == '_v':
                self._rst_val2(self.odict[_i])
            elif mtag == '_e':
                self._rst_eq(self.odict[_i])
            elif mtag == '_t':
                self._rst_table(self.odict[_i])
            elif mtag == '_s':
                self._rst_sect(self.odict[_i])
                self.xtraline = False
            elif mtag == '_x':
                self._rst_txt(self.odict[_i])
                self.xtraline = False
            elif mtag == '_y':
                self._rst_val1(self.odict[_i])
                self.xtraline = False
            else:
                pass
            if mtag == '_~':
                self._rst_blnk()
                continue
            if self.xtraline:
                self._rst_blnk()
        
        if '_lt' in self.odict:                  # add calc license
            self._rst_txt(self.odict[_i2],0)
        #for _i in self.odict: print(i, self.odict[i])
        self._rst_terms()                         # add term definitions
        self._rst_blnk()
        self._rst_txt(['  **[end of calc]**'])  # end calc
        self.rf1.close()                          # close rst file
        self.el.logwrite("< reST file written >", self.vbos)


    def _rst_txt(self, txt):
        """Print pass-through text.
          arguments:
            txt (string): text that is not part of an tag

        """
        #print('txt ',txt)
        if txt[0][0:3] == '  |' :                       # handle lines
            print(txt[0][2:].rstrip(), file=self.rf1)
            self.xtraline = False
        elif txt[0][0:3] == '  `' :                     # handle literal
            if self.literalflag == 2:
                self.literalflag = 0
            if self.literalflag == 1:
                self.literalflag = 2
            print('  ', file=self.rf1)
            self.xtraline = False     
        elif txt[0][0:4] == '  ::' :                    # handle literal
            print(txt[0][2:].rstrip(), file=self.rf1)
            self.literalflag = 1
            self.xtraline = False        
        elif txt[0][0:4] == '  ..' :                    # handle raw
            print(txt[0][2:].rstrip(), file=self.rf1)                
            self.xtraline = False        
        else:
            print(txt[0][2:].rstrip(), file=self.rf1)
            self.xtraline = True


    def _rst_blnk(self):
        """Print blank line.

        """
        if self.literalflag == 2:                       # handle literal
            print('  ', file=self.rf1)
            self.xtraline = False     
        else:
            print('  ', file=self.rf1)
            print(".. raw:: latex", file=self.rf1)
            print('  ', file=self.rf1)
            print('   \\vspace{3mm}', file=self.rf1)
            print('  ', file=self.rf1)
            print('  ', file=self.rf1)


    def _rst_run(self, dval2):

        """        

            [r]   p0 |   p1   |   p2     |   p3    |   p4   |    p5   |   p6    
                        'os'     command     arg1      arg2      arg3     arg4 
                        'py'     script      arg1      arg2      arg3     arg4     
        """
        pass

    
    def _rst_ins(self, dval2):
        """Insert file data into or from reST        
            
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
        option = ""
        fpath = ""
        fp = ""
        var2 = ""
        var3 = "100"
        var4 = "center"
                            
        option = dval2[0].strip()[0:3]
        fname = dval2[1].strip()
        fp =  os.path.join(self.figpath,fname)
        var2 = dval2[2].strip()
        var3 = dval2[3].strip()
        var4 = dval2[4].strip()

        if option == 'fig':
            if var4[0:1] == 'r' : var4 = 'right'
            elif var4[0:1] == 'l' : var4 = 'left'
            elif var4[0:1] == 'c' : var4 = 'center'            
            else: var4 = 'center'
            print(' ', file=self.rf1)
            print('.. figure:: ' + fp, file=self.rf1)
            print('   :width: ' + var3 + ' %', file=self.rf1)
            print('   :align: ' + var4, file=self.rf1)
            print('   ', file=self.rf1)
            print('   ' + var2, file=self.rf1)
            print(' ', file=self.rf1)
            self.el.logwrite("< figure "+fname+" added to TeX >", self.vbos)

            
    def _rst_val1(self, dval2):
        """Print value description to reST.
            key: values        
            _y :  p0                | p1
                 block description    eqnum       
        """
        #print('dval2', dval2)

        descrip = dval2[0].strip()
        eqnum = dval2[1].strip()
        # equation reference line
        print('  ', file=self.rf1)
        print(".. raw:: latex", file=self.rf1)
        print('  ', file=self.rf1)
        print('   \\vspace{7mm}', file=self.rf1)
        print('  ', file=self.rf1)
        print('   \\hfill\\textbf{'+descrip+ ' ' +eqnum +'}', file=self.rf1)
        print('  ', file=self.rf1)


    def _rst_val2(self, dval2):
        """Print values to reST:
        
            key: values    
            _v :   p0  |   p1  |  p2      |    p3            
                 var     expr     statemnt   descrip     
                 
        """
        val1 = eval(dval2[1])
        ptype = type(val1)
        var1 = dval2[0].strip()
        state = var1 + ' = ' + str(val1)
        shift = int(self.widthp / 2.0)
        ref = dval2[3].strip().ljust(shift)
        valuepdf = " "*4 + ref + ' | ' + state
        if ptype == ndarray or ptype == list or ptype == tuple:
            shift = int(self.widthp / 2.1)
            ref = dval2[3].strip().ljust(shift)
            tmp1 = str(val1)
        if ptype == ndarray:
            if '[[' in tmp1:
                tmp2 = tmp1.replace(' [', '.  [')
                tmp1 = tmp2.replace('[[', '. [[')
            else:
                tmp1 = tmp1.replace('[', '. [')
            valuepdf = '. ' + ref + ' | ' + var1 + ' = ' + tmp1
        elif ptype == list or ptype == tuple:
            if ']]' in tmp1:
                tmp1 = tmp1.replace(']]', ']]\n')
            else:
                tmp1 = tmp1.replace(']', ']\n')
            valuepdf = '. ' + ref + ' | ' + var1 + ' = ' + tmp1
        print('  ', file=self.rf1)
        print('::', file=self.rf1)
        print('  ', file=self.rf1)
        print(valuepdf, file=self.rf1)
        print('  ', file=self.rf1)
        print('  ', file=self.rf1)


    def _rst_eq(self, dval):
        """Print equation to reST:
        
            key : _e + line number  
            value:  p0  |  p1     |  p2   |   p3    |  p4  | p5   |  p6  |  p7       
                    var   expr      state    descrip   dec1  dec2   unit   eqnum

        """
        try:                                # set decimal format
            eformat, rformat = str(dval[4]).strip(), str(dval[5]).strip()
            exec("set_printoptions(precision=" + eformat.strip() + ")")
            exec("Unum.VALUE_FORMAT = '%." + eformat.strip() + "f'")
            #print('eformat',eformat, rformat)
        except:
            eformat = '3'
            rformat = '3'
            set_printoptions(precision=3)
            Unum.VALUE_FORMAT = "%.3f"
        try:        
            eunit = dval[6].strip()
            #print('eunit', eunit)
        except:
            eunit = ' '
        var0 = dval[0].strip()
        for k1 in self.odict:                  # evaluate values and equations      
            if k1[0:2] in ['_v','_e']:
                    try:
                        exec(self.odict[k1][2].strip())
                    except:
                        pass  
        descrip = dval[3].strip()              # equation reference line
        eqnum = dval[7].strip()
        print('  ', file=self.rf1)
        print(".. raw:: latex", file=self.rf1)
        print('  ', file=self.rf1)
        print('   \\vspace{7mm}', file=self.rf1)
        print('  ', file=self.rf1)
        print('   \\hfill\\textbf{'+descrip+ ' ' +eqnum +'}', file=self.rf1)
        print('  ', file=self.rf1)
        for _j in self.odict:                       # symbolic form
            if _j[0:2] in ['_v','_e']:
                #print(str(self.odict[_j][0]))
                varsym(str(self.odict[_j][0]))
        try:                                        # try sympy processing
            symeq = sympify(dval[1].strip())
            print('  ', file=self.rf1)
            print(".. raw:: latex", file=self.rf1)
            print('  ', file=self.rf1)
            print('   \\vspace{3mm}', file=self.rf1)
            print('  ', file=self.rf1)
            print('.. math:: ', file=self.rf1)
            print('  ', file=self.rf1)
            print('  ' + latex(symeq, mul_symbol="dot"), file=self.rf1)
            print('  ', file=self.rf1)
            print(".. raw:: latex", file=self.rf1)
            print('  ', file=self.rf1)
            print('   \\vspace{4mm}', file=self.rf1)
            print('  ', file=self.rf1)
        except:                                    # otherwise write ASCII form
            symeq = dval[1].strip()
            print('  ', file=self.rf1)
            print('::', file=self.rf1)
            print('  ', file=self.rf1)
            print('  ' + symeq, file=self.rf1)
            print('  ', file=self.rf1)
        try:                                # substitute values for variables
            symat = symeq.atoms(Symbol)
            latexrep = latex(symeq, mul_symbol="dot")
            #print('latex1', latexrep)
            switch1 = []
            for _n in symat:              # rewrite latex equation with braces
                #print('_n1', _n)
                newlatex1 = str(_n).split('__')
                if len(newlatex1) == 2:
                    newlatex1[1] += '}'
                    newlatex1 = '~d~'.join(newlatex1)
                newlatex1 = str(_n).split('_')
                if len(newlatex1) == 2:
                    newlatex1[1] += '}'
                    newlatex1 = '~s~'.join(newlatex1)
                newlatex1 = ''.join(newlatex1)
                newlatex1 = newlatex1.replace('~d~', '__{')
                newlatex1 = newlatex1.replace('~s~', '_{')
                #print('newlatex1', newlatex1)
                switch1.append([str(_n), newlatex1])
            for _n in switch1:                    
                #print('_n2', _n)
                expr1 = eval(_n[0])
                if type(expr1) == float:                # set sub decimal points
                    form = '{:.' + eformat.strip() +'f}'
                    symvar1 = '{' + form.format(expr1) + '}'
                else:
                    symvar1 = '{' + str(expr1) + '}'
                #print('replace',_n[1], symvar1)
                latexrep = latexrep.replace(_n[1], symvar1)
                latexrep = latexrep.replace("\{", "{")
                #print('latex2', latexrep)
            print('  ', file=self.rf1)                  # add equation to rst file
            print('.. math:: ', file=self.rf1)
            print('  ', file=self.rf1)
            print('  ' + latexrep, file=self.rf1)
            print('  ', file=self.rf1)
            print(".. raw:: latex", file=self.rf1)
            print('  ', file=self.rf1)
            print('   \\vspace{1mm}', file=self.rf1)
            print('  ', file=self.rf1)
            print('  ', file=self.rf1)
        except:
            pass
        for j2 in self.odict:                           # restore units
            try:
                statex = self.odict[j2][2].strip()
                exec(statex)
            except:
                pass
        var3s = var0.split('_')                        
        if var3s[0] in greeks:                          # result var to greek
            var3g = "\\" + var0
        else:
            var3g = var0
        typev = type(eval(var0))
        #print('typev', typev)
        print1 = 0                                      # format result printing
        if typev == ndarray:
            print1 = 1
            tmp1 = str(eval(var0))
            if '[[' in tmp1:
                tmp2 = tmp1.replace(' [', '.  [')
                tmp1 = tmp2.replace('[[', '. [[')
            else:
                tmp1 = tmp1.replace('[', '. [')
        elif typev == list or typev == tuple:
            print1 = 1
            tmp1 = str(eval(var0))
            if '[[' in tmp1:
                tmp2 = tmp1.replace(' [', '.  [')
                tmp1 = tmp2.replace('[[', '. [[')
                tmp1 = tmp1.replace('],', '],\n')
            else:
                tmp1 = tmp1.replace('[', '. [')
                tmp1 = tmp1.replace('],', '],\n')
        elif typev == Unum:
            print1 = 2
            exec("Unum.VALUE_FORMAT = '%." + rformat.strip() + "f'")
            if len(eunit) > 0:
                tmp = eval(var0).asU(eval(eunit))
            else:
                tmp = eval(var0)
            tmp1 = tmp.strUnit()
            tmp2 = tmp.asNumber()
            chkunit = str(tmp).split()
            #print('chkunit', tmp, chkunit)
            if len(chkunit) < 2:
                tmp1 = ''
            resultform = "{:,."+rformat + "f}"
            result1 = resultform.format(tmp2)
            tmp3 = var0 +"="+ result1 + ' '  + tmp1
        else:
            print1 = 2
            if type(eval(var0)) == float or type(eval(var0)) == float64:
                resultform = "{:,."+rformat + "f}"
                result1 = resultform.format(eval(var0))
                tmp3 = var0 +"="+ result1
            else:
                tmp3 = var0 +"="+ str(eval(var0))
        if print1 == 1:                                 # for lists and arrays
            print('  ', file=self.rf1)
            print('::', file=self.rf1)
            print('  ', file=self.rf1)
            print('. ' + var0 + ' = ', file=self.rf1)
            print(tmp1, file=self.rf1)
            print('  ', file=self.rf1)
            print(".. raw:: latex", file=self.rf1)
            print('  ', file=self.rf1)
            print('   \\vspace{4mm}', file=self.rf1)
            print('  ', file=self.rf1)       
        if print1 == 2:                                 # add space at units
            try: 
                result2 = latex(tmp3).split()
                tmp3 = ''.join(result2[:-2]) + ' \ '.join(result2[-2:])
            except:
                pass
            #print(' ', file=self.rf1)
            #print('.. math:: ', file=self.rf1)
            #print('  ', file=self.rf1)
            #print("  {" + latex(tmp3, mode='plain') + "}", file=self.rf1)
            print('  ', file=self.rf1)
            print(".. raw:: latex", file=self.rf1)
            print('  ', file=self.rf1)
            print('   \\hfill{\\underline{'+tmp3 +'}}', file=self.rf1)
            print('  ', file=self.rf1)
        print(".. raw:: latex", file=self.rf1)
        print('  ', file=self.rf1)
        print('   \\vspace{8mm}', file=self.rf1)
        print('  ', file=self.rf1)

        
    def _rst_table(self, dval):
        """Print table to reStructuredText:
        
            _t + line number - 9 - [t] table
            
            [t]   p0 |  p1  |  p2  |  p3  |  p4    |   p5   | p6   | p7  | p8
                        var  state1  desc   range1   range2   dec1   un1   un2
        """
        try:
            eformat, rformat = dval[6].split(',')
            exec("set_printoptions(precision=" + eformat + ")")
            exec("Unum.VALUE_FORMAT = '%." + eformat + "f'")
        except:
            eformat = '3'
            rformat = '3'
            set_printoptions(precision=3)
            Unum.VALUE_FORMAT = "%.3f"
            Unum.VALUE_FORMAT = "%.3f"
        # table heading
        vect = dval[1:]
        eqnum = dval[10].strip()
        tablehdr = 'Table  ' + eqnum
        print(".. raw:: latex", file=self.rf1)
        print('  ', file=self.rf1)
        print('   \\vspace{7mm}', file=self.rf1)
        print('  ', file=self.rf1)
        print("aaxbb " + "**" + tablehdr + "**", file=self.rf1)
        print('  ', file=self.rf1)
        ref5 = dval[5].strip()
        if ref5 != '':
            print(".. raw:: latex", file=self.rf1)
            print('  ', file=self.rf1)
            print('   \\hfill\\text{' + ref5 + '}', file=self.rf1)
            print('   \\begin{flushleft}', file=self.rf1)
            print('  ', file=self.rf1)
            print('   \\end{flushleft}', file=self.rf1)
            print('  ', file=self.rf1)
        # draw horizontal line
        #print('  ', file=self.rf1)
        #print(".. raw:: latex", file=self.rf1)
        #print('  ', file=self.rf1)
        #print('   \\vspace{-1mm}', file=self.rf1)
        #print('  ', file=self.rf1)
        #print('   \\hrulefill', file=self.rf1)
        #print('  ', file=self.rf1)
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
            symeq = vect[0].split('=')[1].strip()
        except:
            pass
        # evaluate equation and array variables - keep units
        for k1 in self.odict:
            if k1[0] != '_' or k1[0:2] == '_a':
                    try:
                        exec(self.odict[k1][3].strip())
                    except:
                        pass
                    try:
                        exec(self.odict[k1][4].strip())
                    except:
                        pass
                    try:
                        exec(self.odict[k1][1].strip())
                    except:
                        pass
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
            print(ptable, file=self.rf1)
            print('  ', file=self.rf1)
            return
        # evaluate variables - strip units for arrays
        for k1 in self.odict:
            #print('k1', k1)
            if k1[0] != '_':
                    try:
                        exec(self.odict[k1][1].strip())
                    except:
                        pass
                    try:
                        state = self.odict[k1][1].strip()
                        varx = state.split('=')
                        state2 = varx[0].strip()+'='\
                        +varx[0].strip() + '.asNumber()'
                        exec(state2)
                        #print('j1', k1)
                    except:
                        pass
            if k1[0:2] == '_a':
                #print('k1-2', k1)
                try:
                    exec(self.odict[k1][3].strip())
                    exec(self.odict[k1][4].strip())
                    exec(self.odict[k1][1].strip())
                except:
                    pass
        # imported table
        if len(str(vect[1])) == 0:
            _a = eval(vect[0])
            # print table
            table2 = tabulate
            flt1 = "." + eformat.strip() + "f"
            ptable = table2.tabulate(_a[1:], _a[0], 'rst', floatfmt=flt1)
            print(ptable, file=self.rf1)
            print('  ', file=self.rf1)
        # explicit table
        elif len(str(vect[2])) == 0 and len(str(vect[3])) == 0:
            ops = [' - ',' + ',' * ',' / ']
            _a1 = vect[0].split('=')[0].strip()
            cmd_str1 = _a1 + ' = array(' + vect[1] +')'
            exec(cmd_str1)
            _z1 = vect[0].split('=')[0].strip()
            cmd_str1 = _z1 + ' = array(' + vect[1] +')'
            #print(cmd_str1)
            exec(cmd_str1)
            _rc = eval(_z1).tolist()
            # evaluate numbers
            for inx in ndindex(eval(_z1).shape):
                try:
                    _fltn1 = float(_rc[inx[0]][inx[1]])
                    _rc[inx[0]][inx[1]] = _fltn1
                except:
                    pass
                #print('chk1', inx, _a[inx[0]][inx[1]])
            # evaluate expressions
            for inx in ndindex(eval(_z1).shape):
                for _k in ops:
                        if _k in str(_rc[inx[0]][inx[1]]) :
                            _fltn2 = _rc[inx[0]][inx[1]]
                            _rc[inx[0]][inx[1]] = eval(_fltn2)
                            break
            # print table
            table2 = tabulate
            flt1 = "." + eformat.strip() + "f"
            ptable = table2.tabulate(_rc[1:], _rc[0], 'rst', floatfmt=flt1)
            print(ptable, file=self.rf1)
            print('  ', file=self.rf1)
        # single row vector - 1D table
        elif len(str(vect[3])) == 0 and len(str(vect[0])) != 0:
            # process range variable 1 and heading
            symeq1 = sympify(symeq)
            print('  ', file=self.rf1)
            print('.. raw:: latex', file=self.rf1)
            print('  ', file=self.rf1)
            print('   \\vspace{2mm}', file=self.rf1)
            print('  ', file=self.rf1)
            print('  Variables:', file=self.rf1)
            print('  ', file=self.rf1)
            print('   \\vspace{1mm}', file=self.rf1)
            print('  ', file=self.rf1)
            print('  ' + latex(var1, mul_symbol="dot"), file=self.rf1)
            print('  ', file=self.rf1)
            print('   \\vspace{1mm}', file=self.rf1)
            print('  ', file=self.rf1)
            print('.. math:: ', file=self.rf1)
            print('  ', file=self.rf1)
            print('  ' + latex(symeq1, mul_symbol="dot"), file=self.rf1)
            print('  ', file=self.rf1)
            rnge1 = vect[2]
            exec(rnge1.strip())
            rnge1a = rnge1.split('=')
            rlist = [vect[6].strip() + ' = ' +
                     str(_r)for _r in eval(rnge1a[1])]
            #process equation
            equa1 = vect[0].strip()
            #print(equa1)
            exec(equa1)
            var2 = equa1.split('=')[0]
            etype = equa1.split('=')[1]
            elist1 = eval(var2)
            if etype.strip()[:1] == '[':
                # data is in list form
                #elist2 = []
                elist2 = eval(equa1.split('=')[1])
                # for _v in alist1:
                #         try:
                #             elist2.append(list(_v))
                #         except:
                #             elist2.append(_v)
            else:
                try:
                    elist2 = elist1.tolist()
                except:
                    elist2 = elist1

                elist2 = [elist2]
            # create 1D table
            ptable = tabulate.tabulate(elist2, rlist, 'rst',
                                floatfmt="."+eformat.strip()+"f")
            print(ptable, file=self.rf1)
            print('  ', file=self.rf1)
            #print(ptable)
        # 2D table
        elif len(str(vect[3])) != 0 and len(str(vect[0])) != 0:
            symeq1 = sympify(symeq)
            print('  ', file=self.rf1)
            print('.. raw:: latex', file=self.rf1)
            print('  ', file=self.rf1)
            print('   \\vspace{2mm}', file=self.rf1)
            print('  ', file=self.rf1)
            print('  Variables:', file=self.rf1)
            print('  ', file=self.rf1)
            print('   \\vspace{1mm}', file=self.rf1)
            print('  ', file=self.rf1)
            print('  ' + latex(var1, mul_symbol="dot"), file=self.rf1)
            print('  ', file=self.rf1)
            print('   \\vspace{2mm}', file=self.rf1)
            print('  ', file=self.rf1)
            print('  ' + latex(var2, mul_symbol="dot"), file=self.rf1)
            print('  ', file=self.rf1)
            print('.. math:: ', file=self.rf1)
            print('  ', file=self.rf1)
            print('   \\vspace{4mm}', file=self.rf1)
            print('  ', file=self.rf1)
            print('  ' + latex(symeq1, mul_symbol="dot"), file=self.rf1)
            print('  ', file=self.rf1)
            # process range variable 1
            rnge1 = vect[2]
            exec(rnge1.strip())
            rnge1a = rnge1.split('=')
            rlist = [vect[6].strip() + ' = ' +
                     str(_r) for _r in eval(rnge1a[1])]
            # process range variable 2
            rnge2 = vect[3]
            exec(rnge2.strip())
            rnge2a = rnge2.split('=')
            clist = [str(_r).strip() for _r in eval(rnge2a[1])]
            rlist.insert(0, vect[7].strip())
            # process equation
            equa1 = vect[0].strip()
            #print('equa1', equa1)
            exec(equa1)
            etype = equa1.split('=')[1]
            if etype.strip()[:1] == '[':
                # data is in list form
                #alist = []
                alist = eval(equa1.split('=')[1])
                #print('alist1', alist1)
                # for _v in alist1:
                #     for _x in _v:
                        #print('_x', _x)
                #         alist.append(list(_x))
                        #print('append', alist)
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
                    #print('append', alist)

            for _n, _p in enumerate(alist):  _p.insert(0, clist[_n])
            # create 2D table
            flt1 = "." + eformat.strip() + "f"
            #print(alist)
            ptable = tabulate.tabulate(alist, rlist, 'rst', floatfmt=flt1)
            print(ptable, file=self.rf1)
            print('  ', file=self.rf1)


    def _rst_sect(self, dval):
        """Print section title to reST.
        
        ::
    
           _s :    p0         |       p1      |   p2        
                  left string    calc number     sect num   
       
        """        
        tleft = dval[0].strip()
        tright = dval[1].strip() + dval[2].strip()
        print(' ', file=self.rf1)
        print(".. raw:: latex", file=self.rf1)
        print(' ', file=self.rf1)
        print('   \\vspace{3mm}', file=self.rf1)
        print(' ', file=self.rf1)
        print(' ', file=self.rf1)
        print(tleft.strip() + "aaxbb " + tright.strip(),file=self.rf1)
        print("-" * self.widthp, file=self.rf1)
        print(' ', file=self.rf1)
        print(' ', file=self.rf1)
        print(".. raw:: latex", file=self.rf1)
        print(' ', file=self.rf1)
        print('   \\vspace{1mm}', file=self.rf1)
        print(' ', file=self.rf1)

    
    def _rst_terms(self):
        """Print section with term definitions to reST:
      
            key: values    
            _v :   p0  |   p1  |  p2      |    p3            
                 var     expr     statemnt   descrip     

            key : _e  
            value:  p0  |  p1     |  p2   |   p3    |  p4  | p5   |  p6  |  p7       
                    var   expr      state    descrip   dec1  dec2   unit   eqnu 
        
        """
        taglist =[]
        for _i in self.odict:
            mtag = _i[0:2]
            taglist.append(mtag)
        if ('_v' or '_e') in taglist:        
            tleft = "AST Variables and Definitions"
            print(' ', file=self.rf1)
            print(".. raw:: latex", file=self.rf1)
            print(' ', file=self.rf1)
            print('   \\vspace{3mm}', file=self.rf1)
            print(' ', file=self.rf1)
            print(' ', file=self.rf1)
            print(tleft.strip(),file=self.rf1)
            print("-" * self.widthp, file=self.rf1)
            print(' ', file=self.rf1)
            print(' ', file=self.rf1)
            print(".. math::", file=self.rf1) 
            print(' ', file=self.rf1)            
            print('  \\begin{align}', file=self.rf1)
            cnt = 0
            for _i in self.odict:            # execute dictionary line by line
                if _i[0:2] in ['_v','_e']:
                    cnt += 1
                    if cnt == 35:
                        print('  \\end{align}', file=self.rf1)
                        print(' ', file=self.rf1)
                        print(' ', file=self.rf1)
                        print(".. math::", file=self.rf1) 
                        print(' ', file=self.rf1)            
                        print('  \\begin{align}', file=self.rf1)
                        cnt = 0
                    mvals = self.odict[_i]
                    varstring1 = "  \\bm{" + str(mvals[0]) + "} "
                    varstring2 = "&= \\textrm{" + str(mvals[3]) + "}\\\\"
                    print(varstring1 + varstring2, file=self.rf1)
                    #print('rstmtag', mtag, _i, mvals, mvals[0])
            print('  \\end{align}', file=self.rf1)
            print(' ', file=self.rf1)
        else:
            pass


class CalcPDF(object):
    """write PDF calc from rst file
    
    """

    def __init__(self):
        """Initialize rst, tex and pdf file paths.

        """
        self.vbos = cfg.verboseflag
        self.el = ModCheck()
        self.mfile = cfg.mfile
        #print('mfile', self.mfile)
        self.xpath = cfg.xpath
        self.ppath = cfg.ppath
        self.cpath = cfg.cpath
        self.pdffile = cfg.cfilepdf
        self.rfile = cfg.rstfile
        self.texfile = cfg.texfile
        self.rpath = cfg.rpath
        self.calctitle = cfg.calctitle
        self.texfile2 = os.path.join(cfg.xpath, self.texfile)
        self.auxfile =  os.path.join(cfg.xpath, cfg.mbase + '.aux')
        self.outfile =  os.path.join(cfg.xpath, cfg.mbase + '.out')
        self.texmak2 =  os.path.join(cfg.xpath, cfg.mbase + '.fls')
        self.texmak3 =  os.path.join(cfg.xpath, cfg.mbase + '.fdb_latexmk')
        self.stylepathpdf = os.path.join(once.__path__[0],'once.sty')
        
    def gen_tex(self):
        """Generate tex file and call mod_tex.

        """
        #print("gen_tex1")
        fixstylepath = self.stylepathpdf.replace('\\', '/')
        try:
            pypath = os.path.dirname(sys.executable)
            rstexec = os.path.join(pypath,"Scripts","rst2latex.py")
            with open(rstexec) as f1:
                f1.close()
            pythoncall = 'python '
            #print("< rst2latex path 1> " + rstexec)
        except:
            try:
                pypath = os.path.dirname(sys.executable)
                rstexec = os.path.join(pypath,"rst2latex.py")
                with open(rstexec) as f1:
                    f1.close()
                pythoncall = 'python '
                #print("< rst2latex path 2> " + rstexec)
            except:
                rstexec = "/usr/local/bin/rst2latex.py"
                pythoncall = 'python '
                #print("< rst2latex path 3> " + rstexec)
        tex1 = "".join([pythoncall, rstexec
                        ,
                        " --documentclass=report ",
                        " --documentoptions=12pt,notitle,letterpaper",
                        " --stylesheet=",
                        fixstylepath + " ", self.rfile + " ", self.texfile2])
        self.el.logwrite("tex call:\n" + tex1, self.vbos)
        try:
            os.system(tex1)
            self.el.logwrite("< TeX file written >", self.vbos)
        except:
            print()
            self.el.logwrite("< error in docutils writer call >", self.vbos)
        
        self.mod_tex(self.texfile2)


    def mod_tex(self, tfile):
        """Modify TeX file to avoid problems with escapes:

            - Modifies the marker "aaxbb " inserted by once with
              \\hfill which is not handled well by reST.
            - Deletes inputenc package
            - Modifies title section and adds table of contents
            
        """
        with open(tfile, 'r') as texin:
            texf = texin.read()
        texf = texf.replace("""inputenc""", """ """)
        texf = texf.replace("aaxbb ", """\\hfill""")
        if texf.find("phantom") > -1:
            texf = texf.replace("""\\begin{document}""", '')
            texf = texf.replace("""\\maketitle""", '')
            texf = texf.replace("""\\title{\\phantomsection%""",
                                """\\renewcommand{\contentsname}{""" +
                                self.calctitle + "}\n" +
                                """\\begin{document}""" + "\n" +
                                """\\tableofcontents"""
                                """\\chapter{%""")
        else:
            texf = texf.replace("""\\begin{document}""",
                                """\\renewcommand{\contentsname}{""" +
                                self.calctitle + "}\n" +
                                """\\begin{document}""" + "\n" +
                                """\\tableofcontents""")    
        with open (tfile, 'w') as texout:
            print(texf, file=texout)


    def gen_pdf(self):
        """Write PDF file from tex file.

        """
        os.chdir(self.xpath)
        if os.path.isfile(os.path.join(self.ppath,self.pdffile)):
            os.remove(os.path.join(self.ppath,self.pdffile))
        pdf1 ='latexmk -xelatex -quiet -f '+os.path.join(self.xpath,self.texfile)
        #print("pdf call:  ", pdf1)
        self.el.logwrite("< PDF calc written >", self.vbos)    
        os.system(pdf1)
        pdfname = self.pdffile
        pdfname = list(pdfname)
        pdfname[0]='m'
        pdfname2 = "".join(pdfname)
        pdfftemp = os.path.join(self.xpath, pdfname2)
        pdffnew = os.path.join(self.cpath, self.pdffile)
        try:
            os.remove(pdffnew)
        except:
            pass
        try:
            os.rename(pdfftemp, pdffnew)
        except:    
            self.el.logwrite("< PDF calc not moved from temp >", 1)
        tocname2 = pdfname2.replace('.pdf','.toc')
        toctemp = os.path.join(self.xpath, tocname2)
        tocnew = os.path.join(self.rpath, tocname2)
        try:
            shutil.copyfile(toctemp, tocnew)
        except:    
            self.el.logwrite("< TOC not moved from temp >", 1)


    def reprt_list(self):
        """Append calc name to reportmerge.txt
        
        """
        try: 
            filen1 = os.path.join(self.rpath, "reportmerge.txt")
            print(filen1)
            file1 = open(filen1, 'r')
            mergelist = file1.readlines()
            file1.close()
            mergelist2 = mergelist[:]
        except OSError:
            print('< reportmerge.txt file not found in reprt folder >')
            return
        calnum1 = self.pdffile[0:5]
        file2 = open(filen1, 'w')
        newstr1 = 'c | ' +  self.pdffile  + ' | ' + self.calctitle
        for itm1 in mergelist:
            if calnum1 in itm1:
                indx1 = mergelist2.index(itm1)
                mergelist2[indx1] = newstr1
                for j1 in mergelist2: file2.write(j1)
                file2.close()
                return
        mergelist2.append("\n" + newstr1)
        for j1 in mergelist2: file2.write(j1)
        file2.close()
        return
                
            
            
        
            
            
            