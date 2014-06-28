from __future__ import print_function
import os
import sys
import tabulate
import oncepy.oconfig as cfg
from oncepy import ccheck
from oncepy import cdict
from oncepy import ctext
from oncepy import crst
from oncepy import cpdf
from oncepy import cproj
from unum import Unum
from numpy import *

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


class ModStart():
    """reads a on-c-e markup file and returns a formatted document

    The program **oncepy** takes a **on-c-e** model as input and
    returns a formatted UTF-8 or PDF calc.

    The beta code and documentation are released to solicit
    participation and feedback on basic concepts.  Currently the
    program can run usable calculation models, as illustrated in the
    examples. Some classes and methods are not implemented yet.
    The current beta development cycle will complete model operations,
    add input error checking, add a unit test framework and
    package the program for pypi distribution.

    Progress can be tracked at Trello:
    https://on-c-e.info

    Source code and documentation are here:

        http://on-c-e.github.io/

    email contact: once.pyproject@gmail.com

    Running the Program
    ===================
    Copy **onceutf_nnn.py** and the model file into the same directory,
    change to the directory and type, from a terminal window:

    .. code:: python

            python -m oncepy model.m.txt (-c or -b)

    The -c or -b options will echo results to a console (-c) or
    a Windows browser (-b). The -b option is needed on Windows
    because of UTF-8 encoding problems in the console.

    Use the lower form if you copy the onceutf file into the
    Python Lib/site-packages directory and rename to onceutf.py.
    The lower form has the advantage of being available to every model
    folder and the Komodo Edit tool buttons.

    To open a terminal window in a folder in Windows 7 or 8 ,
    navigate to the folder using Explorer, hold the shift key,right click,
    click on 'open command window here' in the context menu.

    Change the browser encoding settings if needed:
    -----------------------------------------------
    Chrome  - type chrome:settings/fonts  in url bar -
    scroll to the bottom of the dialog box and make the change

    Firefox - options - content - advanced - UTF-8

    Internet Explorer - right click - encoding - UTF-8

    The program will execute the file and return results in files.

    To obtain a more complete UTF-8 font set install **DejaVu Mono** fonts
    http://dejavu-fonts.org/wiki/Main_Page

    For further details refer to the user manual and programs here:

        **onceutf**
        https://on-c-e.us

        **oncepy**
        http://on-c-e.org/programs/

        **methods**
        gen_paths()  find model and project paths
        _cmdline()  command line prompt
        _gen_files() generate new file names
        _out_term() check console printing flags
        summ_calc() write calculation summary to stdout

        """

    def __init__(self):
        """initialize files and paths

        file arguments are stored in oconfig.py

        """

        # initial file names
        self.pname = '-'
        self.ppath = '-'
        self.stylepath = '-'
        self.calcf = ''
        self.pyf = ''
        self.sumf = ''
        self.packagepath = cfg.packagepath

        if cfg.pfile != '':
            # if the file is a project pass execution to cproj
            pstart = cproj.ProjStart
            pstart.build_pdict()
        else:
            self.mpath = cfg.mpath
            self.mfile = cfg.mfile
            sys.path.append(self.mpath)

        # error and event log
        self.ew = ccheck.ModCheck()
        #self.ew.ewrite1("< todo: write error log code >")

        # generate new file names
        self._gen_files()

        # build dictionaries and write variable list to stdout
        self.model1 = cdict.ModDict(self.mfile, self.mpath)
        self._calc_summ()

        # check model files for errors
        ctext.CalcText(self.model1.mdict, self.calcf, self.pyf,
                                         self.sumf, self.mpath)

        # read calculation type
        self.ew.ewrite2('')
        self.ew.ewrite2('<calculation type> ' + cfg.caltype)
        self.ew.ewrite2('')

        # initialize PDF files
        rstfile = ''
        texfile = ''
        pdffile = ''

        # write rst and PDF calc if options selected
        if cfg.caltype.strip() == 'pdf'or cfg.caltype.strip() == 'PDF':
            rstfile = self.mfile.replace('.txt', '.rst')
            rstout1 = crst.CalcRST(self.model1.mdict,
                                   self.mpath, self.mfile)
            rstout1.prt_rst()
            pdfout1 = cpdf.CalcPdf()
            pdfout1.prt_pdf()


        elif cfg.caltype.strip() == 'rst':
            rstfile = self.mfile.replace('.txt', '.rst')
            rstout1 = crst.CalcRST(self.model1.mdict,
                                   self.mpath, self.mfile)
            rstout1.prt_rst()
            self.ew.ewrite2('')
            self.ew.ewrite2("< rst file written >")
        else:
            pass

        self.ew.ewrite2(( " Files written:\n" +
                " ------------------\n" +
                " model file    :  {}\n" +
                " python file   :  {}\n" +
                " summary file  :  {}\n" +
                " reST file     :  {}\n" +
                " tex file      :  {}\n" +
                " PDF file      :  {}\n").format(self.calcf, self.pyf,
                                                 self.sumf, rstfile,
                                                 texfile, pdffile))

        self.ew.ewrite2("< calculation completed >")

        # UTF-8 calc to console or browser, -c or -b switch
        self._out_term()

    def _gen_files(self):
        """generate new file names"""

        calcf1 = self.mfile.split('.')
        self.calcf = '.'.join([calcf1[0], 'cal' + calcf1[1], calcf1[2]])
        self.sumf = '.'.join([calcf1[0], 'sum' + calcf1[1], calcf1[2]])
        self.pyf = self.mfile.replace('.txt', '.py')

        print("""
    Calculation Summary
    ===================

    Files and paths
    ---------------
    model input    :  {}
    calc output    :  {}
    py output file :  {}
    summary file   :  {}
    units imported :  {}
    model path     :  {}
    project path   :  {}
    project file   :  {}
    style path     :  {}
        """.format(self.mfile, self.calcf, self.pyf, self.sumf,
                   cfg.unitfile, self.mpath,
                   self.ppath, self.pname, self.stylepath))

    def _calc_summ(self):
        """write terms, equations, arrays and functions to stdout

        Dictionary:

        arrays:    [[a], statement, expr, range1, range2,
                    ref, decimals, unit1, unit2]
        functions: [[f], function name, ref]
        equations: [[e], state, expr, ref, decimals, units, prnt opt]
        terms:     [[t], statement, expr, ref ]

        """

        tab1 = []
        for _m in self.model1.mdict:
            #print(_m, self.model1.mdict[_m])
            if self.model1.mdict[_m][0] == '[t]':
                edict1 = self.model1.mdict[_m]
                state1 = edict1[1].strip()
                term1 = _m.strip()
                val4 = ''
                try:
                    exec(state1)
                except:
                    val4 = "[t] runtime"
                try:
                    val2 = eval(term1)
                except:
                    val2 = ''
                try:
                    val1 = str(val2.asNumber())
                except:
                    val1 = str(type(val2)).split("'")[1]

                mfile2 = self.model1.mdict[_m][4]

                if val4 == "[t] runtime":
                    val1 = val4
                try:
                    unitx = str(val2.strUnit())
                except:
                    unitx = '-'

                tab1.append(['| ' + str(term1), val1, unitx, mfile2])

            elif self.model1.mdict[_m][0] == '[e]':
                edict1 = self.model1.mdict[_m]
                term1 = _m.strip()
                state1 = edict1[1].strip()
                mfile2 = self.model1.mdict[_m][7]
                val1 = 'equation'
                state1 = edict1[1].strip()
                try:
                    exec(state1)
                except:
                    val1 = "[e] runtime"

                try:
                    unitx = str(self.model1.mdict[_m][5])
                except:
                    unitx = '-'

                tab1.append(['| ' + str(term1), val1, unitx, mfile2])

            elif self.model1.mdict[_m][0] == '[a]':
                edict1 = self.model1.mdict[_m]
                term1 = self.model1.mdict[_m][1].split('=')[0].strip()
                if self.model1.mdict[_m][4] == '':
                    val1 = "1D array"
                else:
                    val1 = "2D array"

                state1 = edict1[1].strip()
                try:
                    exec(state1)
                except:
                    val1 = "[a] runtime"
                unitx = '-'
                mfile2 = self.model1.mdict[_m][9]
                tab1.append(['| ' + str(term1), val1, unitx, mfile2])

            elif self.model1.mdict[_m][0] == '[f]':
                edict1 = self.model1.mdict[_m]
                term1 = self.model1.mdict[_m][1].strip()
                val1 = "function"
                unitx = "-"
                mfile2 = self.model1.mdict[_m][3]
                tab1.append(['| ' + str(term1), val1, unitx, mfile2])

            else:
                pass

        print("   Table of Model Variables")

        ## onceweb modified
        table1 = tabulate
        print(table1.tabulate(tab1,
                headers=[' Variable', 'Value or Type', 'Units', 'File'],
                tablefmt='rst', floatfmt=".4f"))

    def _out_term(self):
        """check -e or -b flag and echo calc to console or browser"""
        # onceweb modified
        sysargv = cfg.sysargv
        if len(sysargv) > 2 and sysargv[2].strip() == '-e':
            print()
            print("|||||||||||||||||||||||||||||||||  "
                  "echo calc file ||||||||||||||||||"
                  "|||||||||||||||||")
            print()
            try:
                mod1 = open(self.calcf, 'r')
                _r = mod1.readlines()
                mod1.close()
                for _i in _r:
                    print(_i)
            except:
                pass
        elif len(sysargv) > 2 and sysargv[2].strip() == '-b':
            try:
                os.system("start chrome " + self.calcf)
            except:
                try:
                    os.system("start firefox " + self.calcf)
                except:
                    try:
                        os.system("start iexplore file:///%CD%/" +
                                  self.calcf)
                    except:
                        pass

    @staticmethod
    def _cmdline():
    """command line help"""
    print()
    print("onceutf" + __version__ + ": writes on-c-e calcs")
    print()
    print("Use:")
    print("python oncewebnnn.py modfile.m.txt (options)")
    print("    when oncewebnnn.py is in model folder")
    print("         or")
    print("python -m oncewebnnn modfile.m.txt (options)")
    print("    when oncewebnnnn.py is in Python /Lib/site-packages")
    print()
    print()
    print("options:")
    print("   -h    prints this prompt")
    print("   -c    echoes UTF-8 model output to console (stdout)")
    print("   -b    opens UTF-8 model output in Windows browser")
    print("         tries the following browsers in order:")
    print("             start chrome modfile.m.txt ")
    print("             start firefox modfile.m.txt")
    print("             start iexplore file:///%CD%/modfile.m.txt")
    print("set browser encoding to UTF-8; refer to user manual")
    print()
    print("outputs:")
    print("   model.logm.txt")
    print()
    print("if no errors then outputs:")
    print("   modfile.calm.txt (UTF-8 formatted calculation file")
    print("   modfile.summ.txt (calculation summary)")
    print("   modfile.m.py     (Python equation file")
    sys.exit(1)
