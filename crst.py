from __future__ import division
from __future__ import print_function
import os
import sys
import time
import tabulate
import codecs
import oncepy.oconfig as cfg
from oncepy import ccheck
from oncepy import oconfig as cfg
from unum import Unum
from numpy import *
from sympy import *
from sympy import var as varsym
from sympy.core.alphabets import greeks
#from sympy.printing.latex import tex_greek_dictionary as texdict


class CalcRST(object):
    """Accepts a model dictionary and writes an rst file"""

    def __init__(self, odict, mpath, mfile):
        """initialize files

    **Args**
        odict (dict)
        mpath (str)
        mfile (str)

        """
        # execution log
        self.ew = ccheck.ModCheck()

        self.mpath = mpath
        self.rfilename = mfile.replace('.txt', '.rst')
        self.rpath = os.path.join(mpath, self.rfilename)
        print(self.rpath)
        self.rfile = ''

        self.cfolder = mpath
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

    def prt_rst(self):
        """ write rst file """

        self.rfile = codecs.open(self.rpath, 'w', encoding='utf8')
        print(time.strftime("%c"), file=self.rfile)

        for _i in self.odict:
            #print(_i, self.odict[_i])
            mtag = self.odict[_i][0]
            #print(mtag)
            if mtag ==   '[d]':
                if self.odict[_i].split('|')[3].strip() == 'f':
                    self._pdf_figure(self.odict[_i])
                    self.xtraline = False
            elif mtag == '[r]':
                self._pdf_read(self.odict[_i])
                self.xtraline = False
            elif mtag == '[o]':
                self._pdf_olic(self.odict[_i])
                self.xtraline = False
            elif mtag == '[t]':
                self._pdf_term(self.odict[_i])
                self.xtraline = True
            elif mtag == '[c]':
                self._pdf_check(self.odict[_i])
                self.xtraline = True
            elif mtag == '[a]':
                self._pdf_array(self.odict[_i])
                self.xtraline = True
            elif mtag == '[f]':
                self._pdf_func(self.odict[_i])
                self.xtraline = True
            elif mtag == '[e]':
                self._pdf_eq(_i, self.odict[_i])
                self.xtraline = False
            elif mtag == '[s]':
                self._pdf_sect(self.odict[_i])
                self.xtraline = False
            elif mtag == '[x]':
                self._pdf_txt(self.odict[_i])
                self.xtraline = True
            elif mtag == '[~]' and self.xtraline is False:
                self.xtraline = True
            elif mtag == '[~]' and self.xtraline is True:
                self._pdf_blnk()
            else:
                continue

        # close rst file
        self.rfile.close()
        #for i in self.odict: print(i, self.odict[i])

    def _pdf_figure(self, dval):

        """print tag [d]

        Dictionary Value:
        equation:[[d], file path, options, var1, var2, var3]

        Args: strng
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
            print(' ', file=self.rfile)
            print('.. figure:: ' + fp, file=self.rfile)
            print('   :width: ' + param2 + ' %', file=self.rfile)
            print('   :align: centered', file=self.rfile)
            print('   ', file=self.rfile)
            print('   ' + param1, file=self.rfile)
            print(' ', file=self.rfile)

    def _pdf_read(self, dval):
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

        var1 = dval[3].strip()

        sep1 = dval[4].strip()
        if sep1 == '':
            sep1 = ','
        elif sep1 == '*':
            sep1 = " "

        skip = dval[5].strip()
        if skip == '':
            skip = 0
        else:
            skip = int(skip)

        fpath = dval[1].strip()
        file1 = open(fpath, 'r')
        var2 = genfromtxt(file1, delimiter=sep1, skip_header=skip)
        file1.close()

        exec(var1 + '= var2')
        eval(var1)

        # print reference line
        tmp = int(self.widthclc-1) * '-'
        print((tmp + u'\u2510').rjust(self.widthclc), 0)

        strend = "data file: " + dval[1].strip()
        print(strend.rjust(self.widthclc), 0)
        print(" ", 1)

        # evaluate data
        print(dval[1].strip(), 0)
        strng_return = eval(dval[1].strip())
        print(' ', 0)
        print(strng_return, 0)
        print(' ', 0)

        tmp = int(self.widthclc-1) * '-'
        print((tmp + u'\u2518').rjust(self.widthclc), 0)
        print(" ", 0)

    def _pdf_olic(self, dval):
        """print tag [l]

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
        symeq2 = pretty(symeq, wrap_line=False)
        out3 = symeq2.replace('*', u'\u22C5')
        cnt = 0
        for _m in out3:
            if _m == '-':
                cnt += 1
                continue
            else:
                if cnt > 1:
                    out3 = out3.replace('-'*cnt, u'\u2014'*cnt)
                cnt = 0
        print(out3.replace('<=', '='), 1)
        print(" ", 0)

    def _pdf_term(self, dval):
        """
        output terms
        terms: [[t], statement, expr, ref ]

        """
        shift = int(self.widthp / 2.8)
        ref = dval[3].strip().ljust(shift)
        param = dval[1].strip()
        ptype = type(eval(dval[2]))
        if ptype == list or ptype == ndarray or ptype == tuple:
            param = param.split('=')[0].strip()
        termpdf = " "*4 + ref + param

        strend = dval[3].strip()
        param = '  ' + dval[1].strip()
        print(' ', file=self.rfile)
        print('::', file=self.rfile)
        print(' ', file=self.rfile)
        print(termpdf, file=self.rfile)

    def _pdf_check(self, dval):
        """print [c]

        Dictionary:
        check:  [[c], check expr, op, limit, ref, dec, ok]

        """
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
            comment = ' ' + dval[6].strip()
        else:
            comment = ' *** not ' + dval[6].strip() + ' ***'

        out2p = subbed + '  ' + comment
        strend = dval[4].strip()

        # clean output
        #out2p = pretty((symeq1, '  ', out2, '=', out3, comment))
        #repc = [(',', ' '), ('(', ' '), (')', ' ')]
        #out2a = out2p
        #for _k in repc:
        #    out2a = out2a.replace(_k[0], _k[1])
        #strend = ratio[3].strip()

        print('  ', file=self.rfile)
        print("**yxxhfillxxx " + strend + "**", file=self.rfile)
        print('  ', file=self.rfile)

        print('::', file=self.rfile)
        print(' ', file=self.rfile)
        print(pretty(symeq1), file=self.rfile)
        print(' ', file=self.rfile)
        print(pretty(out2p), file=self.rfile)
        print(' ', file=self.rfile)

        print(".. raw:: latex", file=self.rfile)
        print('  ', file=self.rfile)
        print('   \\hrulefill', file=self.rfile)
        print('  ', file=self.rfile)
        print(".. raw:: latex", file=self.rfile)
        print('  ', file=self.rfile)
        print('   \\vspace{2mm}', file=self.rfile)
        print('  ', file=self.rfile)


    def _pdf_array(self, dval):
        """
        print tag [a] - an ascii table from statements or variable

        arrays: [[a], range1, range2, statement, expr,
                    ref, decimals, unit1, unit2]

        """

        set_printoptions(precision=3)

        # table heading
        var = dval[2].split('=')[0].strip()
        tright = dval[5].strip().split(' ')
        eqnum = tright[-1].strip()
        tleft = ' '.join(tright[:-1]).strip()
        ahdpdf = tleft + ' ' + eqnum

        print(' ', file=self.rfile)
        print("**yxxhfillxxx " + var + " = " + ahdpdf + "**",
              file=self.rfile)
        print(' ', file=self.rfile)

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

            print(' ', file=self.rfile)
            print(out1, file=self.rfile)
            print(' ', file=self.rfile)
        except:
            pass

        # strip units from terms and equations and process
        for _j in self.odict:
            try:
                #print(self.odict[_j])
                state = self.odict[_j][1].strip()
                #print('state', state)
                exec(state)
                eval(self.odict[_j][2].strip())
            except:
                pass

            try:
                var = state.split('=')
                state2 = var[0].strip()+'='+var[0].strip()+'.asNumber()'
                exec(state2)
            except:
                pass


        # array from disk or python code
        if len(str(vect[3])) == 0 and len(str(vect[0])) == 0:
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
                        elist2.append(list(_v))
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

            print(ptable, file=self.rfile)
            print('  ', file=self.rfile)
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
            exec(equa1)
            etype = equa1.split('=')[1]
            if etype.strip()[:1] == '[':
                # data is in list form
                alist = []
                alist1 = eval(equa1.split('=')[1])
                for _v in alist1:
                    for _x in _v:
                        alist.append(list(_x))

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

            # create table
            flt1 = "."+str(dval[6]).strip()+"f"


            # create table
            #print(alist)
            ptable = tabulate.tabulate(alist, rlist, 'rst',
                                       floatfmt=flt1)
            print(ptable, file=self.rfile)
            print('  ', file=self.rfile)

    def _pdf_func(self, dval):
        """print tag [f]

        Dictionary:

        Arguments:
        ip: a model line or block

        Dictionary Value:
        function:[[f], function name, ref, model number

        """

        # print reference line

        fhdpdf = dval[2].strip()

        print(' ', file=self.rfile)
        print("**yxxhfillxxx " + fhdpdf + "**", file=self.rfile)
        print(' ', file=self.rfile)



        # evaluate function
        strng_return = eval(dval[1].strip())
        print(' ', file=self.rfile)
        print(pretty(strng_return), file=self.rfile)
        print(' ', file=self.rfile)


        print(".. raw:: latex", file=self.rfile)
        print('  ', file=self.rfile)
        print('   \\vspace{-9mm}', file=self.rfile)
        print('  ', file=self.rfile)
        print(".. raw:: latex", file=self.rfile)
        print('  ', file=self.rfile)
        print('   \\hrulefill', file=self.rfile)
        print('  ', file=self.rfile)
        print(".. raw:: latex", file=self.rfile)
        print('  ', file=self.rfile)
        print('   \\vspace{2mm}', file=self.rfile)
        print('  ', file=self.rfile)

    def _pdf_eq(self, var3, dval):
        """tag [e]

        equations dict:
        [[e], statement, expr, ref, decimals, units, prnt opt]
        key = var3

        """

        # number of decimal places
        #print("set_printoptions(precision="+dval[4].strip()+")")
        #print("Unum.VALUE_FORMAT = '%." + dval[4].strip() + "f'")
        try:
            exec("set_printoptions(precision=" + dval[4].strip() + ")")
            exec("Unum.VALUE_FORMAT = '%." + dval[4].strip() + "f'")
        except:
            set_printoptions(precision=3)
            Unum.VALUE_FORMAT = "%.3f"

        cunit = dval[5].strip()
        var3 = dval[1].split("=")[0].strip()
        val3 = eval(dval[2])

        # evaluate only
        if dval[6].strip() == '0':
            exec(dval[1])
            return

        # result only
        elif dval[6].strip() == '1':
            # print reference line
            strend = dval[3].strip()
            print(' ', file=self.rfile)
            print("**" + var3 + " |" + "yxxhfillxxx " + strend + "**",
                  file=self.rfile)
            print(' ', file=self.rfile)

            for _k in self.odict:
                if _k[0] != '_':
                    #print(type(eval(self.odict[_k][2].strip())))
                    eval(self.odict[_k][2].strip())
                    exec(self.odict[_k][1].strip())

            # print result right justified
            if type(eval(var3)) != Unum:
                if type(eval(var3)) == float or type(eval(var)) == float64:
                    resultform = '{:.' + dval[4].strip()+'f}'
                    result1 = resultform.format(float(eval(var)))
                    print((var3 + " = " + str(result1)).rjust(self.widthp),
                          file=self.rfile)
                else:
                    print((var3 + " = " + str(eval(var3))).rjust(self.widthp),
                          file=self.rfile)
            else:
                if len(cunit) > 0:
                    tmp1 = str(eval(var3).asUnit(eval(cunit)))
                else:
                    tmp1 = str(eval(var3))
                print((var3 + " = " + tmp1).rjust(self.widthp),
                      file=self.rfile)
            return


        # symbolic and substituted forms
        else:
            # print reference line
            strend = dval[3].strip()
            print(' ', file=self.rfile)
            print("**" + var3 + " |" + "yxxhfillxxx " + strend + "**",
                  file=self.rfile)
            print(' ', file=self.rfile)


            # print symbolic form
            for _j in self.symb:
                if str(_j)[0] != '_':
                    varsym(str(_j))

            #print('dval2', dval[2])
            symeq = sympify(dval[2].strip())
            print('  ', file=self.rfile)
            print('.. math:: ', file=self.rfile)
            print('  ', file=self.rfile)
            print('  ' + latex(symeq, mul_symbol="dot"), file=self.rfile)
            print(' ', file=self.rfile)
            print('|', file=self.rfile)


            # substitute values
            # evaluate all terms and equations
            if dval[6].strip() == '3':
                for _k in self.odict:
                    if _k[0] != '_':
                        #print(self.odict[_k][1].strip())
                        exec(self.odict[_k][1].strip())

                symat = symeq.atoms(Symbol)
                symeq1 = sympify(dval[2].strip())

                #rewrite equation - new variables same length as value
                for _n in symat:
                    #get length of eval(variable)
                    evlen = len((eval(_n.__str__())).__str__())
                    new_var = str(_n).ljust(evlen, '~')
                    symeq1 = symeq1.subs(_n, symbols(new_var))
                symat1 = symeq1.atoms(Symbol)
                out2 = pretty(symeq1, wrap_line=False)

                #substitute variables
                for _n in symat1:
                    orig_var = str(_n).replace('~', '')
                    expr = eval((self.odict[orig_var][1]).split("=")[1])
                    if type(expr) == float:
                        form = '{:.' + dval[4].strip()+'f}'
                        symvar1 = form.format(eval(str(expr)))
                    else:
                        symvar1 = eval(orig_var.__str__()).__str__()
                    out2 = out2.replace(str(_n), symvar1)

                print('  ', file=self.rfile)
                print('.. math:: ', file=self.rfile)
                print('  ', file=self.rfile)
                print('  ' + latex(out2, mode='plain'), file=self.rfile)
                print('  ', file=self.rfile)
                print('|', file=self.rfile)

                #convert variables to greek
                if var.strip() in greeks:
                    var1 = "\\" + var.strip()
                else:
                    var1 = var

                if len(cunit.strip()) == 0:
                    out3 = var1 + " = " + str(eval(var))
                    print(' ', file=self.rfile)
                    print('.. math:: ', file=self.rfile)
                    print('  ', file=self.rfile)
                    print("  \\boldsymbol{" + latex(out3, mode='plain') + "}",
                                    file=self.rfile)
                    print('  ', file=self.rfile)
                else:
                    out4 = var1 + " = " + str(eval(var).asUnit(eval(cunit)))
                    print(' ', file=self.rfile)
                    print('.. math:: ', file=self.rfile)
                    print('  ', file=self.rfile)
                    print("  \\boldsymbol{" + latex(out4, mode='plain') + "}",
                                    file=self.rfile)
                    print('  ', file=self.rfile)


            # print result right justified
            if type(eval(var)) != Unum:
                if type(eval(var)) == float or type(eval(var)) == float64:
                    resultform = '{:.' + dval[4].strip()+'f}'
                    result1 = resultform.format(float(eval(var)))
                    print((var + " = " +
                                str(result1)).rjust(self.widthclc-1), 1)
                else:
                    print((var + " = " +
                                str(eval(var))).rjust(self.widthclc-1), 1)
            else:
                if len(cunit) > 0:
                    tmp = str(eval(var).asUnit(eval(cunit)))
                else:
                    tmp = str(eval(var))
                print((var + " = " + tmp).rjust(self.widthclc), 1)


            strend = dval[3].strip()
            print(' ', file=self.rfile)
            print("**" + var + " =" + "yxxhfillxxx " + strend + "**",
                  file=self.rfile)
            print(' ', file=self.rfile)

        print(".. raw:: latex", file=self.rfile)
        print('  ', file=self.rfile)
        print('   \\vspace{-9mm}', file=self.rfile)
        print('  ', file=self.rfile)
        print(".. raw:: latex", file=self.rfile)
        print('  ', file=self.rfile)
        print('   \\hrulefill', file=self.rfile)
        print('  ', file=self.rfile)
        print(".. raw:: latex", file=self.rfile)
        print('  ', file=self.rfile)
        print('   \\vspace{2mm}', file=self.rfile)
        print('  ', file=self.rfile)

    def _pdf_sect(self, dval):

        """print [s]

        Dictionary:
        section: ['[s]', sleft, state, file]

        """

        tleft = dval[1].strip()
        tright = dval[3].strip()
        print('  ', file=self.rfile)
        print(tleft.strip() + " xxxhfillxxx " + tright.strip(),
              file=self.rfile)
        print("-"*self.pdfwidth, file=self.rfile)
        notes = '\n'.join([i.strip() for i in dval[2]])
        if len(notes.strip()) > 0:
            print(notes + '\n', file=self.rfile)
        print(' ', file=self.rfile)
        print(".. raw:: latex", file=self.rfile)
        print(' ', file=self.rfile)
        print('   \\vspace{4mm}', file=self.rfile)
        print(' ', file=self.rfile)

    def _pdf_txt(self, txt):
        """output pass-through text"""
        print(txt[1].strip(), file=self.rfile)

    def _pdf_blnk(self):
        print(' ', file=self.rfile)
