from __future__ import print_function
from __future__ import division
import os
import sys
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


class ModStart():
    """reads a on-c-e model and returns a UTF-8 or PDF calc

    The program **oncepy** takes a **on-c-e** ASCII model as input
    and returns a formatted structural engineering calculation. The
    program formats structural calculations using a simple, natural
    markup language.

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

    For further details refer to the user manual and programs here:
        http://on-c-e.org/programs/

    email contact:
    r holland
    once.pyproject@gmail.com

    Running the Program
    ===================

    Copy the **oncepy** package (folder) to the python/lib/site-packages
    directory. From a terminal window type:

    .. code:: python

        python -m oncepy xxyy.model.txt (-c or -b)


    where *xxyy.model.txt* is the file name, xx is the chapter number
    and yy is the model number.

    The program will write the calc file calxxyy.model.txt and the
    -c or -b options will echo the calc to a console (-c) or
    a Windows browser (-b). The -b option is needed on Windows because
    of UTF-8 encoding limitations in the console.

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

        **methods:**
            gen_paths()  find model and project paths
            cmdline()  command line prompt
            gen_files() generate new file names
            out_term() check console printing flags
            sum_calc() write calculation summary to stdout

        """
    def __init__(self):
        """initialize files and process classes

        file names are stored in oconfig.py

        """
        # initialize file names
        self.stylepath = '-'
        self.calcf = ''
        self.pdff = ''
        self.pyf = ''
        self.sumf = ''

        self.ew = ccheck.ModCheck()

        if cfg.stylefile == 'project folder':
            os.chdir(os.pardir)
            self.stylepath = os.getcwd()
            os.chdir(cfg.mpath)
        elif cfg.stylefile == 'model folder':
            self.stylepath = os.getcwd()
        else:
            self.stylepath = oncepy.__path__

        sys.path.append(cfg.mpath)

        # generate new file names
        self.gen_files()

        # build dictionaries
        self.model1 = cdict.ModDicts()

        # write variable list to stdout
        self.var_table()

        # write UTF calc
        ctext.CalcText(self.model1.mdict, self.calcf, self.pyf,
                       self.sumf)

        # calculation type
        self.ew.ewrite2('')
        self.ew.ewrite2('<calculation type> ' + cfg.caltype)
        self.ew.ewrite2('')

        rstfile = ''
        texfile = ''

        # write rst and PDF calc if options selected
        if cfg.caltype.strip() == 'pdf'or \
                        cfg.caltype.strip() == 'PDF':

            # PDF files
            rstfile = cfg.mfile.replace('.txt', '.rst')
            texfile = cfg.mfile.replace('.txt', '.tex')
            auxfile = cfg.mfile.replace('.txt', '.aux')
            outfile = cfg.mfile.replace('.txt', '.out')
            logfile = cfg.mfile.replace('.txt', '.log')

            # clean out any auxiliary files
            try:
                os.remove(rstfile)
            except OSError:
                pass
            try:
                os.remove(auxfile)
            except OSError:
                pass
            try:
                os.remove(texfile)
            except OSError:
                pass
            try:
                os.remove(outfile)
            except OSError:
                pass
            try:
                os.remove(logfile)
            except OSError:
                pass

            rstout1 = crst.CalcRST(self.model1.mdict)
            rstout1.gen_rst()
            self.ew.ewrite2("< rst file written >")
            pdfout1 = cpdf.CalcPDF(cfg.mfile, self.pdff)
            pdfout1.gen_tex()
            pdfout1.gen_pdf()
            self.ew.ewrite2("< pdf file written >")

            # open pdf file
            #try:
            #    os.system(self.pdff)
            #    self.ew.ewrite2('')
            #    self.ew.ewrite2("< opened PDF calc >")
            #except:
            #    pass

        elif cfg.caltype.strip() == 'rst':
            rstfile = cfg.mfile.replace('.txt', '.rst')
            rstout1 = crst.CalcRST(self.model1.mdict)
            rstout1.gen_rst()
            self.ew.ewrite2('')
            self.ew.ewrite2("< rst file written >")
        else:
            pass

        csumm2 =  ((" Files written:\n" +
                    " ------------------\n" +
                    " model file    :  {}\n" +
                    " python file   :  {}\n" +
                    " summary file  :  {}\n" +
                    " reST file     :  {}\n" +
                    " tex file      :  {}\n" +
                    " PDF file      :  {}\n").format(
                                self.calcf, self.pyf, self.sumf,
                                rstfile, texfile, self.pdff))

        print('\n', csumm2)
        print("< calculation completed >")
        self.ew.ewrite2(csumm2)
        self.ew.ewrite2("< calculation completed >")

        # UTF-8 calc to console or browser, -c or -b switch
        self.out_term()

    def gen_files(self):
        """generate new file names"""

        calcf1 = cfg.mfile.split('.')
        self.pdff = '.'.join(['cal' + calcf1[0], calcf1[1], 'pdf'])
        self.calcf = '.'.join(['cal' + calcf1[0], calcf1[1], calcf1[2]])
        self.sumf = '.'.join(['sum' + calcf1[0], calcf1[1], calcf1[2]])
        self.pyf = cfg.mfile.replace('.txt', '.py')

        csumm1 = ("""
    Calculation Summary
    ===================

    Files and paths
    ---------------
    model input    :  {}
    calc output    :  {}
    py output file :  {}
    summary file   :  {}
    units path     :  {}
    model path     :  {}
    project path   :  {}
    project file   :  {}
    style path     :  {}
        """.format(cfg.mfile, self.calcf, self.pyf, self.sumf,
                   cfg.unitfile, cfg.mpath,
                   cfg.ppath, cfg.pfile, cfg.stylefile))

        print(csumm1)
        self.ew.ewrite2(csumm1)

    def var_table(self):
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
                term1 = self.model1.mdict[_m][2].strip()
                val1 = "function"
                unitx = "-"
                mfile2 = self.model1.mdict[_m][4]
                tab1.append(['| ' + str(term1), val1, unitx, mfile2])

            elif self.model1.mdict[_m][0] == '[d]':
                if self.model1.mdict[_m][2].strip() == 'r':
                    term1 = self.model1.mdict[_m][3].strip()
                    val1 = "data"
                    unitx = "-"
                    mfile2 = self.model1.mdict[_m][6]
                    tab1.append(['| ' + str(term1), val1, unitx, mfile2])

            else:
                pass

        print("   Table of Model Variables")

        ## onceweb modified
        table1 = tabulate
        tabout1 = (table1.tabulate(tab1,
                headers=[' Variable', 'Value or Type', 'Units', 'Model'],
                tablefmt='rst', floatfmt=".4f"))

        print(tabout1)
        self.ew.ewrite2(tabout1)

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
                mod1 = open(self.calcf, 'r')
                _r = mod1.readlines()
                mod1.close()
                for _i in _r:
                    print(_i)
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
        print("python -m oncepy xxyy.modfile.txt (options)")
        print("   where xx is the chapter and yy is the model number")
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
        print("   logxxyy.model.txt")
        print()
        print("if no errors then outputs:")
        print("     xxyy.modfile.py     (Python equation file")
        print("     calxxyy.modfile.txt (UTF-8 calc")
        print("     sumxxyy.modfile.txt (calculation summary)")
        print("if option selected in model or project file:")
        print("     calxxyy.modfile.pdf (PDF calc")
        print("     project.pdf (PDF project calc)")

        sys.exit(1)
