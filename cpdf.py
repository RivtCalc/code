from __future__ import division
from __future__ import print_function
import os
import sys
import oncepy
from oncepy import ccheck
from oncepy import oconfig as cfg

class CalcPDF(object):
    """write PDF calc from rst file"""

    def __init__(self, mfile, pdffile):
        """initialize rst, tex and pdf file paths"""

        self.mfile = mfile
        #print('mfile', self.mfile)
        self.ew = ccheck.ModCheck()

        self.pdffile = pdffile
        self.rstfile = self.mfile.replace('.txt', '.rst')
        self.texfile = self.mfile.replace('.txt', '.tex')
        self.pdffile1 = self.mfile.replace('.txt', '.pdf')

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
        """generate and modify tex file"""
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
        # write tex file
        #print(tex1)
        os.system(tex1)
        self.ew.ewrite2("< tex file written >")
        self.mod_tex(self.texfile)

    def mod_tex(self, tfile):
        """modify tex file and bypass escapes

        modifies this type of entry
        "**" + var3 + " |" + "aa-bb " + strend + "**",
              file=self.rf1)

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
        """if only one chapter modify tex file

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
        self.ew.ewrite2("< tex file modified >")
        print("< tex file modified >")

    def gen_pdf(self):
        """generate PDF file"""
        pdf1 = 'latexmk -xelatex -quiet ' + str(self.texfile)
        os.system(pdf1)
        self.ew.ewrite2('')
        self.ew.ewrite2("< xelatex " + str(self.texfile) +" >")
        self.ew.ewrite2("< pdf file written - pass 1 >")
        os.system(pdf1)
        self.ew.ewrite2("< pdf file written - pass 2 >")
        if os.path.isfile(self.pdffile):
            os.remove(self.pdffile)
        os.rename(self.pdffile1, self.pdffile)
