from __future__ import division
from __future__ import print_function
import os
import tabulate
import codecs
import oncepy
import oncepy.oconfig as cfg
from oncepy import ccheck
from oncepy import oconfig as cfg
from numpy import *
from numpy import linalg as LA
import numpy.linalg as linalg
from sympy import *
from sympy import var as varsym
from sympy.core.alphabets import greeks

mpathcrst = os.getcwd()
try:
    from unitc import *
    cfg.unitfile = 'model folder'
except ImportError:
    try:
        os.chdir(os.pardir)
        from unitc import *
        cfg.unitfile = 'project folder'
        os.chdir(mpathcrst)
    except ImportError:
        from oncepy.unitc import *
        cfg.unitfile = 'built-in'
os.chdir(mpathcrst)


class CalcRST(object):
    """Accepts a model dictionary and writes an rst file"""

    def __init__(self, odict):
        """initialize files

    **Args**
        odict (dict)
        mpath (str)
        mfile (str)

        """
        # execution log
        self.ew = ccheck.ModCheck()

        self.mpath = cfg.mpath
        self.mfile = cfg.mfile
        #print('mfile', self.mfile)
        self.rfilename = self.mfile.replace('.txt', '.rst')
        self.rpath = os.path.join(self.mpath, self.rfilename)
        #print('rpath', self.rpath)
        self.rf1 = ''

        self.prfilename = ''
        self.previous = ''
        self.xtraline = False

        self.widthp = 70   # line width for terms
        #self.widthc = 90

        # get list of equation symbols
        self.odict = odict
        self.symb = self.odict.keys()
        self.symblist = []
        self.fignum = 0


    def gen_rst(self):
        """ write rst file """

        self.rf1 = codecs.open(self.rpath, 'w', encoding='utf8')
        #print(' ' + time.strftime("%c"), file=self.rf1)

        termbegin = 1
        mtagx = ''
        for _i in self.odict:
            #print(_i, self.odict[_i])
            mtag = self.odict[_i][0]
            # avoid extra lines in term lists
            if mtagx == '[t]':
                if mtag == '[t]':
                    termbegin = 0
            if mtagx == '[t]':
                if mtag != '[t]':
                    termbegin = 1
                    print('  ', file=self.rf1)
            mtagx = mtag

            if mtag ==   '[r]':
                self._rst_read(self.odict[_i])
                self.xtraline = False
            elif mtag == '[d]':
                if self.odict[_i][2].strip() == 'f':
                    self._rst_figure(self.odict[_i])
                    self.xtraline = False
                else:
                    self._rst_disk(self.odict[_i])
                    self.xtraline = False
            elif mtag == '[o]':
                self._rst_olic(self.odict[_i])
                self.xtraline = False
            elif mtag == '[t]':
                self._rst_term(self.odict[_i], termbegin)
                self.xtraline = False
            elif mtag == '[c]':
                self._rst_check(self.odict[_i])
                self.xtraline = True
            elif mtag == '[a]':
                self._rst_array(self.odict[_i])
                self.xtraline = True
            elif mtag == '[f]':
                self._rst_func(self.odict[_i])
                self.xtraline = False
            elif mtag == '[e]':
                self._rst_eq(_i, self.odict[_i])
                self.xtraline = False
            elif mtag == '[s]':
                self._rst_sect(self.odict[_i])
                self.xtraline = False
            elif mtag == '[x]':
                self._rst_txt(self.odict[_i])
                self.xtraline = True
            # [r] is a virtual tag
            elif mtag == '[r]':
                self._rst_read(self.odict[_i])
                self.xtraline = False
            elif mtag == '[~]' and self.xtraline is False:
                self.xtraline = True
            elif mtag == '[~]' and self.xtraline is True:
                self._rst_blnk()
            else:
                continue

        # add calc license
        for _i in self.odict:
            if _i == '_pd':
                self._rst_blnk()
                lic_txt = """
___________________________________________________________________________

This calc (the calc) is generated from a generic on-c-e model template.
The calc is distributed under the CCO 1.0 Public Domain Dedication
(see http://creativecommons.org/publicdomain/zero/1.0/ ). The calc is not a
structural design calculation and the template must be
modified by the user prior to use. The calc user assumes sole and complete
responsibility for all existing inputs and results.
"""

                self._rst_txt([' ', lic_txt])

        # print end of calc
        self._rst_blnk()
        self._rst_txt([' ','\n**[end of calc]**'])

        # close rst file
        self.rf1.close()
        #for i in self.odict: print(i, self.odict[i])

    def _rst_figure(self, dval):
        """print figure

        Dictionary Value:
        equation:[[d], file path, options, var1, var2, var3]

        Args: str
            dval[0] - operation
            dval[1] - data file
            dval[2] - option -> 'f'
            dval[3] - caption
            dval[4] - percent width
            dval[5] - 'double' -> side by side figures
        """
        fpath = dval[1].strip()
        fp = os.path.join(self.mpath, fpath)
        option = dval[2].strip()
        param1 = dval[3].strip()
        param2 = dval[4].strip()
        param3 = dval[5].strip()

        if option == 'f':
            print(' ', file=self.rf1)
            print('.. figure:: ' + fp, file=self.rf1)
            print('   :width: ' + param2 + ' %', file=self.rf1)
            print('   :align: center', file=self.rf1)
            print('   ', file=self.rf1)
            print('   ' + param1, file=self.rf1)
            print(' ', file=self.rf1)

    def _rst_read(self, dval):
        """read csv data file

        Args: strng
            dval[0] - operation
            dval[1] - data file
            dval[2] - option
            dval[3] - var
            dval[4] - sep
            dval[5] - skip line
            dval[6] - model file
        """
        secthead =  str(dval[3]) + " | read data " + dval[6]

        print("aa-bb " + "**" + secthead + "**", file=self.rf1)
        print('  ', file=self.rf1)

        # set skip lines
        skip1 = dval[5]
        if skip1 == '':
            skip1 = int(0)
        else:
            skip1 = int(skip1)

        fpath = dval[1].strip()
        # set separator
        sep1 = dval[4]
        if sep1 == '*':
            var4 = genfromtxt(fpath, delimiter=' ',
                              skip_header=skip1)
        elif sep1 == ',' or sep1 == '':
            var4 = genfromtxt(fpath, delimiter=',',
                              skip_header=skip1)
        else:
            var4 = genfromtxt(fpath, delimiter=str(sep1),
                              skip_header=skip1)
        #print('var4', var4[:2])

        cmdstr1 = str(dval[3].strip())
        cmdstr2 = cmdstr1 + '=' + str(list(var4))
        self.odict[cmdstr1] = ['[rd]', cmdstr2]
        #print(self.odict[cmdstr1])

        # print data selection
        print('  ', file=self.rf1)
        print("file: " + dval[1].strip(), file=self.rf1)
        print('  ', file=self.rf1)
        print(str(var4[:4]) + ' ... ' + str(var4[-4:]),
              file=self.rf1)
        print('  ', file=self.rf1)


        # draw line
        print(".. raw:: latex", file=self.rf1)
        print('  ', file=self.rf1)
        print('   \\hrulefill', file=self.rf1)
        print('  ', file=self.rf1)
        print(".. raw:: latex", file=self.rf1)
        print('  ', file=self.rf1)
        print('   \\vspace{2mm}', file=self.rf1)
        print('  ', file=self.rf1)

        #print('mdict', self.mdict[str(var1)])

    def _rst_disk(self, dval):
        """print and execute disk operations

        Dictionary Value:
        equation:[[d], file path, parameter, var1, var2, var3]

        options:
        s: run a python script
        """
        _prt_log = self.ew.ewrite2

        fpath = dval[1].strip()
        fp = os.path.abspath(fpath)
        option = dval[2].strip()
        var1 = dval[3].strip()
        var2 = dval[4].strip()
        var3 = dval[5]  # variable with edit lines

        # additional disk operation output for PDF calcs
        if option == 's':
            # execute script in model namespace
            f1 = open(fp, 'r')
            fr = f1.read()
            f1.close()
            exec(fr, globals())
            link1 = "< execute python script: " + str(fp) + " >"
            _prt_log(link1)
            _prt_log("file: " + fpath + " compiled")

        elif option == 'e':
            editlist = []
            for item in var3:
                editlist.append(item)

            strend = "edit file " + dval[6].strip()
            print("aa-bb " + "**" + strend + "**",
                  file=self.rf1)
            print(" ", file=self.rf1)

            # edit line table
            print('  ', file=self.rf1)
            print('::', file=self.rf1)
            print('  ', file=self.rf1)
            print("  file: " + dval[1].strip(), file=self.rf1)
            title1 = '  [line #]'.center(8) + \
                     '[replacement line]'.rjust(25)
            print(title1, file=self.rf1)
            for _i in editlist[:-1]:
                _j = _i.split('|')
                print(('     ' + _j[0].strip()).ljust(10)
                              + (_j[1].strip()), file=self.rf1)
            print(' ', file=self.rf1)

            # draw horizontal line
            print(".. raw:: latex", file=self.rf1)
            print('  ', file=self.rf1)
            print('   \\vspace{4mm}', file=self.rf1)
            print('  ', file=self.rf1)
            print(".. raw:: latex", file=self.rf1)
            print('  ', file=self.rf1)
            print('   \\hrulefill', file=self.rf1)
            print('  ', file=self.rf1)
            print(".. raw:: latex", file=self.rf1)
            print('  ', file=self.rf1)
            print('   \\vspace{2mm}', file=self.rf1)
            print('  ', file=self.rf1)


    def _rst_olic(self, dval):
        """print symbolic representation

        Dictionary:
        symbolic:[[l], expr]

        """
        dval = dval[1].replace('=', '<=')
        exp2 = dval.split('\n')
        exp3 = ' '.join([ix.strip() for ix in exp2])
        symp1 = sympify(exp3)

        for _j in symp1.atoms():
            varsym(str(_j))

        symeq = eval(dval)
        # symbolic repr
        print('  ', file=self.rf1)
        print('.. math:: ', file=self.rf1)
        print('  ', file=self.rf1)
        print('  ' + latex(symeq, mul_symbol="dot"), file=self.rf1)
        print('  ', file=self.rf1)
        print('|', file=self.rf1)
        print('  ', file=self.rf1)

    def _rst_term(self, dval, termbegin):
        """print terms

        terms: [[t], statement, expr, ref ]

        """
        ptype = type(eval(dval[2]))
        val1 = eval(dval[2].strip())
        var1 = dval[1].split('=')[0].strip()
        if ptype == ndarray:
            tmp1 = str(val1)
            if '[[' in tmp1:
                tmp2 = tmp1.replace(' [', '.  [')
                tmp1 = tmp2.replace('[[', '. [[')
            else:
                tmp1 = tmp1.replace('[', '. [')
            print('  ', file=self.rf1)
            print('::', file=self.rf1)
            print('  ', file=self.rf1)
            print('. ' + var1 + ' = ', file=self.rf1)
            print(tmp1, file=self.rf1)
            print('  ', file=self.rf1)
            print(".. raw:: latex", file=self.rf1)
            print('  ', file=self.rf1)
            print('   \\vspace{1mm}', file=self.rf1)
            print('  ', file=self.rf1)
            return
        elif ptype == list or ptype == tuple:
            tmp1 = str(val1)
            if ']]' in tmp1:
                tmp1 = tmp1.replace(']]', ']]\n')
            else:
                tmp1 = tmp1.replace(']', ']\n')
            print('\n' + var1 + ' = ', file=self.rf1)
            print(tmp1, file=self.rf1)
            return
        state = var1 + ' = ' + str(val1)
        shift = int(self.widthp / 2.5)
        ref = dval[3].strip().ljust(shift)
        termpdf = " "*4 + ref + ' | ' + state
        if termbegin:
            #print('termbegin')
            print('  ', file=self.rf1)
            print('::', file=self.rf1)
            print('  ', file=self.rf1)
        print(termpdf, file=self.rf1)

    def _rst_check(self, dval):
        """print check

        Dictionary:
        check:  [[c], check expr, op, limit, ref, dec, ok]

        """

        try:
            exec("set_printoptions(precision=" + dval[5].strip() + ")")
            exec("Unum.VALUE_FORMAT = '%." + dval[5].strip() + "f'")
        except:
            set_printoptions(precision=3)
            Unum.VALUE_FORMAT = "%.3f"

        # convert variables to symbols
        for _j in self.symb:
            if _j[0] != '_':
                varsym(_j)

        # symbolic form
        symeq1 = eval(dval[1].strip() + dval[2].strip() +
                      dval[3].strip())
        #pprint(symeq1)
        # evaluate variables
        for _k in self.odict:
            if _k[0] != '_':
                #print(self.odict[_k][1].strip())
                exec(self.odict[_k][1].strip())

        # substitute values
        try:
            nounits1 = eval(dval[1].strip()).asNumber()
        except:
                nounits1 = eval(dval[1].strip())
        try:
            nounits2 = eval(dval[3].strip()).asNumber()
        except:
                nounits2 = eval(dval[3].strip())

        result = eval(str(nounits1) + dval[2].strip() + str(nounits2))
        resultform = '{:.' + dval[5].strip()+'f}'
        result1 = resultform.format(float(str(nounits1)))
        result2 = resultform.format(float(str(nounits2)))
        subbed = result1 + ' ' + dval[2].strip() + ' ' + result2

        if result:
            comment = ' - ' + dval[6].strip()
        else:
            comment = ' *** not ' + dval[6].strip() + ' ***'
        out2p = subbed + '  ' + comment

        # section header
        secthead = dval[4].strip()
        # equation label
        print("aa-bb " + "**" + secthead + "**", file=self.rf1)
        print('  ', file=self.rf1)

        # symbolic repr
        print('  ', file=self.rf1)
        print('.. math:: ', file=self.rf1)
        print('  ', file=self.rf1)
        print('  ' + latex(symeq1, mul_symbol="dot"), file=self.rf1)
        print('  ', file=self.rf1)
        print('|', file=self.rf1)
        print('  ', file=self.rf1)

        # substituted values in equation
        # list of symbols
        symat = symeq1.atoms(Symbol)

        # convert to latex form
        latexrep = latex(symeq1, mul_symbol="dot")
        #print('latex', latexrep)

        switch1 = []
        # rewrite equation with braces
        for _n in symat:
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
            symeq1 = symeq1.subs(_n, symbols(newlatex1))
            switch1.append([str(_n), newlatex1])
        # list of new symbols

        # substitute values
        for _n in switch1:
            expr1 = eval((self.odict[_n[0]][1]).split("=")[1])
            if type(expr1) == float:
                form = '{:.' + dval[5].strip() +'f}'
                symvar1 = '{' + form.format(expr1) + '}'
            else:
                symvar1 = '{' + str(expr1) + '}'
            latexrep = latexrep.replace(_n[1], symvar1)
            latexrep = latexrep.replace("\{", "{")


        # add substituted equation to rst file
        print('  ', file=self.rf1)
        print('.. math:: ', file=self.rf1)
        print('  ', file=self.rf1)
        print('  ' + latexrep, file=self.rf1)
        print('  ', file=self.rf1)
        print('|', file=self.rf1)
        print('  ', file=self.rf1)

        # result
        print(' ', file=self.rf1)
        print('.. math:: ', file=self.rf1)
        print('  ', file=self.rf1)
        print("  \\boldsymbol{" + latex(out2p,
                mode='plain') + "}", file=self.rf1)
        print('  ', file=self.rf1)

        # draw line
        print(".. raw:: latex", file=self.rf1)
        print('  ', file=self.rf1)
        print('   \\hrulefill', file=self.rf1)
        print('  ', file=self.rf1)
        print(".. raw:: latex", file=self.rf1)
        print('  ', file=self.rf1)
        print('   \\vspace{2mm}', file=self.rf1)
        print('  ', file=self.rf1)

    def _rst_array(self, dval):
        """
        print tag [a] - an ascii table from statements or variable

        arrays:   [[a], statement, expr, range1, range2,
        ref, decimals, unit1, unit2, model]

        """
        try:
            eformat, rformat = dval[4].split(',')
            exec("set_printoptions(precision=" + eformat + ")")
            exec("Unum.VALUE_FORMAT = '%." + eformat + "f'")
        except:
            eformat = '3'
            rformat = '3'
            set_printoptions(precision=3)
            Unum.VALUE_FORMAT = "%.3f"

        # table heading
        varx = dval[2].strip()
        tright = dval[5].strip().split(' ')
        eqnum = tright[-1].strip()
        tleft = ' '.join(tright[:-1]).strip()
        tablehdr = tleft + ' ' + eqnum

        print("aa-bb " + "**" + tablehdr + "**",
              file=self.rf1)

        print(' ', file=self.rf1)
        print('**range variables:** ', file=self.rf1)
        print(' ', file=self.rf1)
        print(pretty(dval[3].strip()), file=self.rf1)
        print(' ', file=self.rf1)
        print(pretty(dval[4].strip()), file=self.rf1)

        vect = dval[1:]
        # print symbolic form
        # convert variables to symbols except for arrays
        try:
            for _j in self.symb:
                if str(_j)[0] != '_':
                    varsym(str(_j))

            #convert array variable
            var1 = vect[2].split('=')[0].strip()
            varsym(str(var1))

            try:
                var2 = vect[3].split('=')[0].strip()
                varsym(str(var2))
            except:
                pass

            symeq = eval(vect[1].strip())
            out1 = symeq

            etype = vect[0].split('=')[1]
            if etype.strip()[:1] == '[':
                out1 = str(vect[0].split('=')[1])

            print(' ', file=self.rf1)
            print('**equation:** ', file=self.rf1)
            print(' ', file=self.rf1)
            # symbolic repr
            print('  ', file=self.rf1)
            print('.. math:: ', file=self.rf1)
            print('  ', file=self.rf1)
            print('  ' + latex(symeq, mul_symbol="dot"), file=self.rf1)
            print('  ', file=self.rf1)
            print('|', file=self.rf1)
            print('  ', file=self.rf1)
        except:
            pass

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

        # single row vector - 1D table
        if len(str(vect[3])) == 0 and len(str(vect[0])) != 0:
            # process range variable 1 and heading
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
                elist2 = []
                alist1 = eval(equa1.split('=')[1])
                for _v in alist1:
                        try:
                            elist2.append(list(_v))
                        except:
                            elist2.append(_v)
            else:
                try:
                    elist2 = elist1.tolist()
                except:
                    elist2 = elist1

            elist2 = [elist2]
            # create table
            # onceutf modified
            ptable = tabulate.tabulate(elist2, rlist, 'rst',
                                floatfmt="."+dval[6].strip()+"f")

            print(ptable, file=self.rf1)
            print('  ', file=self.rf1)
            #print(ptable)

        # 2D table
        if len(str(vect[3])) != 0 and len(str(vect[0])) != 0:
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
                alist = []
                alist1 = eval(equa1.split('=')[1])
                #print('alist1', alist1)
                for _v in alist1:
                    for _x in _v:
                        #print('_x', _x)
                        alist.append(list(_x))
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

            #print('alist', alist)
            for _n, _p in enumerate(alist):
                _p.insert(0, clist[_n])

            # create table
            flt1 = "." + eformat.strip() + "f"
            #print(alist)
            ptable = tabulate.tabulate(alist, rlist, 'rst',
                                       floatfmt=flt1)
            print(ptable, file=self.rf1)

            print('  ', file=self.rf1)

    def _rst_func(self, dval):
        """print function

        Dictionary:

        Arguments:
        ip: a model line or block

        Dictionary Value:
        function:[[f], function name, ref, model number

        """
        # print reference line
        funcname = dval[1].split('(')[0]
        funchd = funcname.strip() + ' | function ' + dval[4].strip()
        # insert pattern for later modification of tex file
        print("aa-bb " + "**" + funchd + "**", file=self.rf1)
        print(' ', file=self.rf1)

        # convert symbols to numbers - retain units
        for k1 in self.odict:
            if k1[0] != '_':
                try:
                    exec(self.odict[k1][1].strip())
                except:
                    pass
            if k1[0:2] == '_a':
                #print('ek1-2', k1)
                try:
                    exec(self.odict[k1][3].strip())
                    exec(self.odict[k1][4].strip())
                    exec(self.odict[k1][1].strip())
                except:
                    pass

        # evaluate function
        print(" ", file=self.rf1)
        print('function description: ' + dval[3].strip(), file=self.rf1)
        print(" ", file=self.rf1)
        print('function call: ' + dval[1].strip(), file=self.rf1)
        funcname = dval[1].split('(')[0]
        docs1 = eval(funcname + '.__doc__')
        print('  ', file=self.rf1)
        print('**function doc string:**', file=self.rf1)
        print('  ', file=self.rf1)
        print('::', file=self.rf1)
        print('  ', file=self.rf1)
        print('  ' + docs1, file=self.rf1)
        print('  ', file=self.rf1)

        return1 = eval(dval[1].strip())
        if return1 is None:
            print('function evaluates to None', file=self.rf1)
            print('  ', file=self.rf1)
        else:
            print('**function returned:** ', file=self.rf1)
            tmp1 = str(return1)
            if '[[' in tmp1:
                tmp2 = tmp1.replace(' [', '.  [')
                tmp1 = tmp2.replace('[[', '. [[')
            elif '[' in tmp1:
                tmp1 = tmp1.replace('[', '. [')
            else:
                if tmp1[0:2] != '  ':
                    tmp1 = '  ' + tmp1
            print('  ', file=self.rf1)
            print('::', file=self.rf1)
            print('  ', file=self.rf1)
            print(tmp1, file=self.rf1)
            print('  ', file=self.rf1)
            print(".. raw:: latex", file=self.rf1)
            print('  ', file=self.rf1)
            print('   \\vspace{2mm}', file=self.rf1)
            print('  ', file=self.rf1)

        # draw line
        print(".. raw:: latex", file=self.rf1)
        print('  ', file=self.rf1)
        print('   \\hrulefill', file=self.rf1)
        print('  ', file=self.rf1)
        print(".. raw:: latex", file=self.rf1)
        print('  ', file=self.rf1)
        print('   \\vspace{2mm}', file=self.rf1)
        print('  ', file=self.rf1)

    def _rst_eq(self, var3, dval):
        """print equation

        equations dict:
        [[e], statement, expr, ref, decimals, units, prnt opt]
        key = var3

        """
        try:
            eformat, rformat = dval[4].split(',')
            exec("set_printoptions(precision=" + eformat + ")")
            exec("Unum.VALUE_FORMAT = '%." + eformat + "f'")
        except:
            eformat = '3'
            rformat = '3'
            set_printoptions(precision=3)
            Unum.VALUE_FORMAT = "%.3f"

        cunit = dval[5].strip()
        #var3 = dval[1].split("=")[0].strip()
        #val3 = eval(dval[2])

        # evaluate variables
        for k1 in self.odict:
            #print('k1', k1)
            if k1[0] != '_':
                    try:
                        exec(self.odict[k1][1].strip())
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

        exec(dval[1])
        # evaluate only
        if dval[6].strip() == '0':
            print('  ', file=self.rf1)
            return

        # equation reference line
        print('  ', file=self.rf1)
        print(".. raw:: latex", file=self.rf1)
        print('  ', file=self.rf1)
        print('   \\vspace{1mm}', file=self.rf1)
        print('  ', file=self.rf1)
        strend = dval[3].strip()
        print('  ', file=self.rf1)
        print("aa-bb " + "**" + var3 + " | " + strend + "**",
              file=self.rf1)
        print('  ', file=self.rf1)

        # result only
        if dval[6].strip() == '1':
            #convert result variable to greek
            var3s = var3.split('_')
            if var3s[0] in greeks:
                var3g = "\\" + var3
            else:
                var3g = var3
            # print result
            typev = type(eval(var3))
            if typev == ndarray:
                tmp1 = str(eval(var3))
                if '[[' in tmp1:
                    tmp2 = tmp1.replace(' [', '.  [')
                    tmp1 = tmp2.replace('[[', '. [[')
                else:
                    tmp1 = tmp1.replace('[', '. [')
                print('  ', file=self.rf1)
                print('::', file=self.rf1)
                print('  ', file=self.rf1)
                print('. ' + var3 + ' = ', file=self.rf1)
                print(tmp1, file=self.rf1)
                print('  ', file=self.rf1)
                print(".. raw:: latex", file=self.rf1)
                print('  ', file=self.rf1)
                print('   \\vspace{4mm}', file=self.rf1)
                print('  ', file=self.rf1)
            elif typev == list or typev == tuple:
                tmp1 = str(eval(var3))
                if '[[' in tmp1:
                    tmp2 = tmp1.replace(' [', '.  [')
                    tmp1 = tmp2.replace('[[', '. [[')
                else:
                    tmp1 = tmp1.replace('[', '. [')
                tmp1 = tmp1.replace('],', '],\n')
                print('  ', file=self.rf1)
                print('::', file=self.rf1)
                print('  ', file=self.rf1)
                print('. ' + var3 + ' = ', file=self.rf1)
                print(tmp1, file=self.rf1)
                print('  ', file=self.rf1)
                print(".. raw:: latex", file=self.rf1)
                print('  ', file=self.rf1)
                print('   \\vspace{4mm}', file=self.rf1)
                print('  ', file=self.rf1)
            elif type(eval(var3)) != Unum:
                if type(eval(var3)) == float \
                    or type(eval(var3)) == float64:
                    resultform = '{:.' + eformat.strip() + 'f}'
                    tmp1 = resultform.format(float(eval(var3)))
                    result2 = var3g + " = " + str(tmp1)
                    print(' ', file=self.rf1)
                    print('.. math:: ', file=self.rf1)
                    print('  ', file=self.rf1)
                    print("  \\boldsymbol{" + latex(result2,
                            mode='plain') + "}", file=self.rf1)
                    print('  ', file=self.rf1)
                else:
                    result2 = var3 + " = " + str(eval(var3))
                    print(' ', file=self.rf1)
                    print('.. math:: ', file=self.rf1)
                    print('  ', file=self.rf1)
                    print("  \\boldsymbol{" + latex(result2,
                            mode='plain') + "}", file=self.rf1)
                    print('  ', file=self.rf1)
            else:
                if len(cunit) > 0:
                    tmp2 = str(eval(var3).asUnit(eval(cunit)))
                else:
                    tmp2 = str(eval(var3))
                result3 = var3g + " = " + str(tmp2)
                print(' ', file=self.rf1)
                print('.. math:: ', file=self.rf1)
                print('  ', file=self.rf1)
                print("  \\boldsymbol{" + latex(result3,
                        mode='plain') + "}", file=self.rf1)
                print('  ', file=self.rf1)
            return

        # symbolic and substituted forms
        else:
            # print symbolic form
            for _j in self.symb:
                if str(_j)[0] != '_':
                    varsym(str(_j))
            #print('dval2', dval[2])
            try:
                symeq = sympify(dval[2].strip())
                print('  ', file=self.rf1)
                print('.. math:: ', file=self.rf1)
                print('  ', file=self.rf1)
                print('  ' + latex(symeq, mul_symbol="dot"), file=self.rf1)
                print('  ', file=self.rf1)
                print(".. raw:: latex", file=self.rf1)
                print('  ', file=self.rf1)
                print('   \\vspace{1mm}', file=self.rf1)
                print('  ', file=self.rf1)
            except:
                symeq = dval[2].strip()
                print('  ', file=self.rf1)
                print('::', file=self.rf1)
                print('  ', file=self.rf1)
                print('  ' + symeq, file=self.rf1)
            # substitute values for variables
            if dval[6].strip() == '3':
                # list of symbols
                symat = symeq.atoms(Symbol)
                # copy of equation
                #symeq1 = sympify(dval[2].strip())
                # convert to latex form
                latexrep = latex(symeq, mul_symbol="dot")
                #print('latex', latexrep)
                switch1 = []
                # rewrite latex equation withbraces
                for _n in symat:
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
                    #symeq1 = symeq1.subs(_n, symbols(newlatex1))
                    switch1.append([str(_n), newlatex1])
                # substitute values
                for _n in switch1:
                    #print('swi', (self.odict[_n[0]][1]).split("=")[1])
                    expr1 = eval((self.odict[_n[0]][1]).split("=")[1])
                    if type(expr1) == float:
                        form = '{:.' + eformat.strip() +'f}'
                        symvar1 = '{' + form.format(expr1) + '}'
                    else:
                        symvar1 = '{' + str(expr1) + '}'
                    #print('replace',_n[1], symvar1)
                    latexrep = latexrep.replace(_n[1], symvar1)
                    latexrep = latexrep.replace("\{", "{")
                    #print(latexrep)
                # add substituted equation to rst file
                print('  ', file=self.rf1)
                print('.. math:: ', file=self.rf1)
                print('  ', file=self.rf1)
                print('  ' + latexrep, file=self.rf1)
                print('  ', file=self.rf1)
                print(".. raw:: latex", file=self.rf1)
                print('  ', file=self.rf1)
                print('   \\vspace{1mm}', file=self.rf1)
                print('  ', file=self.rf1)
                print('  ', file=self.rf1)
            # restore units
            for j2 in self.odict:
                try:
                    state = self.odict[j2][1].strip()
                    exec(state)
                except:
                    pass
            #convert result variable to greek
            var3s = var3.split('_')
            if var3s[0] in greeks:
                var3g = "\\" + var3
            else:
                var3g = var3
            # print result
            typev = type(eval(var3))
            if typev == ndarray:
                tmp1 = str(eval(var3))
                if '[[' in tmp1:
                    tmp2 = tmp1.replace(' [', '.  [')
                    tmp1 = tmp2.replace('[[', '. [[')
                else:
                    tmp1 = tmp1.replace('[', '. [')
                print('  ', file=self.rf1)
                print('::', file=self.rf1)
                print('  ', file=self.rf1)
                print('. ' + var3 + ' = ', file=self.rf1)
                print(tmp1, file=self.rf1)
                print('  ', file=self.rf1)
                print(".. raw:: latex", file=self.rf1)
                print('  ', file=self.rf1)
                print('   \\vspace{4mm}', file=self.rf1)
                print('  ', file=self.rf1)
            elif typev == list or typev == tuple:
                tmp1 = str(eval(var3))
                if '[[' in tmp1:
                    tmp2 = tmp1.replace(' [', '.  [')
                    tmp1 = tmp2.replace('[[', '. [[')
                else:
                    tmp1 = tmp1.replace('[', '. [')
                tmp1 = tmp1.replace('],', '],\n')
                print('  ', file=self.rf1)
                print('::', file=self.rf1)
                print('  ', file=self.rf1)
                print('. ' + var3 + ' = ', file=self.rf1)
                print(tmp1, file=self.rf1)
                print('  ', file=self.rf1)
                print(".. raw:: latex", file=self.rf1)
                print('  ', file=self.rf1)
                print('   \\vspace{4mm}', file=self.rf1)
                print('  ', file=self.rf1)
            elif type(eval(var3)) != Unum:
                if type(eval(var3)) == float \
                    or type(eval(var3)) == float64:
                    resultform = '{:.' + dval[4].strip()+'f}'
                    tmp1 = resultform.format(float(eval(var3)))
                    result2 = var3g + " = " + str(tmp1)
                    print(' ', file=self.rf1)
                    print('.. math:: ', file=self.rf1)
                    print('  ', file=self.rf1)
                    print("  \\boldsymbol{" + latex(result2,
                            mode='plain') + "}", file=self.rf1)
                    print('  ', file=self.rf1)
                else:
                    result2 = var3 + " = " + str(eval(var3))
                    print(' ', file=self.rf1)
                    print('.. math:: ', file=self.rf1)
                    print('  ', file=self.rf1)
                    print("  \\boldsymbol{" + latex(result2,
                            mode='plain') + "}", file=self.rf1)
                    print('  ', file=self.rf1)
            else:
                if len(cunit) > 0:
                    exec("Unum.VALUE_FORMAT = '%." + rformat.strip()
                         + "f'")
                    tmp2 = str(eval(var3).asUnit(eval(cunit)))
                else:
                    tmp2 = str(eval(var3))
                result3 = var3g + " = " + str(tmp2)
                print(' ', file=self.rf1)
                print('.. math:: ', file=self.rf1)
                print('  ', file=self.rf1)
                print("  \\boldsymbol{" + latex(result3,
                        mode='plain') + "}", file=self.rf1)
                print('  ', file=self.rf1)

            # draw horizontal line
            print(".. raw:: latex", file=self.rf1)
            print('  ', file=self.rf1)
            print('   \\vspace{-9mm}', file=self.rf1)
            print('  ', file=self.rf1)
            print(".. raw:: latex", file=self.rf1)
            print('  ', file=self.rf1)
            print('   \\hrulefill', file=self.rf1)
            print('  ', file=self.rf1)
            print(".. raw:: latex", file=self.rf1)
            print('  ', file=self.rf1)
            print('   \\vspace{2mm}', file=self.rf1)
            print('  ', file=self.rf1)

    def _rst_sect(self, dval):
        """print section

        Dictionary:
        section: ['[s]', sleft, state, file]

        """
        tleft = dval[1].strip()
        tright = dval[3].strip()
        print('  ', file=self.rf1)
        print(tleft.strip() + "aa-bb " + tright.strip(),
              file=self.rf1)
        print("-"*self.widthp, file=self.rf1)
        notes = '\n'.join([i.strip() for i in dval[2]])
        if len(notes.strip()) > 0:
            print(notes + '\n', file=self.rf1)
        print(' ', file=self.rf1)
        print(".. raw:: latex", file=self.rf1)
        print(' ', file=self.rf1)
        print('   \\vspace{1mm}', file=self.rf1)
        print(' ', file=self.rf1)

    def _rst_txt(self, txt):
        """output pass-through text"""
        print(txt[1].strip(), file=self.rf1)

    def _rst_blnk(self):
        """print blank line"""
        print('  ', file=self.rf1)
        print(".. raw:: latex", file=self.rf1)
        print('  ', file=self.rf1)
        print('   \\vspace{4mm}', file=self.rf1)
        print('  ', file=self.rf1)