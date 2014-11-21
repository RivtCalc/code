from __future__ import division
from __future__ import print_function
from collections import OrderedDict
import os
import glob
from numpy import *
from oncepy import ccheck
import oncepy.oconfig as cfg


class ModDicts(object):
    """Return an ordered dictionary of model operations.
    ::

     methods:
        build_dicts()   # combine models for single dictionary
        _build_mdict()  # model operations dictionary
        _build_fdict()  # equation format dictionary
        _build_fidict() # file operation dictionary

    """
    def __init__(self):
        """Assemble dictionaries from models and comodels

            curmod : [[mod number],[model list of lines]]
        """
        self.ew = ccheck.ModCheck()

        self.midx = 0
        self.mdict = OrderedDict()
        self.fidict = OrderedDict()
        self.fdict = {}
        self.mstrx = []
        self.mstr = []

        # model path
        self.mfile = cfg.mfile
        self.mpath = cfg.mpath

        self.mpathfile = os.path.join(self.mpath, self.mfile)
        with open(self.mpathfile, 'r') as mofile:
            self.mmod = mofile.readlines()

        # model operation tags
        taglist = ['#- ', '[i]', '[s]', '[y]', '[t]',
                   '[c]', '[a]', '[f]', '[e]', '[~]']
        self.mtags = taglist

        self.pdstrng1 = ("# This file contains a on-c-e public "
                        "domain template (the template).")

        # initialize section and equation labels
        self.cnt = 0
        self.snum = self.snumchk = self.enum = 0
        self.dec1 = 2

        try:
            self.mnum = (self.mfile.split('.')[0])
            self.modelnum = str(self.mnum)
        except:
            self.modelnum = '0001'

        # read format defaults from main model file
        self.widthc = 90
        for _i in self.mmod:
            mtag = _i[0:11]
            if mtag == "#- formateq":
                ilist = _i[3:].split('|')
                dec1 = ilist[1].strip()
                self.defaultdec = dec1

    def build_dicts(self):
        """ build fdict, fidict and mdict
        ::

         fdict: equation and array format dictionary
         fidict: file operation dictionary
         mdict: model dictionary

        """
        # construct list of model and comodel lines
        mflag1 = 1
        mainmod1 = []
        copath = ''
        comod = ''
        # find comodels
        for lines in self.mmod:
            #print(lines)
            if len(lines.strip()) > 3:
                if lines.split()[0] == '#-' and lines.count('|') == 0:
                    fino = lines.split()[1]
                    for ln2 in self.mmod:
                        try:
                            if ln2.split()[1] == fino and \
                                        ln2.split('|')[1].strip() == 'i':
                                os.chdir(os.pardir)
                                cofile1 = ln2.split('|')[2].strip()
                                dirpat = cofile1[0:2] + '*'
                                dirpat1 = glob.glob(dirpat)
                                copath = os.path.abspath(dirpat1[0])
                                copath2 = os.path.join(copath, cofile1)
                                print('copath', copath2)
                                with open(copath2, 'r') as f1:
                                    comod = f1.readlines()
                                print('done')
                        except:
                            continue
                # write model segments to dicts
                    os.chdir(self.mpath)
                    if len(comod) > 0:
                        if len(mainmod1) > 0:
                            # build main model dict
                            curmod = [self.mpathfile, mainmod1]
                            self.modelnum = os.path.basename(self.mpathfile).split('.')[0]
                            self._build_fdict(curmod)  # format dictionary
                            self.ew.errwrite("< format dict appended - model >"
                            + self.modelnum, 1)
                            self._build_mdict(curmod)  # model dictionary
                            self.ew.errwrite("< model dict appended - model >"
                                             + self.modelnum, 1)
                            mainmod1 = []

                            # comodel dict
                            mflag1 += 1
                            curmod = [copath2, comod]
                            self.modelnum = os.path.basename(copath2).split('.')[0]
                            self._build_fdict(curmod)  # format dictionary
                            self.ew.errwrite("< format dict appended - comodel >"
                                             + self.modelnum, 1)
                            self._build_fidict(curmod)  # file dictionary
                            self.ew.errwrite("< file dict appended - comodel >"
                                             + self.modelnum, 1)
                            self._build_mdict(curmod)  # model dictionary
                            self.ew.errwrite("< model dict appended - comodel >"
                                                 + self.modelnum, 1)
                            comod = ''
                            continue
            mainmod1.append(lines)

        # write remaining main model segments
        os.chdir(self.mpath)
        curmod = [self.mpathfile, mainmod1]
        self.modelnum = os.path.basename(self.mpathfile).split('.')[0]
        self._build_fdict(curmod)  # format dictionary
        self.ew.errwrite("< format dictionary completed >"
             + self.modelnum, 1)
        self._build_fidict(curmod)  # file dictionary
        self.ew.errwrite("< file dictionary completed >"
             + self.modelnum, 1)
        self._build_mdict(curmod)  # model dictionary
        self.ew.errwrite("< model dictionary completed >"
             + self.modelnum, 1)
        self.ew.errwrite("< model dictionaries completed - no. models = " +
                    str(mflag1) + " >\n", 1)

    def get_mdict(self):
        """return model dictionary

        """
        return self.mdict

    def get_fdict(self):
        """return equation and array format dictionary

        """
        return self.fdict

    def get_fidict(self):
        """return file operation dictionary

        """
        return self.fidict

    def _build_fdict(self, curmod):
        """Build format dictionary from '#- formateq' op tag.
        ::

         Append if more than one model

         arguments:
            curmod (string): current model

         dictionary:
            fdict[refnumber] : [decimals, units, units]

        """
        with open(curmod[0]) as cm:
            cmtxt = cm.readlines()
        pend1 = False
        for i in cmtxt:
            mtag = i[0:11]
            if mtag == "#- formateq":
                pend1 = True
                tg, fmt, caltyp = i.split('|')
                self.fdict['default'] = [fmt.strip(), caltyp.strip(), '']
                continue
            if pend1:
                if len(i.strip()) == 0:
                    break
                else:
                    fnum, dec2, unt, lbl = i[2:].split('|')
                    fnum = str(self.modelnum) + fnum.strip()
                    self.fdict[fnum] = [dec2.strip(), unt.strip(), lbl.strip()]

    def _build_fidict(self, curmod):
        """Build file dictionary from '#- fileop' op tag.
        ::

         Append if more than one model.

         arguments:
            curmod (string): current model

         dictionary:
            fidict[refnumber] : [option, file, var1, var2, var3]

        """
        # set reference values
        with open(curmod[0]) as cm:
            cmtxt = cm.readlines()
        # set reference values
        pend1 = False
        pend2 = False
        editlist = []
        for i in cmtxt:
            if i[:9] == "#- fileop":
                pend1 = True
                continue

            if pend2:
                if i[:3].strip() == '#--':
                        pend2 = False
                        self.fidict[fnum1] = [opt.strip(),file1.strip(),
                        var1.strip(), var2.strip(), editlist]
                        editlist = ''
                        continue

                if i[:2].strip() == '#-':
                    #print('edit', i)
                    edline1, edit1 = i[2:].strip().split('|')
                    editlist.append([edline1, edit1])
                    continue

            if pend1:
                if len(i.strip()) == 0:
                    break
                if i[:2].strip() == '#-' and pend1:
                    try:
                        opt1 = i[2:].split('|')[1]
                    except:
                        opt1 = ' '

                    if opt1.strip() == 'e':
                        pend2 = True
                        editlist =[]
                        fnum, opt, file1, var1, var2, var3 = i[2:].strip().split('|')
                        fnum1 = str(self.modelnum) + fnum.strip()
                        continue

                    if not pend2:
                        fnum, opt, file1, var1, var2, var3 = i[2:].strip().split('|')
                        fnum1 = str(self.modelnum) + fnum.strip()
                        self.fidict[fnum1] = [opt.strip(),file1.strip(),
                        var1.strip(), var2.strip(), editlist]
                        #print('fidict', fnum1, self.fidict[fnum1])

    def _build_mdict(self, curmod):
        """Build model dictionary.
        ::

         Keys for equations and terms are the dependent
         variable. Unique keys for other operations are generated by a
         line counter.

         For non-equation entries the dictionary key is:
            _i + incremented number - file operation
            _s + incremented number - sections
            _y + incremented number - symbolic representation
            _t + incremented number - inserted text
            _c + incremented number - check operation
            _a + incremented number - array and ranges
            _f + incremented number - function
            _x + incremented number - pass-through text
            _m + incremented number - current model directory
            _pd - license text

         Dictionary structure for each operation. An op is added with a method.

         single line inputs:
            file:     [[i], refnum, description, mod number]
            sections: [[s], left string, mod number]
            symbolic: [[y], expr]
            terms:    [[t], statement, expr, ref, mod number ]

         multiline inputs
            check:    [[c], check expr, limits, ref, ok]
            arrays:   [[a], state1, expr, range1, range2, ref, dec, u1, u2]
            function: [[f], function call, var, ref, eq num]
            equations:[[e], statement, expr, ref, decimals, units, prnt opt]

        """
        # current model content
        self.mstrx = curmod[1]
        #print(curmod[0])

        # build ordered dictionary mdict of models
        ip = ''  # accumulator for multiline operations
        pend = ' '

        # write model dictionary
        self.midx += 1
        mkey = '_m'+str(self.midx)
        self.mdict[mkey] = ['[m]', self.modelnum]
        #print(mkey, self.modelnum)

        for i1 in self.mstrx:
            self.cnt += 1
            # add public domain license to dictionary
            if str(i1.strip()) == ("# This file contains a on-c-e public "
                                    "domain template (the template)."):
                self._tag_pd()
                continue

            # skip comment lines
            try:
                if i1.strip()[0:2] == '# ':
                    continue
            except:
                pass

            #print('i', i1.strip())
            if len(i1.strip()) == 0:
                mtag = '[~]'  # blank line
            else:
                if i1.lstrip()[:3] in self.mtags:
                    i1 = i1.lstrip()
                    mtag = i1[:3]
                else:
                    mtag = '[x]'
            #print('tag ', mtag)

            # add public domain license to dictionary
            if str(i1.strip()) == self.pdstrng1:
                self._tag_pd()

            # accumulate multiline blocks
            pendlist = [ 'y', 'c', 'a', 'f', 'e']
            if pend in pendlist and mtag != '[~]':
                ip += i1
                continue
            # end block
            if pend in pendlist and mtag == '[~]':
                if pend ==   'y': self._tag_y(ip)
                elif pend == 'c': self._tag_c(ip)
                elif pend == 'a': self._tag_a(ip)
                elif pend == 'f': self._tag_f(ip)
                elif pend == 'e': self._tag_e(ip)
                else:
                    pass
                ip = ''
                pend = ''
                mkey = '_x' + str(self.cnt)
                self.mdict[mkey] = ['[~]', ' ']
                continue

            # pass-through text
            if mtag == '[x]':
                mkey = '_x'+str(self.cnt)
                self.mdict[mkey] = [mtag, i1]
                continue

            # select tag
            if mtag in self.mtags:
                if mtag ==   '#- ':
                    self._tag_file(i1)
                elif mtag == '[s]':
                    self._tag_s(i1)
                elif mtag == '[y]':
                    ip += i1
                    pend = 'y'
                elif mtag == '[t]':
                    self._tag_t(i1)
                elif mtag == '[c]':
                    ip += i1
                    pend = 'c'
                elif mtag == '[a]':
                    ip += i1
                    pend = 'a'
                elif mtag == '[f]':
                    ip += i1
                    pend = 'f'
                elif mtag == '[e]':
                    ip += i1
                    pend = 'e'
                elif mtag == '[~]':
                    mkey = '_x' + str(self.cnt)
                    self.mdict[mkey] = ['[~]', ' ']
                else:
                    mkey = '_x' + str(self.cnt)
                    self.mdict[mkey] = ['[x]', i1]

        #for i1 in self.mdict: print(self.mdict[i1])

    def _tag_file(self, line):
        """Add [i] file operation number to mdict.
        ::

         Argument:
            line: file line

         Dictionary:
            _i: [[i], fnum, string, mod number]

        """
        if len(line.split('|')) < 2:
            s1 = line.strip()
            fnum = str(self.modelnum) + s1.split()[1]
            mkey = '_i' + str(self.cnt)
            try:
                s2 = int(s1.split()[1].strip())
                s2 = s1.split()[1].strip()
            except:
                return

            self.mdict[mkey] = ['[i]', fnum.strip(), s2,
                                '['+ str(self.modelnum) +']']

    def _tag_s(self, line):
        """Add [s] to mdict.
        ::

         Argument:
            line: section line

         Dictionary:
            _s: [[s], left string, mod number]

        """
        stitle = line[3:].strip()
        self.snum += 1
        sleft = '[' + str(self.snum) + '] ' + stitle
        mkey = '_s' + str(self.cnt)
        self.mdict[mkey] = ['[s]', sleft, '[' + str(self.modelnum) +']']

    def _tag_y(self, line):
        """add [y] symbolic op to mdict

        Argument:
            line: symbolic line

        Dictionary:
            symbolic: [[y], symlang, expr ]

        """

        # reset equation number at new section
        self.enum += 1
        if self.snum > self.snumchk:
            self.enum = 1
            self.snumchk = self.snum
        enumb = ' [' + str(self.snum) + '.' + str(self.enum) + ']'



        mkey = '_y' + str(self.cnt)
        symlang = line[3:].split('|')[0].strip()
        expr = line[3:].split('|')[1].strip()
        self.mdict[mkey] = ['[y]', symlang, expr, enumb]

    def _tag_t(self, line):
        """Add [t] term op to mdict.
        ::

         Argument:
            line: term line

         Dictionary:
            terms: [[t], statement, expr, ref ]

        """
        ivect = line
        ref, state = ivect[3:].split("|")
        var = state.split("=")[0].strip()
        expr = state.split("=")[1].strip()
        self.mdict[var] = ['[t]', state.strip(), expr, ref,
                           '['+ self.modelnum +']']

    def _tag_c(self, block):
        """Add [c] check op to mdict.
        ::

         Argument:
            block: check block of input

         Dictionary:
            check:  [[c], check expr, op, limit, ref, dec, ok]

        """
        ivect = block.split('\n')
        ref, ok, dec = ivect[0].strip()[3:].split('|')
        check, op, limits = ivect[1].strip().split('|')
        self.enum += 1
        if self.snum > self.snumchk:
            self.enum = 1
            self.snumchk = self.snum

        enumb = ' [' + str(self.snum) + '.' + \
                str(self.enum) + ']'
        ref = ref.strip() + enumb
        mkey = '_c'+str(self.cnt)
        self.mdict[mkey] = ['[c]', check, op, limits, ref, dec, ok]

    def _tag_a(self, block):
        """ Add [a] array op to mdict.
        ::

         Arguments:
            block: array block of input

         Dictionary:
            _a : [[a], statement, expr, range1, range2,
            ref, decimals, unit1, unit2, mod number]

        """
        # reset equation number at new section
        self.enum += 1
        if self.snum > self.snumchk:
            self.enum = 1
            self.snumchk = self.snum

        ivect = block.strip().split('\n')

        try:
            ref, fnum = ivect[0][3:].split("#-")
            fnum = str(self.modelnum) + fnum.strip()
        except:
            ref = ivect[0][3:]
            fnum = str(self.modelnum) + '01'

        decs, unts, opt = self.fdict[fnum]

        try:
            decs.split(',')
        except:
            decs = self.fdict['default'][1]
        enumb = ' [' + str(self.snum) + '.' + str(self.enum) + '] '
        ref = '  ' + ref.strip().ljust(self.widthc-len(enumb)-2) + \
              enumb

        # set dictionary values
        rng1 = rng2 = state = expr = ''
        mkey = '_a' + str(self.cnt)
        arrayblock = ivect[1:]
        if len(arrayblock) == 1:
            state = expr = arrayblock[0]

        elif len(arrayblock) == 2:
            rng1 = arrayblock[0]
            state = arrayblock[1]
            expr = state.split("=")[1].strip()

        elif len(arrayblock) == 3:
            rng1 = arrayblock[0]
            rng2 = arrayblock[1]
            state = arrayblock[2]
            expr = state.split("=")[1].strip()

        self.mdict[mkey] = ['[a]', state, expr, rng1, rng2, ref,
                            decs, unts, opt, '[' + self.modelnum + ']']
        #print(state)

    def _tag_f(self, block):
        """Add [f] function op to mdict.
        ::

         Arguments:
            block: function lines

         Dictionary Value:
            _f :[[f], function call, var, ref, eq num]

        """
        self.enum += 1
        if self.snum > self.snumchk:
            self.enum = 1
            self.snumchk = self.snum
        enumb = ' [' + str(self.snum) + '.' + str(self.enum) + ']'

        ivect = block.split('\n')
        fname = ivect[1].split('|')[0]
        var2 = ivect[1].split('|')[1].strip()
        ref = ivect[0].strip()

        # set dictionary values
        mkey = '_f' + str(self.cnt)
        self.mdict[mkey] = ['[f]', fname, var2, ref, enumb]

    def _tag_e(self, block):
        """Add [e] equation op to mdict.
        ::

         Arguments:
            block: equation lines

         Dictionary key : value:
            _e : [[e], statement, expr, ref, decimals, units, prnt opt, mod number]

        """
        # reset equation number at new section
        self.enum += 1
        if self.snum > self.snumchk:
            self.enum = 1
            self.snumchk = self.snum
        line1 = block.split('\n')
        #print(line1)
        try:
            ref, fnum = line1[0][3:].split("#-")
            fnum = str(self.modelnum) + fnum.strip()
        except:
            ref = line1[0][3:]
            fnum = str(self.modelnum) + '01'

        decs, unts, opt = self.fdict[fnum]

        try:
            decs.split(',')
        except:
            unts = self.fdict['default'][1]
        enumb = ' [' + str(self.snum) + '.' + str(self.enum) + ']'
        ref = ref.strip() + enumb

        # set dictionary values
        state = ''
        for j in line1[1:]:
            state = state + j.strip()
        expr = state.split("=")[1].strip()
        var1 = state.split("=")[0].strip()
        self.mdict[var1] = ['[e]', state, expr, ref, decs, unts, opt,
                            '['+ self.modelnum +']']

    def _tag_pd(self):
        """add public domain license to dict

        """
        mkey = '_pd'
        self.mdict[mkey] = \
"""____________________________________________________________________________

This document (the calc) is generated from a on-c-e public domain template.
The template is licensed under the CCO 1.0 Public Domain Dedication
at http://creativecommons.org/publicdomain/zero/1.0/
Neither the template or calc represent structural designs and
the user is solely responsible for inputs and results.
"""
