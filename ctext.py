from __future__ import division
from __future__ import print_function
from oncepy import ccheck
import codecs
import sys
import os
import tabulate
import time
from numpy import *
from sympy import *
from sympy import var as varsym
import oncepy.oconfig as cfg

from unum import Unum
mfile = os.getcwdb()
try:
    from unitc import *
    cfg.unitfile = 'model folder'
except ImportError:
    try:
        os.chdir(os.pardir)
        from unitc import *
        cfg.unitfile = 'project folder'
        os.chdir(mfile)
    except ImportError:
        from oncepy.unitc import *
        cfg.unitfile = 'built-in'

class CalcText(object):
    """Return calc files

        Files:
        model.calnnn.txt: UTF-8 file with formatted and solved calculations
        model.sumnnn.txt: model section summary for database
        model.nnn.py    : terms, equations and arrays in Python form

        Methods:
        _prt_py()
        _prt_summary()

        """

    def __init__(self, odict, calcf, pyf, sumf, mpath):
        """Return calc files

        Files:
        model.calnnn.txt: UTF-8 file with formatted and solved calculations
        model.sumnnn.txt: model section summary for database
        model.nnn.py    : terms, equations and arrays in Python form

        """
        # execution log
        self.ew = ccheck.ModCheck()

        self.odict = odict
        self.pyfile = pyf
        self.sumfile = sumf
        self.mpath = mpath
        self.fignum = 0

        self.widthc = 90
        self.xtraline = False

        # get list of equation symbols
        self.symb = self.odict.keys()
        self.cfile = codecs.open(calcf, 'w', encoding='utf8')

        # print date at top of calc
        self._prt_utf(time.strftime("%c"), 0)

        for _i in self.odict:
            #print(_i, self.odict[_i])
            mtag = self.odict[_i][0]
            #print(mtag)
            if mtag == '[c]':
                self._prt_check(self.odict[_i])
                self.xtraline = True
            elif mtag == '[a]':
                self._prt_array(self.odict[_i])
                self.xtraline = True
            elif mtag == '[f]':
                self._prt_func(self.odict[_i])
                self.xtraline = True
            elif mtag == '[e]':
                self._prt_eq(_i, self.odict[_i])
                self.xtraline = False
            elif mtag == '[s]':
                self._prt_sect(self.odict[_i])
                self.xtraline = False
            elif mtag == '[d]':
                self._prt_disk(self.odict[_i])
                self.xtraline = False
            elif mtag == '[o]':
                self._prt_olic(self.odict[_i])
                self.xtraline = False
            elif mtag == '[t]':
                self._prt_term(self.odict[_i])
                self.xtraline = True
            elif mtag == '[x]':
                self._prt_txt(self.odict[_i])
                self.xtraline = True
            elif mtag == '[~]' and self.xtraline is False:
                self.xtraline = True
            elif mtag == '[~]' and self.xtraline is True:
                self._prt_blnk()
            else:
                continue
        # close calc file
        self.cfile.close()
        # print ipython file
        self._prt_py()
        # print calc summary file
        self._prt_summary()

        #for _i in self.odict: print(i, self.odict[i])

    def _prt_utf(self, mentry, pp):
        """write output to utf-8 encoded file"""
        if pp:
            mentry = pretty(mentry, use_unicode=True, num_columns=92)
        print(mentry, file=self.cfile)

    def _prt_disk(self, dval):

        """print tag [d]

        Dictionary Value:
        equation:[[d], file path, parameter, var1, var2]

        options:
        s: run a python script
        t: add text file contents to output
            (no operations are processed.)
        o: run an external operating system command and
            wait for completion.
        w: write values of variable to file. w+ appends to file.
        f: insert jpg, png etc, figures into calc
        i: insert and process external model file.  Integrate
            sections and equation numbering.
        r: read file data into variable
        e: edit external file - replace lines
        """

        _prt_log = self.ew.ewrite1

        fpath = dval[1].strip()
        fp = os.path.abspath(fpath)
        option = dval[2].strip()
        param1 = dval[3].strip()
        param2 = dval[4].strip()
        param3 = dval[5].strip()

        var3 = ''

        # relative path specified for the following options
        if option == 's':
            f = open(fp, 'r')
            fr = f.read()
            f.close()
            exec(fr, globals())
            link1 = "< execute python script: " + str(fp) + " >"
            _prt_log(link1)
            _prt_log("file: " + fpath + " compiled")

        elif option == 't':
            mpath2 = os.getcwd()
            os.chdir(os.pardir)
            fp = os.path.abspath(fpath)
            os.chdir(mpath2)
            f = open(fp, 'r')
            tstrng = f.readlines()
            f.close()
            if var1.strip() != '':
                instxt = eval('tstrng[' + var1.strip() + ']')
                instxt = ''.join(instxt)
            else:
                instxt = ''.join(tstrng)
            mkey = '_x'+str(self.midx)
            self.mdict[mkey] = ['[x]', instxt]
            link1 = "< insert text from file: " + str(fp) + " >"
            _prt_log(link1)
            _prt_log('')

        elif option == 'o':
            os.system(fpath)
            link1 = "< execute command: " + str(fp) + " >"
            _prt_log(link1)
            _prt_log('')

        elif option == 'w':
            var2 = array(var1)
            dim2 = var2.shape[0]
            for rows in range(dim2):
                var3 += str(var2[rows]) + '\n'
            f = open(fp, 'w')
            f.write(var3)
            f.close()
            link1 = "< write variable " + var1 + " to file: " \
                    + str(fp) + ">"
            _prt_log(link1)

        elif option == 'w+':
            var2 = array(var1)
            dim2 = var2.shape[0]
            for rows in range(dim2):
                var3 += str(var2[rows]) + '\n'
            f = open(fp, 'w+')
            f.write(var3)
            f.close()
            link1 = "< append variable " + var1 + " to file: " \
                    + str(fp) + ">"
            _prt_log(link1)

        elif option == 'f':
            # insert figure in utf-8 document
            self.fignum += 1
            link1 = "<insert figure " + str(self.fignum) + '. ' \
                    + " file: " + str(fpath) + '>'
            _prt_log(link1)
            link2 = "<Figure " + str(self.fignum) + '. ' + param1 \
                    + " file: " + str(fpath) + '>'
            self._prt_utf(link2, 1)
            self._prt_utf(" ", 0)


        elif option == 'i':
            # this param is handled in ModDicts.__init__
            link1 = "< insert model from file: " + str(fpath) + " >"
            _prt_log(link1)
            pass

        # absolute path specified for the following options
        elif option == 'r':
            file1 = open(fpath, 'r')
            tmpeval = file1.read()
            file1.close()
            var3 = tmpeval.strip().split(' ')
            expr = ','.join(var3)
            state = str(var1) + " = " + expr
            self.mdict[str(var1)] = ['[t]', state, expr, fpath,
                                     os.path.basename(fpath)]
            #print('mdict', self.mdict[str(var1)])
            link1 = "< variable " + var1 + " read from file: " \
                    + str(fpath) + ">"
            _prt_log(link1)


        elif option == 'e':
            editlist = [var1]
            for item in ivect[1:]:
                editlist.append(item)
            var1 = editlist
            # open file to edit
            f = open(fpath, 'r')
            oldfile = f.readlines()
            f.close()

            # read lines to edit
            for lines in var1[1:-1]:
                mod = lines.split('|')

            # edit file
                nl1 = mod[1].split(' ')
                nla = mod[1]
                for terms in nl1:
                    nl2 = terms.split(' ')
                    for keys in self.mdict:
                        mtag = self.mdict[keys][0]
                        if mtag == '[t]':
                            for term in nl2:
                                if keys == term[1:].strip():
                                    nla = nla.replace('%'+str(keys),
                                    str(eval(self.mdict[keys][2])))
                oldfile[int(mod[0])] = nla+"\n"

            # write edited file
            if var1[0] != '':
                newfile1 = os.path.basename(fpath)
                newfile1 = newfile1.split('.')
                newfile2 = '.'.join([str(newfile1[0]) +
                                var1[0].strip(), newfile1[1]])
                newfile = os.path.join(os.path.dirname(fpath),
                                       newfile2)
            else:
                newfile = fpath

            f = open(newfile, 'w')
            writefile = ''.join(oldfile)
            f.write(writefile)
            f.close()

            link1 = "< edit file: " + str(fpath) + " >"
            _prt_log(link1)

        else:
            pass

    def _prt_olic(self, dval):
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
        self._prt_utf(out3.replace('<=', '='), 1)
        self._prt_utf(" ", 0)

    def _prt_term(self, dval):
        """print [t]

        Dictionary:
        terms: [[t], statement, expr, ref ]

        """
        shift = int(self.widthc / 2.8)
        ref = dval[3].strip().ljust(shift)
        param = dval[1].strip()
        ptype = type(eval(dval[2]))
        if ptype == list or ptype == ndarray or ptype == tuple:
            param = param.split('=')[0].strip()
        self._prt_utf(" "*4 + ref + " | " + param,  1)

    def _prt_check(self, dval):
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
        tmp = int(self.widthc-1) * '-'
        self._prt_utf((tmp + u'\u2510').rjust(self.widthc), 0)
        self._prt_utf(strend.rjust(self.widthc), 1)
        self._prt_utf(" ", 0)
        self._prt_utf(pretty(symeq1), 1)
        self._prt_utf(out2p.rjust(self.widthc-1), 1)
        tmp = int(self.widthc-1) * '-'
        self._prt_utf((tmp + u'\u2518').rjust(self.widthc), 0)
        self._prt_utf(" ", 0)

    def _prt_array(self, dval):
        """print tag [a]

        Dictionary:
        arrays: [[a], statement, expr, range1, range2,
                    ref, decimals, unit1, unit2]

        """

        set_printoptions(precision=3)

        # table heading
        tmp = int(self.widthc-1) * '-'
        self._prt_utf((tmp + (u'\u2510')).rjust(self.widthc), 0)
        tright = dval[5].strip().split(' ')
        eqnum = tright[-1].strip()
        tleft = ' '.join(tright[:-1]).strip()
        self._prt_utf((tleft + ' ' + eqnum).rjust(self.widthc), 0)

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

            self._prt_utf(" ", 0)
            self._prt_utf(out1, 1)
            self._prt_utf(" ", 0)
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
            table1 = tabulate
            ptable = table1.tabulate(elist2, rlist, 'rst',
                                floatfmt="."+dval[6].strip()+"f")

            self._prt_utf(ptable, 1)
            tmp = int(self.widthc-1) * '-'
            self._prt_utf((tmp + u'\u2518').rjust(self.widthc), 0)
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
            table2 = tabulate
            flt1 = "."+str(dval[6]).strip()+"f"
            ptable = table2.tabulate(alist, rlist, 'rst', floatfmt=flt1)
            nstr = pretty(ptable, use_unicode=True, num_columns=92)

            # print table
            self._prt_utf(nstr, 1)
            tmp = int(self.widthc-1) * '-'
            self._prt_utf((tmp + u'\u2518').rjust(self.widthc), 0)

    def _prt_func(self, dval):
        """print tag [f]

        Dictionary:

        Arguments:
        ip: a model line or block

        Dictionary Value:
        function:[[f], function name, ref, model number

        """

        # print reference line
        tmp = int(self.widthc-1) * '-'
        self._prt_utf((tmp + u'\u2510').rjust(self.widthc), 0)

        strend = dval[2].strip()
        self._prt_utf(strend.rjust(self.widthc), 0)
        self._prt_utf(" ", 1)

        # evaluate function
        self._prt_utf(dval[1].strip(), 0)
        strng_return = eval(dval[1].strip())
        self._prt_utf(' ', 0)
        self._prt_utf(strng_return, 0)
        self._prt_utf(' ', 0)


        tmp = int(self.widthc-1) * '-'
        self._prt_utf((tmp + u'\u2518').rjust(self.widthc), 0)
        self._prt_utf(" ", 0)

    def _prt_eq(self, var3, dval):
        """print tag [e]

        Dictionary:
        equations:[[e], statement, expr, ref, decimals, units, prnt opt]

        """

        #number of decimal places
        #print("set_printoptions(precision="+dval[4].strip()+")")
        #print("Unum.VALUE_FORMAT = '%." + dval[4].strip() + "f'")
        try:
            exec("set_printoptions(precision=" + dval[4].strip() + ")")
            exec("Unum.VALUE_FORMAT = '%." + dval[4].strip() + "f'")
        except:
            set_printoptions(precision=3)
            Unum.VALUE_FORMAT = "%.3f"

        cunit = dval[5].strip()
        var = dval[1].split("=")[0].strip()

        # evaluate only
        if dval[6].strip() == '0':
            exec(dval[1])
            return

        # result only
        elif dval[6].strip() == '1':
            tmp = int(self.widthc-1) * '-'
            self._prt_utf((tmp + u'\u2510').rjust(self.widthc), 1)
            strend = dval[3].strip()
            self._prt_utf((var3 + " | " + strend).rjust(self.widthc), 0)
            self._prt_utf(" ", 1)

            for _k in self.odict:
                if _k[0] != '_':
                    #print(type(eval(self.odict[_k][2].strip())))
                    eval(self.odict[_k][2].strip())
                    exec(self.odict[_k][1].strip())

            # print result right justified
            if type(eval(var)) != Unum:
                if type(eval(var)) == float or type(eval(var)) == float64:
                    resultform = '{:.' + dval[4].strip()+'f}'
                    result1 = resultform.format(float(eval(var)))
                    self._prt_utf((var + " = " +
                                str(result1)).rjust(self.widthc-1), 1)
                else:
                    self._prt_utf((var + " = " +
                                str(eval(var))).rjust(self.widthc-1), 1)
            else:
                if len(cunit) > 0:
                    tmp1 = str(eval(var).asUnit(eval(cunit)))
                else:
                    tmp1 = str(eval(var))
                self._prt_utf((var + " = " +
                                tmp1).rjust(self.widthc-1), 1)

            tmp = int(self.widthc-1) * '-'
            self._prt_utf((tmp + u'\u2518').rjust(self.widthc), 1)
            self._prt_utf(" ", 0)
            return

        # symbolic and substituted forms
        else:
            # print reference line
            tmp = int(self.widthc-1) * '-'
            self._prt_utf((tmp + u'\u2510').rjust(self.widthc), 1)

            strend = dval[3].strip()
            self._prt_utf((var3 + " | " +
                            strend).rjust(self.widthc), 0)
            self._prt_utf(" ", 1)


            # print symbolic form
            for _j in self.symb:
                if str(_j)[0] != '_':
                    varsym(str(_j))
            try:
                symeq = sympify(dval[2].strip())
                self._prt_utf(symeq, 1)
                self._prt_utf(" ", 0)
                self._prt_utf(" ", 0)
            except:
                pass

            # substitute values
            # evaluate all terms and equations
            if dval[6].strip() == '3':
                for _k in self.odict:
                    if _k[0] != '_':
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

                # clean up unicode
                out3 = out2.replace('*', u'\u22C5')
                cnt = 0
                for _m in out3:
                    if _m == '-':
                        cnt += 1
                        continue
                    else:
                        if cnt > 1:
                            out3 = out3.replace('-'*cnt, u'\u2014'*cnt)
                        cnt = 0

                # print substituted form
                self._prt_utf(out3, 1)
                self._prt_utf(" ", 0)

            # print result right justified
            if type(eval(var)) != Unum:
                if type(eval(var)) == float or type(eval(var)) == float64:
                    resultform = '{:.' + dval[4].strip()+'f}'
                    result1 = resultform.format(float(eval(var)))
                    self._prt_utf((var + " = " +
                                str(result1)).rjust(self.widthc-1), 1)
                else:
                    self._prt_utf((var + " = " +
                                str(eval(var))).rjust(self.widthc-1), 1)
            else:
                if len(cunit) > 0:
                    tmp = str(eval(var).asUnit(eval(cunit)))
                else:
                    tmp = str(eval(var))
                self._prt_utf((var + " = " +
                               tmp).rjust(self.widthc), 1)
            tmp = int(self.widthc-1) * '-'
            self._prt_utf((tmp + u'\u2518').rjust(self.widthc), 1)
            self._prt_utf(" ", 0)

    def _prt_sect(self, dval):
        """print [s]

        Dictionary:
        section: ['[s]', sleft, state, file]

        """
        sleft = dval[1]
        self._prt_utf('='*self.widthc, 0)
        self._prt_utf(sleft + dval[3].rjust(self.widthc -
                                                 len(sleft)), 1)
        self._prt_utf('='*self.widthc, 0)
        note = [i.strip() for i in dval[2]]
        if len(note) > 10:
            note = note[:10]
        note = [' '*4 + _i for _i in note]
        notes = '\n'.join(note)
        if len(notes) > 0:
            self._prt_utf(notes + '\n', 0)

    def _prt_blnk(self):
        """insert blank line"""

        self._prt_utf(' ', 0)

    def _prt_txt(self, txt):
        """print pass-through text"""

        self._prt_utf(txt[1].rstrip(), 0)

    def _prt_py(self):
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

    def _prt_summary(self):
        """write model file summary to stdout

        equations:[[e], statement, expr, ref, decimals, units, opt]
        arrays:   [[a], statements, ref, decimals, unit1, unit2]
        sections: [[s], left string, notes]

        """
        sumfile1 = open(self.sumfile, 'w')

        for i in self.odict:
            mtype = self.odict[i][0]
            if mtype == '[e]':
                sumfile1.write(self.odict[i][3].strip()+'\n')
            elif mtype == '[a]':
                sumfile1.write(self.odict[i][2].strip()+'\n')
            elif mtype == '[s]':
                sumfile1.write(self.odict[i][1].strip()+'\n')
                for j in self.odict[i][2]:
                    sumfile1.write(j.strip()+'\n')

        sumfile1.close()
