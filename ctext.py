from __future__ import division
from __future__ import print_function
import codecs
import sys
import os
import tabulate
from numpy import *
from sympy import *
from sympy import var as varsym
from unum import Unum
import oncemod.config as om

try:
    from unitc import *
except:
    from oncemod.calcunits import *


class CalcText(object):
    """Return calc files

        Files:
        model_ncal.txt: TF-8 file with formatted and solved calculations
        model_nsum.txt: model section summary for database
        model_n.py    : terms, equations and arrays in Python form

        Methods:
        prt_py()
        prt_summary()

        """
    def __init__(self, odict, calcf, pyf, sumf, mpath):
        """Return calc files

        Files:
        model_ncal.txt: TF-8 file with formatted and solved calculations
        model_nsum.txt: model section summary for database
        model_n.py    : terms, equations and arrays in Python form

        """

        self.odict = odict
        self.pyfile = pyf
        self.sumfile = sumf
        self.mpath = mpath

        self.width_calc = 90
        self.xtraline = False

        # get list of equation symbols
        self.symb = self.odict.keys()
        self.cfile = codecs.open(calcf, 'w', encoding='utf8')
        for _i in self.odict:
            mtag = self.odict[_i][0]
            #print(mtag)
            if mtag ==   '[e]':
                self._prt_eq(_i, self.odict[_i])
                self.xtraline = False
            elif mtag == '[a]':
                self._prt_array(self.odict[_i])
                self.xtraline = True
            elif mtag == '[s]':
                self._prt_sect(self.odict[_i])
                self.xtraline = False
            elif mtag == '[y]':
                self._prt_yp(self.odict[_i])
                self.xtraline = True
            elif mtag == '[d]':
                self._prt_disk(self.odict[_i])
                self.xtraline = False
            elif mtag == '[o]':
                self._prt_o(self.odict[_i])
                self.xtraline = False
            elif mtag == '[t]':
                self._prt_term(self.odict[_i])
                self.xtraline = True
            elif mtag == '[x]':
                self._prt_txt(self.odict[_i])
                self.xtraline = False
            elif mtag == '[~]' and self.xtraline is False:
                self.xtraline = True
            elif mtag == '[~]' and self.xtraline is True:
                self._prt_blnk()
        self.cfile.close()
        # print ipython file
        self.prt_py()
        # print calc summary file
        self.prt_summary()
        #for _i in self.odict: print(i, self.odict[i])

    def _prt_both(self, mentry, pp):
        """send output to utf-8 encoded file"""
        if pp:
            mentry = pretty(mentry, use_unicode=True, num_columns=92)
        #print(mentry)
        print(mentry, file=self.cfile)

    def _prt_eq(self, var3, eq):
        """print tag [e]

        Dictionary:
        equations:[[e], statement, expr, ref, decimals, units, prnt opt]

        """
        # Unum settings
        Unum.VALUE_FORMAT = "%.2f"
        Unum.UNIT_INDENT = ""
        set_printoptions(precision=3)

        # print summary if code = 1
        if eq[6].strip() == '' or eq[6].strip() == '2':
            pass
        elif eq[6].strip() == '0':
            return
        elif eq[6].strip() == '1':
            val3 = eval(eq[2])
            strend = eq[3].strip()
            self._prt_both(' ', 0)
            self._prt_both((var3 + " = " +
                           str(val3)).ljust(self.width_calc -
                                            len(strend)) + strend, 1)
            return

        # print reference line
        strend = eq[3].strip()
        self._prt_both(self.width_calc * '_', 0)
        self._prt_both((var3 + " =").ljust(self.width_calc -
                        len(strend)) + strend, 1)
        self._prt_both(" ", 1)
        # convert variables to symbols except for arrays
        for _j in self.symb:
            if str(_j)[0] != '_':
                varsym(str(_j))

        # print symbolic form
        #print(eq[2].strip())
        symeq = eval(eq[2].strip())
        out1 = symeq
        #print(out1)
        self._prt_both(out1, 1)
        self._prt_both(" ", 0)

        # numerically evaluate terms and equations
        for _k in self.odict:
            if _k[0] != '_':
                exec(self.odict[_k][1].strip())

        # substitute values
        subval =[]
        symat = symeq.atoms(Symbol)
        for _i in symat:
            expr = str(self.odict[str(_i)][1]).split("=")[1].strip()
            symvar = str(eval(expr))
            symvar2 = symbols(symvar)
            subval.append(symvar2)
        subvalzip = zip(symat, subval)
        #print(symat, subval)
        # substitute values
        out2 = symeq.subs(subvalzip)
        out2p = out2

        #print substituted form
        var = eq[1].split("=")[0].strip()
        cunit = str(eq[5].strip())
        self._prt_both(out2p, 1)
        self._prt_both(" ", 0)

        # print result
        if len(cunit.strip()) == 0:
            self._prt_both(var + " = " + str(eval(var)), 1)
        else:
            self._prt_both(var + " = " +
                          str(eval(var).asUnit(eval(cunit))), 1)
        self._prt_both(self.width_calc * '_', 0)
        self._prt_both(self.width_calc * '.', 0)
        self._prt_both(" ", 0)

    def _prt_array(self, mstrng):
        """print tag [a]

        Dictionary:
        arrays: [[a], range1, range2, statement, expr,
        ref, decimals, unit1, unit2]

        """
        # strip units from equations and process
        for _j in self.odict:
            try:
                state = self.odict[_j][1].strip()
                exec(state)
                var = state.split('=')
                state2 = var[0].strip()+'='+var[0].strip()+'.asNumber()'
                exec(state2)
            except:
                pass

        set_printoptions(precision=3)

        # table heading
        tright = mstrng[5]
        tright = mstrng[5].strip().split(' ')
        eqnum = tright[-1].strip()
        tleft = ' '.join(tright[:-1]).strip()
        self._prt_both(tleft + ' '*(self.width_calc - len(tleft +
                        eqnum)) + eqnum, 0)

        vect = mstrng[1:]
        # pre-calculated array from disk or python code
        if len(str(vect[1])) == 0 and len(str(vect[2])) == 0:
            pass

        # single row vector
        if len(str(vect[1])) == 0 and len(str(vect[2])) != 0:
            # process range variable 1 and heading
            rnge1 = vect[0]
            exec(rnge1.strip())
            rnge1a = rnge1.split('=')
            rlist = [vect[6].strip() + ' = ' +
                     str(_r)for _r in eval(rnge1a[1])]
            #process equation
            equa1 = vect[2].strip()
            exec(equa1)
            var2 = vect[2].strip().split('=')[0]
            elist1 = eval(var2)
            elist2 = elist1.tolist()
            elist2 = [elist2]

            # create table
            ptable = tabulate.tabulate(elist2, rlist, 'rst',
                                       floatfmt=".4f")
            self._prt_both(ptable, 1)
            #self._prt_both(self.width_calc * "_")
            #print(ptable)

        # table
        if len(str(vect[1])) != 0 and len(str(vect[2])) != 0:
            # process range variable 1
            rnge1 = vect[0]
            exec(rnge1.strip())
            rnge1a = rnge1.split('=')
            rlist = [vect[6].strip() + ' = ' +
                     str(_r)for _r in eval(rnge1a[1])]


            # process range variable 2
            rnge2 = vect[1]
            exec(rnge2.strip())
            rnge2a = rnge2.split('=')
            clist = [str(_r).strip()for _r in eval(rnge2a[1])]
            rlist.insert(0, vect[7].strip())

            # process equation
            equa1 = vect[2].strip()
            exec(equa1)
            equa1a = vect[2].strip().split('=')
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

            for n, _p in enumerate(alist):
                _p.insert(0, clist[n])
            #print(alist)

            # create table

            ptable = tabulate.tabulate(alist, rlist, 'rst')
            nstr = pretty(ptable, use_unicode=True, num_columns=92)
            self._prt_both(nstr, 1)

    def _prt_sect(self, txt):
        """print [s]

        Dictionary:
        section: ['[s]', sleft, sright, sdir, state]

        """
        tleft = txt[1]
        tright = txt[2].strip()
        self._prt_both('='*self.width_calc, 0)
        self._prt_both(tleft.ljust(self.width_calc)[:-(len(tright)+1)] +
                      tright, 1)
        self._prt_both('='*self.width_calc, 0)
        note = [i.strip() for i in txt[4]]
        if len(note) > 10:
            note = note[:10]
        notes = '\n'.join(note)
        if len(notes) > 0:
            self._prt_both(notes + '\n', 0)

    def _prt_yp(self, ip):
        pass

    def _prt_disk(self, ip):
        pass

    def _prt_o(self, ratio):
        """print [o]

        Dictionary:
        compare: ['[o]', chk expression, limit, ref, ok]

        """
        # convert variables to symbols
        for _j in self.symb:
            if _j[0] != '_':
                varsym(_j)

        # print symbolic form
        symeq1 = eval(ratio[1].strip() + ' ' + ratio[2].strip())
        symeq2 = eval(ratio[1].strip())

       # evaluate variables
        for _k in self.odict:
            if _k[0] != '_':
                #print(self.odict[_k][1].strip())
                exec(self.odict[_k][1].strip())

        # substitute values
        #print(ratio[1].strip() + ' ' + ratio[2].strip())
        nounits = eval(ratio[1].strip()).asNumber()
        result = eval(str(nounits) + ' ' + ratio[2].strip())
        subval =[]
        symat = symeq2.atoms(Symbol)
        for _j in symat:
            symvar2 = str(eval(str(_j)))
            symvar = symbols(symvar2)
            subval.append(symvar)
        subvalzip = zip(symat, subval)
        out2 = symeq2.subs(subvalzip)
        out3 = eval(ratio[1].strip())
        if result:
            comment = '  ' + ratio[4].strip()
        else:
            comment = '  *** not ' + ratio[4].strip() + ' ***'

        # clean output
        out2p = pretty((symeq1, '  ', out2, '=', out3, comment))
        repc = [(',', ' '), ('(', ' '), (')', ' ')]
        out2a = out2p
        for _k in repc:
            out2a = out2a.replace(_k[0],_k[1])
        strend = ratio[3].strip()
        self._prt_both(self.width_calc * '_', 0)
        self._prt_both(strend.rjust(self.width_calc), 1)
        self._prt_both(out2a, 1)
        self._prt_both(" ", 0)
        self._prt_both(self.width_calc * '_', 0)
        self._prt_both(self.width_calc * '.', 0)
        self._prt_both(" ", 0)

    def _prt_term(self, par):
        """print [t]

        Dictionary:
        terms: [[t], statement, expr, ref ]

        """
        strend = par[3].strip() + ' '*10
        param = ' '*4 + '| ' + par[1].strip()
        self._prt_both(param.ljust(self.width_calc-len(strend))
                      + strend, 1)

    def _prt_txt(self, txt):
        """print pass-through text"""
        self._prt_both(txt[1].rstrip(), 0)

    def _prt_blnk(self):
        self._prt_both(' ', 0)

    def prt_py(self):
        """write python code to file from dictionary"""

        pyfile1 = open(self.pyfile, 'w')
        #write import commands
        importstr = str("\n".join(["from numpy import *",
                        "from collections import OrderedDict",
                        "try:",
                        "   from unum import Unum",
                        "except:",
                        " print 'unum module not found'",
                        "pass",
                        "import sys",
                        "sys.path.append('{}')",
                        "try:",
                        "   from unitc import *",
                        "   print 'unitc imported'",
                        "except: ",
                        "    try:",
                        "        from calcunits import *",
                        "    except:",
                        "       print ' '",
                        "       print 'unitc not found' ",
                        "       pass"]).format(self.mpath))

        pyfile1.write(importstr + 2*"\n")

        # write statements for IPython
        for _j in self.odict:
            mtype = self.odict[_j][0]
            if mtype == '[t]':
                pyfile1.write(self.odict[_j][1].strip()+'\n')
            elif mtype == '[e]':
                pyfile1.write(self.odict[_j][1].strip()+'\n')
            elif mtype == '[a]':
                    if len(self.odict[_j][1].strip()):
                        pyfile1.write(self.odict[_j][1].strip() +'\n')
                    if len(self.odict[_j][2].strip()):
                        pyfile1.write(self.odict[_j][2].strip() + '\n')

        # write dictionary of variables for IPython
        pdict = {}
        for _k in self.odict:
            if _k[0] != '_':
                pdict[str(_k).strip()] = [self.odict[_k][1].strip(),
                                    self.odict[_k][2].strip()]
            if _k == '_a':
                rng1 = self.odict[_k][1].split('=')
                rng2 = self.odict[_k][2].split('=')
                pdict[str(rng1[0]).strip()] = [self.odict[_k][1].strip(),
                                  rng1[1].strip()]
                pdict[(rng2[0]).strip()] = [self.odict[_k][2].strip(),
                                  rng2[1].strip()]
        pyfile1.write(str('_md =  ') + str(pdict))
        pyfile1.close()

    def prt_summary(self):
        """write model file summary to stdout

        equations:[[e], statement, expr, ref, decimals, units, opt]
        arrays:   [[a], statements, ref, decimals, unit1, unit2]
        sections: [[s], left string, right string, directives, notes]

        """
        sumfile = open(self.sumfile, 'w')
        for i in self.odict:
            mtype = self.odict[i][0]
            if mtype == '[e]':
                sumfile.write(self.odict[i][3].strip()+'\n')
            elif mtype == '[a]':
                sumfile.write(self.odict[i][2].strip()+'\n')
            elif mtype == '[s]':
                sumfile.write(self.odict[i][1].strip()+'\n')
                sumfile.write(self.odict[i][2].strip()+'\n')
                for j in self.odict[i][4]:
                    sumfile.write(j.strip()+'\n')
        sumfile.close()
