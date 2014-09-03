from __future__ import division
from __future__ import print_function
import os
import sys
import oncepy
from oncepy import ccheck
from oncepy import oconfig as cfg

class CalcPDF(object):
    """write PDF calc from rst file"""

    def __init__(self, mfile):
        """initialize rst, tex and pdf file paths"""

        self.mfile = mfile
        #print('mfile', self.mfile)
        self.ew = ccheck.ModCheck()

        self.pdffile = ('cal' + self.mfile).replace('.txt','.pdf')
        self.pdffile1 = self.mfile.replace('.txt', '.pdf')
        self.rstfile = self.mfile.replace('.txt', '.rst')
        self.texfile = self.mfile.replace('.txt', '.tex')


        cfg.stylefile = 'built-in'
        self.stylepathpdf = oncepy.__path__[0] + '/once.sty'

        os.chdir(os.pardir)
        if os.path.isfile('once.sty'):
            cfg.stylefile = 'project folder'
            self.stylepathpdf = os.getcwd() + '/once.sty'

        os.chdir(cfg.mpath)
        if os.path.isfile('once.sty'):
            cfg.stylefile = 'model folder'
            self.stylepathpdf = os.getcwd() + '/once.sty'

    def gen_tex(self):
        """generate tex file and call mod_tex

        """
        newstylepath = self.stylepathpdf.replace('\\', '/')
        pypath = os.path.dirname(sys.executable)
        rstpath = pypath + "/Scripts/rst2latex.py "
        #print(rstpath)
        tex1 = "".join(["python ", rstpath,
                        "--documentclass=report ",
                        "--documentoptions=12pt,notitlepage ",
                        "--stylesheet=",
                        newstylepath + " ",
                        str(self.rstfile) + " ",
                        str(self.texfile)])
        #print(tex1)
        os.system(tex1)
        self.ew.errwrite("< tex file written >", 0)
        self.mod_tex(self.texfile)

    def mod_tex(self, tfile):
        """modify tex file and bypass escapes

        modifies this type of entry
        "**" + var3 + " |" + "aa-bb " + strend + "**", file=self.rf1)

        calls one_chapter

        """
        texin = open(tfile, 'r')
        texf = texin.read()
        texin.close()
        texf = texf.replace("""inputenc""", """ """)
        texf = texf.replace("aa-bb ", """\\hfill""")
        texout = open(tfile, 'w')
        print(texf, file=texout)
        texout.close()
        self.one_chapter(self.texfile)

    def one_chapter(self, tfile):
        """modify tex file for one chapter

        """
        texin = open(tfile, 'r')
        texf = texin.read()
        texin.close()
        if texf.find("phantom") > -1:
            texf = texf.replace("""\\begin{document}""", '')
            texf = texf.replace("""\\maketitle""", '')
            texf = texf.replace("""\\title{\\phantomsection%""",
                                """\\begin{document}""" + "\n" +
                                """\\chapter{%""")
        texout = open(tfile, 'w')
        print(texf, file=texout)
        texout.close()
        self.ew.errwrite("< tex file modified >", 0)

    def gen_pdf(self):
        """generate PDF file

        """
        pdf1 = 'latexmk -xelatex -quiet ' + str(self.texfile)
        os.system(pdf1)
        self.ew.errwrite('', 1)
        self.ew.errwrite("< xelatex " + str(self.texfile) +" >", 0)
        self.ew.errwrite("< pdf file written - pass 1 >", 0)
        os.system(pdf1)
        self.ew.errwrite("< pdf file written - pass 2 >", 0)
        if os.path.isfile(self.pdffile):
            os.remove(self.pdffile)
        os.rename(self.pdffile1, self.pdffile)
