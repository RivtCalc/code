from __future__ import print_function
import os
import sys
import tabulate
from numpy import *
from oncemod import cdict
from oncemod import ctext
from oncemod import cpdf
import oncemod.config as om
try:
    from unitc import *
except:
    from oncemod.calcunits import *


class ModStart():
    """reads a on-c-e markup file and returns a formatted document

    The program **oncemod** takes a **on-c-e** calculation markup
    file as input and returns a formatted UTF-8 or PDF
    calculation document as output.

    The alpha code and documentation are released to solicit early
    feedback on basic concepts.  Currently the program can
    run usable calculation models, as illustrated in the examples.
    However a number of classes and methods are not implemented yet.
    The primary purposes of the beta development phase will be to
    solidify and complete the model interface operations, add error
    checking and unit tests, and write an installer.

    Progress can be tracked at Trello:
    https://trello.com/b/RQRlXBzH/on-c-e-roadmap-for-beta-release

    To run the program, unzip **oncennn.zip** (where nnn is the
    version number) and copy the oncemod folder into the Python
    site-packages folder.  Run the program from the command line:

    .. code:: python

        python -m oncemod modfile.n.txt -e

        or

        python -m oncemod modfile.n.txt -b

    where *modfile.n.txt* is the file name of the input model number n,
    and *-e* or *-b* are options to echo results to a console or browser
    on Windows. The *-b* option is needed on Windows because of UTF-8
    encoding deficiencies. To open a console window from a folder in
    Windows, navigate to the folder using Explorer, hold the shift key,
    right click, click on 'open command window here' in the context
    menu.

    Change the browser encoding settings if needed:

        - Chrome - type chrome:settings/fonts  in url bar -
          scroll to the bottom of the dialog box and make the change.
        - Firefox - options - content - advanced - UTF-8
        - Internet Explorer - right click - encoding - UTF-8

    The program will execute the file and return results in several
    files. For further details refer to the  manual and program here:

    **oncemod** http://structurelabs.knackhq.com/oncedb#programs/

    **onceweb** a single file subset of **oncemod**
    https://on-c-e.info or
    https://www.dropbox.com/sh/f27xav5sbahejqs/yZ_rUJq8nJ

    Source code and documentation are here:

    http://on-c-e.github.io/

    email contact: once.pyproject@gmail.com

    **methods**

    gen_paths()  find model and project paths

    cmdline()  command line prompt - help

    gen_files() generate new file names

    check_mod() validate model file - check for syntax errors

    out_term() check -p flag for printing calculation to terminal

    summ_calc() write summary of calculation results to stdout

    """
    def __init__(self, sysargv):
        """initialize files and paths

        Arguments:
        sys.argv : command line arguments

        """

        self.sysargv = sysargv
        self.projpath = om.projpath
        self.mfile = om.mfile
        self.mpath = om.mpath
        self.setname = om.setname
        self.calcf = ''
        self.pyf = ''
        self.sumf = ''

        self.stylepath = os.path.join(self.projpath, om.stylefile)

        # create new output file names
        self.gen_files()

        # write variable list to stdout
        self.calc_summ()

        # check model files for errors
        self.check_mod()

        sys.path.append(self.projpath)
        sys.path.append(self.mpath)

        try:
            # write output files
            model1 = cdict.ModDict(self.mfile, self.mpath)
            print()
            print("< model dictionary built > \n")

            ctext.CalcText(model1.mdict, self.calcf, self.pyf,
                                         self.sumf, self.mpath)
        except RuntimeError:
            print("< cannot process calculation >")
            print("<(%s:%s)>" % (sys.exc_info()[0], sys.exc_info()[1]))
            sys.exit(1)

        print()
        print("<calculation type>", om.caltype)
        print()
        # write rst and pdf output if needed
        rstfile = ''
        texfile = ''
        pdffile = ''
        pdfout1 = cpdf.CalcPDF(model1.mdict, self.mpath, self.mfile)
        if om.caltype == 'rst':
            print(" ")
            print("< rst file written >")
            rstfile = self.mfile.replace('.txt', '.rst')
            pdfout1.prt_rst()

        elif om.caltype == 'pdf':
            print(" ")
            pdfout1.prt_rst()
            print("< rst file written >")
            rstfile = self.mfile.replace('.txt', '.rst')
            texfile = self.mfile.replace('.txt', '.tex')
            pdffile = self.mfile.replace('.txt', '.pdf')
            auxfile = self.mfile.replace('.txt', '.aux')
            outfile = self.mfile.replace('.txt', '.out')
            newstylepath = self.stylepath.replace('\\', '/')
            estr_tex = "".join(["python ",
                               "%PYTHONHOME%/scripts/rst2latex.py ",
                                "--documentclass=report ",
                                "--documentoptions=12pt ",
                                "--stylesheet=",
                                newstylepath + " ",
                                str(rstfile) + " ",
                                str(texfile)])
            print(" ")

            print(estr_tex)
            try:
                os.system("del " + auxfile)
                os.system("del " + outfile)
            except:
                pass
            os.system(estr_tex)
            print("< tex file written >")

            print(" ")
            print("< tex file modified >")
            self.mod_tex(texfile)

            print(" ")
            estr_pdf = "xelatex " + str(texfile)
            print(estr_pdf)
            os.system(estr_pdf)
            print("< pdf file written - pass 1 >")
            os.system(estr_pdf)
            print("< pdf file written - pass 2 >")
            try:
                os.system(pdffile)
            except:
                pass

        print(( " Files written:\n" +
                " ------------------\n" +
                " model file    :  {}\n" +
                " python file   :  {}\n" +
                " summary file  :  {}\n" +
                " reST file     :  {}\n" +
                " tex file      :  {}\n" +
                " PDF file      :  {}\n").format(self.calcf, self.pyf,
                                self.sumf, rstfile, texfile, pdffile))

        print("< calculation completed >")

        # write output if -e or -b option is given on command line
        self.out_term()
        self.out_browser()

    def check_mod(self):
        """validate model file - check for syntax errors"""

        #mod = check.ValidateModel(mfile)
        efile = open('calc.log', 'w')
        efile.write(str("< todo: write error log code >"))
        efile.close()

    def gen_files(self):
        """generate new file names"""

        self.calcf = self.mfile.replace('.txt', 'cal.txt')
        self.pyf = self.mfile.replace('.txt', '.py')
        self.sumf = self.mfile.replace('.txt', 'sum.txt')

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
                   om.impcheck, self.mpath,
                   self.projpath, self.setname, self.stylepath))

    def calc_summ(self):
        """
        write summary of calculation results to stdout

        equations: [[e], statement, expr, ref, decimals, units, prnt opt]
        terms: [[t], statement, expr, ref ]

        """

        # build model dictionary
        model1 = cdict.ModDict(self.mfile, self.mpath)

        tab1 = []
        for _m in model1.mdict:
            #print(_m)
            if _m[0] != '_':
                term1 = _m.strip()
                edict1 = model1.mdict[_m]
                state1 = edict1[1].strip()
                exec(state1)
                val1 = eval(term1)
                unitx = ' --- '
                try:
                    newunit = edict1[5].strip()
                    if len(newunit):
                        val1 = val1.asUnit(eval(newunit))
                except:
                    pass

                try:
                    unitx = val1.strUnit()
                    val1 = val1.asNumber()
                except:
                    pass
                tab1.append(['| ' + str(term1), val1, unitx])
        #print(tab1)
        print("   Table of Model Variables")
        print(tabulate.tabulate(tab1, headers=[' Variable', 'Value',
                        'Units'], tablefmt='rst', floatfmt=".4f"))

    def out_term(self):
        """check for -e flag and echo calculation to terminal"""
        # onceweb modified
        try:
            if self.sysargv[2].strip() == '-e':
                print()
                print("|||||||||||||||||||||||||||||||||  "
                      "echo calc file ||||||||||||||||||"
                      "|||||||||||||||||")
                print()
                mod1 = open(self.calcf, 'r')
                _r = mod1.readlines()
                mod1.close()
                for _i in _r:
                    print(_i)
        except:
            pass

    def out_browser(self):
        """check for -b flag and open calculation in Windows browser"""
        try:
            if self.sysargv[2].strip() == '-b':
                try:
                    os.system("start chrome " + self.mfile)
                except:
                    try:
                        os.system("start firefox " + self.mfile)
                    except:
                        try:
                            os.system("start explore file:///%CD%/" +
                                      self.mfile)
                        except:
                            pass
        except:
            pass

    def mod_tex(self, tfile):
        """modify tex file"""
        texin = open(tfile, 'r')
        texf = texin.read()
        texin.close()
        texf = texf.replace("""inputenc""", """ """)
        texf = texf.replace(""" xxxhfillxxx""",
                            """\\hfill""")
        texf = texf.replace("""yxxhfillxxx""",
                            """\\hfill""")
        texout = open(tfile, 'w')
        print(texf, file=texout)
        texout.close()

    @staticmethod
    def gen_paths():
        """find model and project paths and add to config file"""

        dirname = os.path.dirname
        baname = os.path.basename
        ofile = sys.argv[1]
        mfile = os.path.basename(ofile)
        mpath = os.getcwd()
        projdir = om.projpath
        setname = om.setname

        ofilestr = open(ofile, 'r')
        ofilestrv = ofilestr.readlines()

        for line in ofilestrv:
            if line[:10] == '[#] format':
                setname = line.split('|')[4].strip()
                projdir = line.split('|')[3].strip()
                if len(projdir) == 0:
                    projdir = mpath
                else:
                    dir1 = dirname(os.getcwd())
                    try:
                        for _ in range(4):
                            bname = baname(dir1)
                            if bname == projdir:
                                projdir = dir1
                                break
                            dir1 = dirname(dir1)
                    except:
                        pass

        om.mfile = mfile
        om.mpath = mpath
        om.projpath = projdir
        om.setname = setname

    @staticmethod
    def cmdline():
        """command line prompt - help"""
        print()
        print("onceweb" + __version__ + ": writes calcs")
        print()
        print("Use: python oncemod -m modfile_n.txt (options)")
        print()
        print("options:")
        print("   -h    prints this prompt")
        print("   -e    echoes UTF-8 model output to screen (stdout)")
        print("   -b    opens UTF-8 model output in Windows browser")
        print("         tries the following browsers in order:")
        print("             start chrome modfile_n.txt")
        print("             start firefox modfile_n.txt")
        print("             start iexplore file:///%CD%/modfile_n.txt")
        print("set browser encoding to UTF-8; refer to user manual")
        print()
        print("outputs:")
        print("   calc.log")
        print()
        print("if no errors then outputs:")
        print("     modfile_ncal.txt (UTF-8 formatted calculation file")
        print("     modfile_nsum.txt (calculation summary)")
        print("     modfile_n.py     (Python equation file")
        sys.exit(1)
