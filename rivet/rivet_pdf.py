from __future__ import division
from __future__ import print_function
from collections import OrderedDict
import once.config as cfg
import os

class CalcPDF(object):
    """write PDF calc from rst file
    
    """

    def __init__(self):
        """Initialize rst, tex and pdf file paths.

        """
        self.vbos = cfg.verboseflag
        self.el = ModCheck()
        self.mfile = cfg.mfile
        #print('mfile', self.mfile)
        self.xpath = cfg.xpath
        self.ppath = cfg.ppath
        self.cpath = cfg.cpath
        self.pdffile = cfg.cfilepdf
        self.rfile = cfg.rstfile
        self.texfile = cfg.texfile
        self.rpath = cfg.rpath
        self.calctitle = cfg.calctitle
        self.texfile2 = os.path.join(cfg.xpath, self.texfile)
        self.auxfile =  os.path.join(cfg.xpath, cfg.mbase + '.aux')
        self.outfile =  os.path.join(cfg.xpath, cfg.mbase + '.out')
        self.texmak2 =  os.path.join(cfg.xpath, cfg.mbase + '.fls')
        self.texmak3 =  os.path.join(cfg.xpath, cfg.mbase + '.fdb_latexmk')
        self.stylepathpdf = os.path.join(once.__path__[0],'once.sty')
        
    def gen_tex(self):
        """Generate tex file and call mod_tex.

        """
        #print("gen_tex1")
        fixstylepath = self.stylepathpdf.replace('\\', '/')
        try:
            pypath = os.path.dirname(sys.executable)
            rstexec = os.path.join(pypath,"Scripts","rst2latex.py")
            with open(rstexec) as f1:
                f1.close()
            pythoncall = 'python '
            #print("< rst2latex path 1> " + rstexec)
        except:
            try:
                pypath = os.path.dirname(sys.executable)
                rstexec = os.path.join(pypath,"rst2latex.py")
                with open(rstexec) as f1:
                    f1.close()
                pythoncall = 'python '
                #print("< rst2latex path 2> " + rstexec)
            except:
                rstexec = "/usr/local/bin/rst2latex.py"
                pythoncall = 'python '
                #print("< rst2latex path 3> " + rstexec)
        tex1 = "".join([pythoncall, rstexec
                        ,
                        " --documentclass=report ",
                        " --documentoptions=12pt,notitle,letterpaper",
                        " --stylesheet=",
                        fixstylepath + " ", self.rfile + " ", self.texfile2])
        self.el.logwrite("tex call:\n" + tex1, self.vbos)
        try:
            os.system(tex1)
            self.el.logwrite("< TeX file written >", self.vbos)
        except:
            print()
            self.el.logwrite("< error in docutils call >", self.vbos)
        
        self.mod_tex(self.texfile2)


    def mod_tex(self, tfile):
        """Modify TeX file to avoid problems with escapes:
            -  Replace marker "aaxbb " inserted by once with
              \\hfill (not handled by reST).
            - Delete inputenc package
            - Modify title section and add table of contents
            
        """
        with open(tfile, 'r') as texin:
            texf = texin.read()
        texf = texf.replace("""inputenc""", """ """)
        texf = texf.replace("aaxbb ", """\\hfill""")
        texf = texf.replace("""\\begin{document}""",
                            """\\renewcommand{\contentsname}{"""+
                            self.calctitle + "}\n"+
                            """\\begin{document}"""+"\n"+
                            """\\makeatletter"""+
                            """\\renewcommand\@dotsep{10000}"""+
                            """\\makeatother"""+
                            """\\tableofcontents"""+
                            """\\listoftables"""+
                            """\\listoffigures""")    
        with open (tfile, 'w') as texout:
            print(texf, file=texout)


    def gen_pdf(self):
        """Write PDF file from tex file.

        """
        os.chdir(self.xpath)
        if os.path.isfile(os.path.join(self.ppath,self.pdffile)):
            os.remove(os.path.join(self.ppath,self.pdffile))
        pdf1 ='latexmk -xelatex -quiet -f '+os.path.join(self.xpath,self.texfile)
        #print("pdf call:  ", pdf1)
        self.el.logwrite("< PDF calc written >", self.vbos)    
        os.system(pdf1)
        pdfname = self.pdffile
        pdfname = list(pdfname)
        pdfname[0]='m'
        pdfname2 = "".join(pdfname)
        pdfftemp = os.path.join(self.xpath, pdfname2)
        pdffnew = os.path.join(self.cpath, self.pdffile)
        try:
            os.remove(pdffnew)
        except:
            pass
        try:
            os.rename(pdfftemp, pdffnew)
        except:    
            self.el.logwrite("< PDF calc not moved from temp >", 1)
        tocname2 = pdfname2.replace('.pdf','.toc')
        toctemp = os.path.join(self.xpath, tocname2)
        tocnew = os.path.join(self.rpath, tocname2)
        try:
            shutil.copyfile(toctemp, tocnew)
        except:    
            self.el.logwrite("< TOC not moved from temp >", 1)


    def reprt_list(self):
        """Append calc name to reportmerge.txt
        
        """
        try: 
            filen1 = os.path.join(self.rpath, "reportmerge.txt")
            print(filen1)
            file1 = open(filen1, 'r')
            mergelist = file1.readlines()
            file1.close()
            mergelist2 = mergelist[:]
        except OSError:
            print('< reportmerge.txt file not found in reprt folder >')
            return
        calnum1 = self.pdffile[0:5]
        file2 = open(filen1, 'w')
        newstr1 = 'c | ' +  self.pdffile  + ' | ' + self.calctitle
        for itm1 in mergelist:
            if calnum1 in itm1:
                indx1 = mergelist2.index(itm1)
                mergelist2[indx1] = newstr1
                for j1 in mergelist2: file2.write(j1)
                file2.close()
                return
        mergelist2.append("\n" + newstr1)
        for j1 in mergelist2: file2.write(j1)
        file2.close()
        return

class ProjStart(object):
    """Compile calcs into a project calc set - not started"""

    def __init__(self):
        """ Construct lists and dictionaries of project calc data
        ::
        
          **methods**
          build_pdict() constructs the proj calc data dictionary
          build_plist() constructs the proj calc division list
        
          pdf=
          always
          never
          asneeded
        """
        # files


        # method tags
        plist = ['[p]', '[#] pformat' '[#]', '[~]']
        self.ptags = plist
        self.pd = OrderedDict()


    def build_pdict(self):
        """constructs the project data dictionary

        """
        pass


    def build_plist(self):
        """ constructs the proj calc division list

        """

        pass


class WritePcalc(object):
    """ Write the project PDF calc """

    pass
