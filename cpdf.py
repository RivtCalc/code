from __future__ import division
from __future__ import print_function
import sys
import os
import tabulate
import codecs
from unum import Unum
from numpy import *
from sympy import *
from sympy import var as varsym
#from sympy.printing.latex import tex_greek_dictionary as texdict
from sympy.core.alphabets import greeks
import oncemod.config as om
try:
    from unitc import *
except:
    from oncemod.calcunits import *

class CalcPDF(object):
    """
    Accepts a dictionary of equation and text inputs
    and returns a formatted reStructuredText-LaTeX PDF file
    with completed calculations.

    **methods**

    pdf_valid()
    prt_rst()
    _prt_eq()
    _prt_array()
    _prt_sect()
    _prt_yp()
    _prt_disk()
    _prt_o()
    _prt_term()
    _prt_txt()
    _prt_blnk()
    """

    def __init__(self, odict, mpath, mfile):
        """
        initialize files and equation symbol list

        output to stdout and to files:
            rfilename = reStructuredText output file
            pfilename = PDF output file

        """
        # check if PDF write is needed
        mofile = open(mfile, 'r')
        self.mstr = mofile.readlines()
        mofile.close()

        self.rfilename = mfile.replace('.txt', '.rst')
        self.pfilename = mfile.replace('.txt', '.pdf')


        self.cfolder = mpath
        self.setfile = 'set.txt'
        self.setpath = mpath
        self.pdflag = 0
        self.pfiletype = ''
        self.rfile = ''
        self.prfilename = ''
        self.previous = ''

        self.pdfwidth = 70   # width of lines with terms
        self.odict = odict
        self.xtraline = False
        self.symb = self.odict.keys()
        self.symblist = []


        # get set file
        for i in self.mstr:
            mtag = i[0:10]
            if mtag == "[#] format":
                ilist = i[10:].split('|')
                if len(ilist[2].strip()) > 0:
                    self.setpath = ilist[2]
                    self.setpath = os.path.abspath(self.setpath)
                if len(ilist[3].strip()) > 0:
                    self.setfile = ilist[2]

        # get PDF or rst file name
        try:
            pfil = '/'.join([self.setpath, self.setfile])
            pfile = open(pfil,'r')
            self.pstr = pfile.readlines()
            pfile.close()
            for i in self.pstr:
                if len(i.strip()) > 0:
                    if i.strip()[:3] == '[p]':
                        self.prname = i[3:].strip()
                        self.prtype = self.prname.split('.')[-1]
                        if self.prtype == 'rst':
                            self.pdflag = 1
                        elif self.prtype == 'pdf':
                            self.pdflag = 2
                        else:
                            self.pdflag = 0
        except:
            pass

    def prt_rst(self):
        """ write rst file """

        self.rfile = codecs.open(self.rfilename, 'w', encoding='utf8')
        for i in self.odict:
            mtag = self.odict[i][0]
            #print(mtag)
            if mtag ==   '[e]':
                self.prt_eq(i, self.odict[i])
                self.xtraline = False
            elif mtag == '[a]':
                self.prt_array(self.odict[i])
                self.xtraline = True
            elif mtag == '[s]':
                self.prt_sect(self.odict[i])
                self.xtraline = False
            elif mtag == '[y]':
                self.prt_yp(self.odict[i])
                self.xtraline = False
            elif mtag == '[d]':
                self.prt_disk(self.odict[i])
                self.xtraline = False
            elif mtag == '[o]':
                self.prt_o(self.odict[i])
                self.xtraline = False
            elif mtag == '[t]':
                self.prt_term(self.odict[i])
                self.xtraline = True
            elif mtag == '[x]':
                self.prt_txt(self.odict[i])
                self.xtraline = False
            elif mtag == '[~]' and self.xtraline is False:
                self.xtraline = True
            elif mtag == '[~]' and self.xtraline is True:
                self.prt_blnk()
            self.previous = mtag
        self.rfile.close()
        #for i in self.odict: print(i, self.odict[i])

    def prt_eq(self, var, eq):
        """
        tag [e]
        equations:[[e], statement, expr, ref, decimals, units, prnt opt]
        var = odict key

        """

        # Unum settings
        Unum.VALUE_FORMAT = "%.2f"
        Unum.UNIT_INDENT = ""
        set_printoptions(precision=3)

        # print summary only if code = 1
        if eq[6].strip() == '' or eq[6].strip() == '2':
            pass
        elif eq[6].strip() == '0':
            return
        elif eq[6].strip() == '1':
            val = eval(eq[2])
            strend = eq[3].strip()
            print(' ', file=self.rfile)
            print((var+" = " + str(val)).ljust(self.pdfwidth-len(strend)) +
                  strend, file=self.rfile)
            print(' ', file=self.rfile)
            return

        # print reference line
        strend = eq[3].strip()
        print(' ', file=self.rfile)
        print("**" + var + " =" + "yxxhfillxxx " + strend + "**",
              file=self.rfile)
        print(' ', file=self.rfile)

        # convert variables to symbols except for arrays
        # get list of equation symbols
        for _i in self.symb:
            if str(_i[0]) != '_':
                varsym(str(_i))

        # print symbolic form
        symeq = eval(eq[2].strip())
        print('  ', file=self.rfile)
        print('.. math:: ', file=self.rfile)
        print('  ', file=self.rfile)
        print('  ' + latex(symeq, mul_symbol="dot"), file=self.rfile)
        print(' ', file=self.rfile)
        print('|', file=self.rfile)

        # numerically evaluate terms and equations
        for _k in self.odict:
            if _k[0] != '_':
                exec(self.odict[_k][1].strip())

        # substitute values
        subval =[]
        symat = symeq.atoms(Symbol)
        for _i in symat:
            expr =str(self.odict[str(_i)][1]).split("=")[1].strip()
            symvar = str(eval(expr))
            symvar = symbols(symvar)
            subval.append(symvar)
        subvalzip = zip(symat, subval)
        # substitute values
        out2 = symeq.subs(subvalzip)

        var = eq[1].split("=")[0].strip()
        cunit = str(eq[5].strip())
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

    def prt_array(self, mstrng):
        """
        print tag [a] - an ascii table from statements or variable

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
        tright = mstrng[5].strip().split(' ')
        eqnum = tright[-1]
        tleft = ' '.join(tright[:-1])

        print('  ', file=self.rfile)
        print(".. raw:: latex", file=self.rfile)
        print('  ', file=self.rfile)
        print('   \\vspace{3mm}', file=self.rfile)
        print('  ', file=self.rfile)
        print("**" + tleft + "yxxhfillxxx " + eqnum + "**",
              file=self.rfile)
        print('  ', file=self.rfile)

        vect = mstrng[1:]
        # pre-calculated array from disk or python code
        if len(str(vect[1])) == 0 and len(str(vect[2])) == 0:
            pass

        # single row vector
        if len(str(vect[1])) == 0 and len(str(vect[2])) != 0:
            # range variable 1
            rnge1 = vect[0]
            exec(rnge1.strip())
            rnge1a = rnge1.split('=')
            rlist = [vect[6].strip() + ' = ' +
                     str(i)for i in eval(rnge1a[1])]
            #process equation
            equa1 = vect[2].strip()
            exec(equa1)
            var = vect[2].strip().split('=')[0]
            elist1 = eval(var)
            elist2 = elist1.tolist()
            elist2 = [elist2]

            # create table
            ptable = tabulate.tabulate(elist2, rlist, 'rst')
            #print(ptable)
            print(ptable, file=self.rfile)
            print('  ', file=self.rfile)

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
            clist = [str(_i)for _i in eval(rnge2a[1])]
            rlist.insert(0, vect[7].strip())

            # process equation
            equa1 = vect[2].strip()
            equa1a = vect[2].strip().split('=')
            equa2 = equa1a[1]
            rngx = rnge1a[1]
            rngy = rnge2a[1]
            ascii1 = rnge1a[0].strip()
            ascii2 = rnge2a[0].strip()

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
            ptable = tabulate.tabulate(alist, rlist, 'rst',
                                       floatfmt=".4f")
            print(ptable, file=self.rfile)
            print('  ', file=self.rfile)

    def prt_sect(self, txt):
        """
        print [s]
        sections: [[s], left string, right string, directives, notes]

        """
        tleft = txt[1].strip()
        tright = txt[2].strip()
        print('  ', file=self.rfile)
        print(tleft.strip() + " xxxhfillxxx " + tright.strip(),
              file=self.rfile)
        print("-"*self.pdfwidth, file=self.rfile)
        notes = '\n'.join([i.strip() for i in txt[4]])
        if len(notes.strip()) > 0:
            print(notes + '\n', file=self.rfile)
        print(' ', file=self.rfile)
        print(".. raw:: latex", file=self.rfile)
        print(' ', file=self.rfile)
        print('   \\vspace{4mm}', file=self.rfile)
        print(' ', file=self.rfile)

    def prt_yp(self, ip):
        pass
    def prt_disk(self, i):
        pass

    def prt_o(self, ratio):
        """
        print [o]
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
        nounits = eval(ratio[1].strip()).asNumber()
        result = eval(str(nounits) + ' ' + ratio[2].strip())
        symat = symeq2.atoms(Symbol)
        subval =[]
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
            out2a = out2a.replace(_k[0], _k[1])
        strend = ratio[3].strip()
        print('  ', file=self.rfile)
        print("**" + "yxxhfillxxx " + strend + "**", file=self.rfile)
        print('  ', file=self.rfile)

        print('::', file=self.rfile)
        print(' ', file=self.rfile)
        print(out2a, file=self.rfile)
        print(' ', file=self.rfile)

        print(".. raw:: latex", file=self.rfile)
        print('  ', file=self.rfile)
        print('   \\hrulefill', file=self.rfile)
        print('  ', file=self.rfile)
        print(".. raw:: latex", file=self.rfile)
        print('  ', file=self.rfile)
        print('   \\vspace{2mm}', file=self.rfile)
        print('  ', file=self.rfile)

    def prt_term(self, par):
        """
        output terms
        terms: [[t], statement, expr, ref ]

        """
        strend = par[3].strip()
        param = '  ' + par[1].strip()
        print(' ', file=self.rfile)
        print('::', file=self.rfile)
        print(' ', file=self.rfile)
        print(param.ljust(self.pdfwidth-len(strend)) + strend,
                file=self.rfile)

    def prt_txt(self, txt):
        """output pass-through text"""
        print(txt[1].strip(), file=self.rfile)

    def prt_blnk(self):
        print(' ', file=self.rfile)
