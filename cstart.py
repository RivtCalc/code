from __future__ import print_function
from __future__ import division
import os
import sys
import time
import tabulate
import oncepy
import oncepy.oconfig as cfg
from oncepy import ccheck
from oncepy import cdict
from oncepy import ctext
from oncepy import crst
from oncepy import cpdf
from numpy import *

mpathcstart = os.getcwd()
try:
    from unitc import *
    cfg.unitfile = 'model folder'
except ImportError:
    try:
        os.chdir(os.pardir)
        from unitc import *
        cfg.unitfile = 'project folder'
        os.chdir(mpathcstart)
    except ImportError:
        from oncepy.unitc import *
        cfg.unitfile = 'built-in'
os.chdir(mpathcstart)


class ModStart(object):
    """reads a on-c-e model and returns a UTF-8 or PDF calc

    The program **oncepy** takes a **on-c-e** ASCII model as input
    and returns a formatted structural engineering calculation. The
    program formats structural calculations using a simple, natural
    markup language.

    Currently the program can run usable calculation models,
    as illustrated in the User Manual examples. Some classes and
    methods are not implemented yet.

    The program runs on the following operating systems and
    Python scientific platforms::

    workstation (Windows, Linux, OSX: Anaconda, Enthought, Pythonxy)

    Models that do not use projects or PDF calcs run on::

    web (Linux, Wakari, PythonAnywhere)

    mobile - **use onceutf.py** (Android: QPython, iOS: Pythonista)

    Progress can be tracked at Trello: https://on-c-e.info

    Source code and documentation are here: http://on-c-e.github.io/

    Refer to the user manual and programs here: http://on-c-e.org/programs/

    email contact: r holland once.pyproject@gmail.com

    Running the Program
    ===================

    Copy the **oncepy** package (folder) to the python/lib/site-packages
    directory. From a terminal window type:

    .. code:: python

        python -m oncepy ddmm.model.txt (-c or -b)

    where *ddmm.model.txt* is the file name, *ddmm* is the model number,
    *dd* is the division number, and *mm* is the model designation.

    The program will write the calc file calddmm.model.txt and the
    -e or -b options will echo the calc to a shell (-e) or
    a Windows browser (-b). The -b option is needed in the Windows shell because
    the shell lacks needed UTF-8 encoding.

    To open a command shell window in a folder in Windows 7 or 8 ,
    navigate to the folder using Explorer, hold the shift key,right click,
    click on 'open command window here' in the context menu.

    Change the browser encoding settings if needed:
    -----------------------------------------------
    Chrome: type chrome:settings/fonts in url bar -
    scroll to the bottom of the dialog box and make the change

    Firefox: options - content - advanced - UTF-8

    Internet Explorer: right click - encoding - UTF-8

    For further details refer to the user manual:

        http://on-c-e.us/

    A relatively complete UTF-8 font set is needed for proper math
    representation in an IDE.  **DejaVu Mono** fonts are recommended and
    can be downloaded here:

        http://dejavu-fonts.org/wiki/Main_Page

        ModStart methods:
        gen_filenames() read files and generate new file names
        file_summary() write summary of calculation results to stdout
        var_table(mdict1) generate variable table
        out_term() write processing log to terminal
        """

    def __init__(self):
        """generate file names and table of variables

        file names are stored in oconfig.py in the once package directory

        """
        # initialize file names
        self.stylepath = '-'
        self.calcf = ''
        self.pdff = ''
        self.pyf = ''
        self.sumf = ''
        self.ew = ccheck.ModCheck()

        # path to pdf style file
        if cfg.stylefile == 'project folder':
            os.chdir(os.pardir)
            self.stylepath = os.getcwd()
            os.chdir(cfg.mpath)
        elif cfg.stylefile == 'model folder':
            self.stylepath = os.getcwd()
        else:
            self.stylepath = oncepy.__path__

    def gen_filenames(self):
        """generate new file names"""

        calcf1 = cfg.mfile.split('.')
        self.pdff = '.'.join(['cal' + calcf1[0], calcf1[1], 'pdf'])
        self.calcf = '.'.join(['cal' + calcf1[0], calcf1[1], calcf1[2]])
        self.sumf = '.'.join(['sum' + calcf1[0], calcf1[1], calcf1[2]])
        self.pyf = '_onceeq.py'

        #write calc file early to avoid Komodo dialog response
        f1 = open(self.calcf,'w')
        f1.write(time.strftime("%c"))
        f1.close()

        return self.calcf, self.pyf, self.sumf

    def file_summary(self):
        """file summary table
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
        """.format(cfg.mfile, self.calcf, self.pyf, self.sumf,
                   cfg.unitfile, cfg.mpath,
                   cfg.ppath, cfg.pfile, cfg.stylefile, cfg.caltype))

        self.ew.errwrite(csumm1, 1)

    def var_table(self, mdict1):
        """summarize terms, equations, arrays and functions

        Dictionary:

        terms [var]     : [[t], statement, expr, ref ]
        arrays[var]     : [[a], statement, expr, range1, range2,
                            ref, decimals, unit1, unit2]
        functions [var] : [[f], function name, ref]
        equations [var] : [[e], state, expr, ref, decimals, units, prnt opt]

        """

        tab1 = []
        modnum = cfg.mfile.split('.')[0]

        for m1 in mdict1:
            #print(m1, mdict1[m1] )
            if mdict1[m1][0] == '[m]':
                modnum = mdict1[m1][1]

            if mdict1[m1][0] == '[t]':
                edict1 = mdict1[m1]
                state1 = edict1[1].strip()
                term1 = m1.strip()
                unitx = ''
                val11 = ''
                try:
                    exec(state1)
                    val11 = '[t] ' + str(eval(term1))
                    if type(eval(term1)) == list or type(eval(term1))== ndarray:
                        val11 = '[t] ' + 'list or array'
                except:
                    val11 = "[t] runtime"
                    unitx = '-'

                try:
                    val11 = "[t] " + str(eval(term1).asNumber())
                    unitx = str(eval(term1).strUnit())
                except:
                    pass

                tab1.append(['| ' + str(term1), val11, unitx, modnum])

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
                tab1.append(['| ' + str(term1.split('(')[0]),
                             val1, unitx, modnum])

            elif mdict1[m1][0] == '[e]':
                edict1 = mdict1[m1]
                term1 = m1.strip()
                val1 = "[e] runtime "
                state1 = edict1[1].strip()
                unitx = '-'
                try:
                    val14 = '[e] ' + str(eval(term1))
                    if type(eval(term1)) == list or type(eval(term1))== ndarray:
                        val14 = '[e] ' + 'list or array'
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
        """check -e or -b flag and echo calc to console or browser"""
        # onceweb modified
        sysargv = cfg.sysargv
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
        """command line help"""

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
