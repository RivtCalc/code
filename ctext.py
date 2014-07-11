from __future__ import division
from __future__ import print_function
import codecs
import sys
import os
import tabulate
import time
from oncepy import ccheck
from oncepy import oconfig as cfg
from numpy import *
from sympy import *
from sympy import var as varsym

mpathctext = os.getcwd()
try:
    from unitc import *
    cfg.unitfile = 'model folder'
except ImportError:
    try:
        os.chdir(os.pardir)
        from unitc import *
        cfg.unitfile = 'project folder'
        os.chdir(mpathctext)
    except ImportError:
        from oncepy.unitc import *
        cfg.unitfile = 'built-in'
os.chdir(mpathctext)


class CalcText(object):
    """Return UTF-8 calcs

        """
    def __init__(self, odict, calcf, pyf, sumf):
        """Return UTF_8 calcs

        Arguments:
        calcf (str): UTF-8 calc file name
        pyf   (str): Python model name
        sumf  (str): calc summary for database

        Keys for equations and terms are the dependent
        variable. Keys for other operations are generated by a
        line counter.

        For non-equation entries the dictionary key is:
        _x + incremented number - pass-through text
        _o + incremented number - symbolic representation
        _s + incremented number - sections
        _i + incremented number - inserted text
        _y + incremented number - python code
        _c + incremented number - check operation
        _a + incremented number - array and ranges
        _m + incremented number - current model directory
        _d + incremented number - disk operation
        _f + incremented number - function
        _r + incremented number - external data files and content

        the dictionary structure is:
        single line inputs:
        disk:     [[d], filename, parameter, var]
        symbolic: [[o], expr]
        terms:    [[t], statement, expr, ref ]

        multiline inputs
        check:    [[c], check expr, limits, ref, ok]
        arrays:   [[a], state1, expr, range1, range2, ref, dec, u1, u2]
        function: [[f], function name, file name]
        equations:[[e], statement, expr, ref, decimals, units, prnt opt]
        sections: [[s], left string, notes]


        """

        self.ew = ccheck.ModCheck()

        self.odict = odict
        self.pyfile = pyf
        self.sumfile = sumf
        self.fignum = 0

        self.widthc = 90
        self.xtraline = False

        # get list of equation symbols
        self.symb = self.odict.keys()
        self.cfile = codecs.open(calcf, 'w', encoding='utf8')

        # print date at top of calc
        self._prt_utf(time.strftime("%c"), 0)

        for _i in self.odict:
            mtag = self.odict[_i][0]
            #print(mtag, _i, self.odict[_i])
            if mtag ==   '[d]':
                self._prt_disk(self.odict[_i])
                self.xtraline = False
            elif mtag == '[o]':
                self._prt_olic(self.odict[_i])
                self.xtraline = False
            elif mtag == '[t]':
                self._prt_term(self.odict[_i])
                self.xtraline = True
            elif mtag == '[c]':
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
            elif mtag == '[x]':
                self._prt_txt(self.odict[_i])
                self.xtraline = True
            # [r] is a virtual tag
            elif mtag == '[r]':
                self._prt_read(self.odict[_i])
                self.xtraline = False
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

    def _prt_read(self, dval):
        """read csv data file

        Args: str
            dval[0] - operation
            dval[1] - data file
            dval[2] - option
            dval[3] - var
            dval[4] - sep
            dval[5] - skip line
            dval[6] - model file
        """

        # print reference line
        tmp = int(self.widthc-1) * '-'
        self._prt_utf((tmp + u'\u2510').rjust(self.widthc), 0)

        #print('dval', dval)
        strend = str(dval[3]) + " | read data " + dval[6]
        self._prt_utf(strend.rjust(self.widthc - 1), 0)
        self._prt_utf(" ", 1)

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
        self._prt_utf("file: " + dval[1].strip(), 0)
        self._prt_utf(' ', 0)
        self._prt_utf(str(var4[:4]) + ' ... ' + str(var4[-4:]), 1)
        self._prt_utf(' ', 0)

        tmp = int(self.widthc-1) * '-'
        self._prt_utf((tmp + u'\u2518').rjust(self.widthc), 0)
        self._prt_utf(" ", 0)

        #print('mdict', self.mdict[str(var1)])
    def _prt_disk(self, dval):
        """execute and print disk operations

        Dictionary Value:
        equation:[[d], file path, parameter, var1, var2, var3]

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

        _prt_log = self.ew.ewrite2

        fpath = dval[1].strip()
        fp = os.path.abspath(fpath)
        option = dval[2].strip()
        var1 = dval[3].strip()
        var2 = dval[4].strip()
        var3 = dval[5]  # variable with edit lines

        # relative path specified for the following options
        if option == 's':
            # execute script in model namespace
            f1 = open(fp, 'r')
            fr = f1.read()
            f1.close()
            exec(fr, globals())
            link1 = "< execute python script: " + str(fp) + " >"
            _prt_log(link1)
            _prt_log("file: " + fpath + " compiled")

        elif option == 't':
            # this option is handled in cdict.ModDict._tag_d
            # the input is converted to text tags [x]
            pass

        elif option == 'o':
            # execute command
            os.system(fpath)
            link1 = "< execute command: " + str(fp) + " >"
            _prt_log(link1)
            _prt_log('')

        elif option == 'w':
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
            _prt_log(link1)

        elif option == 'w+':
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
            _prt_log(link1)

        elif option == 'f':
            # insert figure in utf-8 document
            self.fignum += 1
            link1 = "< insert figure " + str(self.fignum) + '. ' \
                    + " file: " + str(fpath) + '>'
            _prt_log(link1)
            link2 = "Figure " + str(self.fignum) + '. ' + var1 \
                    + " <file: " + str(fpath) + " >"
            self._prt_utf(link2, 1)
            self._prt_utf(" ", 0)

        elif option == 'i':
            # this option is handled in cdict.ModDicts.__init__
            pass

        # absolute path specified for the following options
        elif option == 'r':
            # handled by _prt_read method
            pass

        elif option == 'e':
            f1 = open(fpath, 'r')
            oldfile = f1.readlines()
            f1.close()
            editlist = []
            for item in var3:
                editlist.append(item)
            # edit file
            for lines in editlist[:-1]:
                #print(lines)
                mod1 = lines.split('|')
                newla = mod1[1]
                newl1 = mod1[1].split(' ')
                for terms in newl1:
                    newl2 = terms.split(' ')
                    for keys in self.odict:
                        mtag = self.odict[keys][0]
                        if mtag == '[t]':
                            for term in newl2:
                                if keys == term[1:].strip():
                                    newla = newla.replace('%'+str(keys),
                                    str(eval(self.odict[keys][2])))
                oldfile[int(mod1[0])-1] = newla+"\n"

            # write edited file
            if var1 != '':
                newfile1 = os.path.basename(fpath)
                newfile1 = newfile1.split('.')
                newfile2 = '.'.join([str(newfile1[0]) +
                                var1.strip(), newfile1[1]])
                newfile = os.path.join(os.path.dirname(fpath),
                                       newfile2)
            else:
                newfile = fpath

            f = open(newfile, 'w')
            writefile = ''.join(oldfile)
            f.write(writefile)
            f.close()

            tmp = int(self.widthc-1) * '-'
            self._prt_utf((tmp + u'\u2510').rjust(self.widthc), 0)

            strend = "edit file " + dval[6].strip()
            self._prt_utf(strend.rjust(self.widthc - 1), 0)
            self._prt_utf(" ", 0)

            # evaluate function
            self._prt_utf("file: " + dval[1].strip(), 0)
            title1 = '[line #]'.center(8) + \
                     '[replacement line]'.rjust(25)
            self._prt_utf(title1, 0)
            for _i in editlist[:-1]:
                _j = _i.split('|')
                self._prt_utf(('  ' + _j[0].strip()).ljust(10)
                              + (_j[1].strip()), 1)
            self._prt_utf(' ', 0)

            tmp = int(self.widthc-1) * '-'
            self._prt_utf((tmp + u'\u2518').rjust(self.widthc), 0)
            self._prt_utf(" ", 0)

            link1 = "< edit file: " + str(fpath) + " >"
            _prt_log(link1)
        else:
            pass

    def _prt_olic(self, dval):
        """print symbolic expression

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
        """print terms

        Dictionary:
        terms: [[t], statement, expr, ref ]

        """
        shift = int(self.widthc / 2.8)
        ref = dval[3].strip().ljust(shift)
        statement = dval[1].strip()
        #ptype = type(eval(dval[2]))
        #if ptype == list or ptype == ndarray or ptype == tuple:
        #    statement = statement.split('=')[0].strip()
        self._prt_utf(" "*4 + ref + " | " + statement,  1)

    def _prt_check(self, dval):
        """print checks

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
            if _k[0:2] == '_a':
                #print('array', self.odict[_k][1].strip())
                exec(self.odict[_k][3].strip())
                exec(self.odict[_k][4].strip())
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

        # symbolic representation
        self._prt_utf(pretty(symeq1), 1)

        # print substituted values in equation
        symat = symeq1.atoms(Symbol)

        #rewrite equation - extend variables to length of value
        for _n in symat:
            #get length of eval(variable)
            evlen = len((eval(_n.__str__())).__str__())
            new_var = str(_n).ljust(evlen, '~')
            symeq1 = symeq1.subs(_n, symbols(new_var))
        # list of new symbols
        symat1 = symeq1.atoms(Symbol)
        out2 = pretty(symeq1, wrap_line=False)

        #substitute values
        for _n in symat1:
            o_var = str(_n).replace('~', '')
            expr1 = eval((self.odict[o_var][1]).split("=")[1])
            if type(expr1) == float:
                form = '{:.' + dval[5].strip()+'f}'
                symvar1 = form.format(eval(str(expr1)))
            else:
                symvar1 = eval(o_var.__str__()).__str__()
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
        self._prt_utf(" ", 0)
        self._prt_utf(out3, 1)
        self._prt_utf(" ", 0)

        # result
        self._prt_utf(out2p.rjust(self.widthc-1), 1)
        tmp = int(self.widthc-1) * '-'
        self._prt_utf((tmp + u'\u2518').rjust(self.widthc), 0)
        self._prt_utf(" ", 0)

    def _prt_array(self, dval):
        """print arrays

        Dictionary:
        arrays: [[a], statement, expr, range1, range2,
                    ref, decimals, unit1, unit2]

        """
        eformat, rformat = dval[6].split(',')
        try:
            exec("set_printoptions(precision=" + eformat.strip() + ")")
            exec("Unum.VALUE_FORMAT = '%." + eformat.strip() + "f'")
        except:
            set_printoptions(precision=3)
            Unum.VALUE_FORMAT = "%.3f"


        # table heading

        tmp = int(self.widthc-1) * '-'
        self._prt_utf((tmp + (u'\u2510')).rjust(self.widthc), 0)
        tright = dval[5].strip().split(' ')
        eqnum = tright[-1].strip()
        tleft = ' '.join(tright[:-1]).strip()
        self._prt_utf((tleft + ' ' + eqnum).rjust(self.widthc), 0)

        varx = dval[1].strip()
        self._prt_utf(' ', 0)
        self._prt_utf('range variables: ' + varx, 0)

        vect = dval[1:]

        # print symbolic form
        # convert variables to symbols
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

            self._prt_utf("equation: ", 1)
            self._prt_utf(" ", 0)
            self._prt_utf(out1, 1)
            self._prt_utf(" ", 0)
        except:
            self._prt_utf('equation: ' + vect[0].strip(), 1)
            self._prt_utf(" ", 0)

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
                exec(self.odict[k1][3].strip())
                exec(self.odict[k1][4].strip())
                exec(self.odict[k1][1].strip())

        # single row vector - 1D table
        if len(str(vect[3])) == 0 and len(str(vect[0])) != 0:
            # process range variable 1
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
                        #print('alist', alist1)
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
                        #print('_x', type(_x), _x)
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
            flt1 = "." + eformat.strip() + "f"
            ptable = table2.tabulate(alist, rlist, 'rst', floatfmt=flt1)
            nstr = pretty(ptable, use_unicode=True, num_columns=92)

            # print table
            self._prt_utf(nstr, 1)
            tmp = int(self.widthc-1) * '-'
            self._prt_utf((tmp + u'\u2518').rjust(self.widthc), 0)

    def _prt_func(self, dval):
        """print functions

        Dictionary:

        Arguments:
        ip: a model line or block

        Dictionary Value:
        function:[[f], function call, var, ref, model number

        """
        # print reference line
        tmp = int(self.widthc-1) * '-'
        self._prt_utf((tmp + u'\u2510').rjust(self.widthc-1), 0)

        funcname = dval[1].split('(')[0]

        strend = funcname + ' | function ' + dval[4].strip()
        self._prt_utf(strend.rjust(self.widthc - 1), 0)

        # evaluate function
        self._prt_utf(" ", 0)
        self._prt_utf('function description: '
                      + dval[3].strip(), 0)
        self._prt_utf(" ", 0)
        self._prt_utf('function value assigned to variable: '
                      + dval[2].strip(), 0)
        self._prt_utf(" ", 1)
        self._prt_utf('function call: ' + dval[1].strip(), 0)
        docs1 = eval(funcname + '.__doc__')
        self._prt_utf(' ', 0)
        self._prt_utf('function doc:', 0)
        self._prt_utf(docs1, 0)
        return1 = eval(dval[1].strip())
        self._prt_utf(' ', 0)
        if return1 is None:
            self._prt_utf('function evaluates to None'.rjust(
                self.widthc-1), 1)
        else:
            self._prt_utf(('function return: ' + return1).rjust(
                self.widthc-1), 1)

        tmp = int(self.widthc-1) * '-'
        self._prt_utf((tmp + u'\u2518').rjust(self.widthc), 0)
        self._prt_utf(" ", 0)

    def _prt_eq(self, var3, dval):
        """print equations

        Dictionary:
        equations:[[e], statement, expr, ref, decimals, units, prnt opt]

        """

        eformat, rformat = dval[4].split(',')

        try:
            exec("set_printoptions(precision=" + eformat + ")")
            exec("Unum.VALUE_FORMAT = '%." + eformat + "f'")
        except:
            set_printoptions(precision=3)
            Unum.VALUE_FORMAT = "%.3f"

        cunit = dval[5].strip()
        var = dval[1].split("=")[0].strip()

        # evaluate variables - strip units for arrays
        for k1 in self.odict:
            #print('ek1', k1)
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
                        #print('ej1', k1)
                    except:
                        pass
            if k1[0:2] == '_a':
                #print('ek1-2', k1)
                exec(self.odict[k1][3].strip())
                exec(self.odict[k1][4].strip())
                exec(self.odict[k1][1].strip())
        # restore units
        for j2 in self.odict:
            try:
                state = self.odict[j2][1].strip()
                varx = state.split('=')
                state2 = varx[0].strip() + '=' + varx[0].strip()
                exec(state2)
            except:
                pass

        # evaluate only
        if dval[6].strip() == '0':
            exec(dval[1])
            return
        # result only
        elif dval[6].strip() == '1':

            # restore units
            for j2 in self.odict:
                try:
                    state = self.odict[j2][1].strip()
                    exec(state)
                except:
                    pass

            tmp = int(self.widthc-1) * '-'
            self._prt_utf((tmp + u'\u2510').rjust(self.widthc), 1)
            strend = dval[3].strip()
            self._prt_utf((var3 + " | " + strend).rjust(self.widthc), 0)
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
            self._prt_utf(" ", 0)

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

                # restore units
                for j2 in self.odict:
                    try:
                        state = self.odict[j2][1].strip()
                        exec(state)
                    except:
                        pass

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
                        form = '{:.' + eformat +'f}'
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
            # restore units
            for j2 in self.odict:
                try:
                    state = self.odict[j2][1].strip()
                    exec(state)
                except:
                    pass
            if type(eval(var)) != Unum:
                if type(eval(var)) == float or type(eval(var)) == float64:
                    resultform = '{:.' + eformat +'f}'
                    result1 = resultform.format(float(eval(var)))
                    self._prt_utf((var + " = " +
                                str(result1)).rjust(self.widthc-1), 1)
                else:
                    self._prt_utf((var + " = " +
                                str(eval(var))).rjust(self.widthc-1), 1)
            else:
                exec("Unum.VALUE_FORMAT = '%." + rformat.strip() + "f'")
                if len(cunit) > 0:
                    tmp = str(eval(var).asUnit(eval(cunit)))
                else:
                    tmp = str(eval(var))
                self._prt_utf((var + " = " +
                               tmp).rjust(self.widthc-1), 1)
            tmp = int(self.widthc-1) * '-'
            self._prt_utf((tmp + u'\u2518').rjust(self.widthc), 1)
            self._prt_utf(" ", 0)

    def _prt_sect(self, dval):
        """print sections

        Dictionary:
        section: ['[s]', sleft, state, file]

        """
        sleft = dval[1]
        self._prt_utf('='*self.widthc, 0)
        self._prt_utf(sleft + dval[3].rjust(self.widthc -
                                                 len(sleft)-1), 1)
        self._prt_utf('='*self.widthc, 0)
        note = [i.strip() for i in dval[2]]
        if len(note) > 10:
            note = note[:10]
        if len(note) > 0:
            #print(note)
            note1 = [_i[2:] if _i[0:2] == '| ' else _i for _i in note[:-1]]
            note2 = [' '*4 + _i for _i in note1]
            notes = '\n'.join(note2)
            self._prt_utf(notes + '\n'*2, 0)

    def _prt_blnk(self):
        """insert blank line"""
        self._prt_utf(' ', 0)

    def _prt_txt(self, txt):
        """print pass-through text"""
        # reST modification
        #print('txt', txt)
        if txt[1][1] == '|':
            txt1 = txt[1][1:].rstrip()
        else:
            txt1 = txt[1].rstrip()
        self._prt_utf(txt1, 1)

    def _prt_py(self):
        """write python code to file from dictionary"""
        pyfile1 = open(self.pyfile, 'w')
        #write import commands
        importstr = str("\n".join(["from __future__ import division",
                        "from __future__ import print_function",
                        "import sys",
                        "import oncepy",
                        "from numpy import *",
                        "from collections import OrderedDict",
                        "try:",
                        "   from unum import Unum",
                        "except:",
                        " print('unum module not found')",
                        "sys.path.append('{}')",
                        "try:",
                        "   from unitc import *",
                        "   print('unitc imported from directory')",
                        "except: ",
                        "    try:",
                        "        from oncepy.unitc import *",
                        "        print('unitc import from oncepy')",
                        "    except:",
                        "       print ' '",
                        "       print 'unitc not found' ",
                        "       pass"]).format(cfg.mpath))

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
                try:
                    pdict[str(_k).strip()] = [self.odict[_k][1].strip(),
                                        self.odict[_k][2].strip()]
                except:
                    pass
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
