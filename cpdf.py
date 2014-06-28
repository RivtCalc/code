

class CalcPDF(object):

    def __init__(self):


            self.ew.ewrite2('')
            self.ew.ewrite2("< rst file written >")

            rstfile = self.mfile.replace('.txt', '.rst')
            texfile = self.mfile.replace('.txt', '.tex')
            pdffile = self.mfile.replace('.txt', '.pdf')
            #auxfile = self.mfile.replace('.txt', '.aux')
            #outfile = self.mfile.replace('.txt', '.out')
            newstylepath = self.stylepath.replace('\\', '/')
            tex1 = "".join(["python ",
                                "%PYTHONHOME%/scripts/rst2latex.py ",
                                "--documentclass=report ",
                                "--documentoptions=12pt ",
                                "--stylesheet=",
                                newstylepath + " ",
                                str(rstfile) + " ",
                                str(texfile)])

            # write tex file
            os.system(tex1)
            self.ew.ewrite2('')
            self.ew.ewrite2("< tex file written >")

            # modify tex file after the fact to deal with escapes
            self._mod_tex(texfile)
            self.ew.ewrite2('')
            self.ew.ewrite2("< tex file modified >")


            pdf1 = "xelatex " + str(texfile)
            os.system(pdf1)
            self.ew.ewrite2('')
            self.ew.ewrite2("< xelatex " + str(texfile) +" >")
            self.ew.ewrite2("< pdf file written - pass 1 >")
            os.system(pdf1)
            self.ew.ewrite2("< pdf file written - pass 2 >")

            # open pdf file
            try:
                os.system(pdffile)
            except:
                pass

    def _mod_tex(self, tfile):
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