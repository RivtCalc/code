from __future__ import print_function
from __future__ import division
import os
import sys
import time
import tabulate
import oncepy
import oncepy.oconfig as oCfg
from oncepy import ccheck
from oncepy import cdict
from oncepy import ctext
from oncepy import crst
from oncepy import cpdf
from numpy import *

mpathcstart = os.getcwd()
try:
    from unitc import *
    oCfg.unitfile = 'model folder'
except ImportError:
    try:
        os.chdir(os.pardir)
        from unitc import *
        oCfg.unitfile = 'project folder'
    except ImportError:
        from oncepy.unitc import *
        oCfg.unitfile = 'built-in'
os.chdir(mpathcstart)

__version__ = '0.4.6'

class ModStart(object):
    """initialize file names and write tabular input summaries
    ::

     Methods:
        gen_filenames(): read files and generate new file names
        file_summary(): write summary of calculation results to stdout
        var_table(mdict1): generate variable table
        out_term(): write processing log to terminal

    """
    def __init__(self):
        """initialize file names
        ::

         File names are stored in oconfig.py in the once package directory

        """
        # initialize file names
        self.stylepath = '-'
        self.calcf = ''
        self.pdff = ''
        self.pyf = ''
        self.sumf = ''
        self.ew = ccheck.ModCheck()


    def gen_filenames(self):
        """generate new file names
        ::

         From a model file name 'model.txt' the generated files are:
            calmodel.txt
            calmodel.pdf
            summodel.txt
            _onceeq.py

        """
        calcf1 = oCfg.mfile.split('.')
        self.pdff = '.'.join(['cal' + calcf1[0], calcf1[1], 'pdf'])
        self.calcf = '.'.join(['cal' + calcf1[0], calcf1[1], calcf1[2]])
        self.sumf = '.'.join(['sum' + calcf1[0], calcf1[1], calcf1[2]])
        self.pyf = '_onceeq.py'

        #start calc file early to avoid Komodo dialog response
        f1 = open(self.calcf,'w')
        f1.write(time.strftime("%c") + "     onceutf version: " + __version__)
        f1.close()

        return self.calcf, self.pyf, self.sumf

    def file_summary(self):
        """file name summary table
        ::

         The following variable parameters are summarized prior to processing:
            variable name
            variable operation tag and value
            units
            model number

        """
        csumm1 = ("""
    File Summary
    ============

    Files and paths
    ---------------
    model input        :  {}
    calc output        :  {}
    py output file     :  {}
    summary file       :  {}
    units path         :  {}
    model path         :  {}
    project path       :  {}
    project file       :  {}
    style path         :  {}
    calc type (margin) :  {}
        """.format(oCfg.mfile, self.calcf, self.pyf, self.sumf,
                   oCfg.unitfile, oCfg.mpath,
                   oCfg.ppath, oCfg.pfile, oCfg.stylefile, oCfg.caltype))

        self.ew.errwrite(csumm1, 1)

    def var_table(self, mdict1):
        """summarize terms, equations, arrays and functions
        ::

         Dictionary:
            terms [var]     : [[t], statement, expr, ref ]
            arrays[var]     : [[a], statement, expr, range1, range2,
                            ref, decimals, unit1, unit2]
            functions [var] : [[f], function name, ref]
            equations [var] : [[e], state, expr, ref, decimals, units, prnt opt]

        """
        tab1 = []
        modnum = oCfg.mfile.split('.')[0]

        for m1 in mdict1:
            #print(m1, mdict1[m1] )
            if mdict1[m1][0] == '[m]':
                modnum = mdict1[m1][1]

            if mdict1[m1][0] == '[t]':
                edict1 = mdict1[m1]
                state1 = edict1[1].strip()
                term1 = m1.strip()
                unitx = ''
                val2 = ''
                try:
                    exec(state1)
                    val2 = '[t] ' + str(eval(term1))
                    if type(eval(term1)) == list or type(eval(term1))== ndarray:
                        val2 = '[t] ' + 'list or array'
                except:
                    val2 = "[t] runtime"
                    unitx = '-'
                try:
                    val2 = "[t] " + str(eval(term1).asNumber())
                    unitx = str(eval(term1).strUnit())
                except:
                    pass
                tab1.append(['| ' + str(term1), val2, unitx, modnum])

            elif mdict1[m1][0] == '[a]':
                edict1 = mdict1[m1]
                term1 = mdict1[m1][1].split('=')[0].strip()
                if mdict1[m1][4] == '':
                    val1 = "1D [a]"
                else:
                    val1 = "2D [a]"

                state1 = edict1[1].strip()
                try:
                    exec(state1)
                except:
                    val1 = "[a] runtime"
                unitx = '-'
                tab1.append(['| ' + str(term1), val1, unitx, modnum])

            elif mdict1[m1][0] == '[f]':
                term1 = mdict1[m1][1].strip()
                val1 = "[f] runtime "
                unitx = "-"
                tab1.append(['| '+str(term1.split('(')[0]), val1, unitx, modnum])

            elif mdict1[m1][0] == '[e]':
                edict1 = mdict1[m1]
                term1 = m1.strip()
                val4 = "[e] runtime "
                state1 = edict1[1].strip()
                unitx = '-'
                try:
                    val4 = '[e] ' + str(eval(term1))
                    if type(eval(term1)) == list or type(eval(term1))== ndarray:
                        val4 = '[e] ' + 'list or array'
                except:
                    val4 = "[e] runtime"
                try:
                    unitx = str(mdict1[m1][5])
                except:
                    unitx = '-'
                tab1.append(['| ' + str(term1), val4, unitx, modnum])

            elif mdict1[m1][0] == '[r]':
                term1 = mdict1[m1][3].strip()
                val1 = "[file] runtime"
                unitx = "-"
                tab1.append(['| ' + str(term1), val1, unitx, modnum])
            else:
                pass

        self.ew.errwrite("   Table of Model Variables", 1)
        table1 = tabulate
        self.ew.errwrite(table1.tabulate(tab1,
                headers=[' Variable', 'Type and Value', 'Units', 'Model'],
                tablefmt='rst', floatfmt=".4f"), 1)

    def out_term(self):
        """-e or -b flag echoes calc to console or browser
        ::

         -b switch needed primarily on Window where UTF-8 is missing

        """
        # onceweb modified
        sysargv = oCfg.sysargv
        if len(sysargv) > 2 and '-e' in sysargv:
            print()
            print("==============================  "
                  "echo calc  =============================")
            print()
            try:
                with open(self.calcf, 'r') as mod1:
                    for i in mod1.readlines():
                        print(i)
            except OSError:
                pass
        elif len(sysargv) > 2 and '-b' in sysargv:
            try:
                os.system("start chrome " + self.calcf)
            except OSError:
                try:
                    os.system("start firefox " + self.calcf)
                except OSError:
                    try:
                        os.system("start iexplore file:///%CD%/" +
                                  self.calcf)
                    except OSError:
                        pass

    @staticmethod
    def cmdline(version):
        """command line help
        ::

         Prints help with -h switch or error.

        """
        print()
        print("oncepy  ver:" + version)
        print("Use:")
        print("python -m oncepy ddmm.modfile.txt (options)")
        print("   where dd is the division and mm is the model number")
        print()
        print("options:")
        print("   -h    prints this prompt")
        print("   -c    echoes UTF-8 calc to console (stdout)")
        print("   -b    opens UTF-8 calc in Windows browser")
        print("         tries the following browsers in order:")
        print("             start chrome modfile.m.txt ")
        print("             start firefox modfile.m.txt")
        print("             start iexplore file:///%CD%/modfile.m.txt")
        print("   -noclean  leaves PDF intermediate files on disk")
        print()
        print("set browser encoding to UTF-8; refer to user manual")
        print()
        print("outputs:")
        print("   logddmm.model.txt")
        print()
        print("if no errors then outputs:")
        print("     ddmm.modfile.py     (Python equation file")
        print("     calddmm.modfile.txt (UTF-8 calc")
        print("     sumddmm.modfile.txt (calculation summary)")
        print("if option selected in model or project file:")
        print("     calddmm.modfile.pdf (PDF calc")
        print("     project.pdf (PDF project calc)")

        sys.exit(1)
