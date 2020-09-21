#!
"""converts calc-strings to reST-strings

The ParseReST class converts model-strings to intermediate reST-strings which
are then converted to pdf or html docs.Model-strings must be indented 4 spaces.
Commands start with a double bar (||) and are single line, except where noted.
Tags are included inline, with the associated text. """

import os 
import sys
import csv
import textwrap
import subprocess
import tempfile
import re
import io
import logging
import numpy.linalg as la
import pandas as pd
import sympy as sp
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
from IPython.display import display as _display
from IPython.display import Image as _Image
from io import StringIO
from sympy.parsing.latex import parse_latex
from sympy.abc import _clash2
from sympy.core.alphabets import greeks
from tabulate import tabulate 
from pathlib import Path
from numpy import *
from IPython.display import display as _display
from IPython.display import Image as _Image
try:
    from PIL import Image as PImage
    from PIL import ImageOps as PImageOps
except:
    pass
from rivtcalc.rc_unit import *

logging.getLogger("numexpr").setLevel(logging.WARNING)

class WriteRST:
    """write calc output to reST file

    """
    def __init__(self, strL: list, folderD: dict, setcmdD: dict,
         setsectD: dict, rivtD: dict, exportS: str):
        
        """process rivt-string to reST-string

        The WriteRST class converts rivt-strings to reST-strings.
        Rivt-strings must be indented 4 spaces. Commands start with
        a double bar (||) and are single line, except where noted. Tags
        are inserted inline with the associated text.
        
        Args:
            exportS (str): stores values that are written to file
            strL (list): calc lines
            folderD (dict): folder paths
            setcmdD (dict): command settings
            setsectD (dict): section settings
            rivtD (dict): global rivt dictionary
        """
    
        self.calcS = """"""             # calc string
        self.exportS = exportS
        self.strL = strL 
        self.folderD = folderD
        self.setsectD = setsectD
        self.setcmdD = setcmdD
        self.rivtD = rivtD
        self.valL = []                  # value list
    
    def _refs(self, objnumI: int, typeS: str) -> str:
        """reference label for equations, tables and figures

        Args:
            objnumI (int): equation, table or figure numbers
            setsectD (dict): section dictionary
            typeS (str): label type

        Returns:
            str: [description]
        """

        objfillS = str(objnumI).zfill(2)
        sfillS = str(self.setsectD["snumS"]).strip().zfill(2)
        cnumSS = str(self.setsectD["cnumS"])
        refS = typeS + cnumSS + "." + sfillS + "." + objfillS 

        return refS

    def _tags(self, tagS: str, tagL: list) -> tuple:
        """parse tag
        
        Args:
            tagS (str): rivt-string with tag
            tagL (list): list of tag parameters
            setsectD (dict): section dictionary
            
        Return:
            rstS (str): restrutured text string 
            setsectD (dict): updated section dictionary
        """

        tagS = tagS.rstrip(); uS = ''
        swidthI =  self.setsectD["swidthI"]-1
        try: 
            tag = list(set(tagL).intersection(tagS.split()))[0]
        except:
            uS = tagS
            return uS   
    
        if tag == "[#]_":           # auto increment footnote mark                      
            uS = tagS + "\n"
        elif tag == "[page]_":        # new page
            uS = ".. raw:: latex \n\n \\newpage"
        elif tag == "[line]_":      # horizontal line
            uS = int(self.setsectD["swidthI"]) * '-'   
        elif tag == "[link]_":      # url link
            tgS = tagS.strip("[link]_").strip()
            tgL = tgS.split("|")
            uS = ".. _" + tgL[0].strip() + ": " + tgL[1].strip()  
        elif tag == "[r]_":         # right adjust text
            tagL = tagS.strip().split("[r]_")
            uS = "\\hfill" + tagL[0].strip() 
        elif tag == "[c]_":        # center text  
            tagL = tagS.strip().split("[c]_")
            uS = "\\begin{center} " + tagL[0].strip() + " \\end{center}"
        elif tag == "[x]_":         # format tex
            tagL = tagS.strip().split("[x]_")
            txS = tagL[0].strip()
            uS = ".. raw:: math\n\n   " + txS + "\n"
        elif tag == "[s]_":         # format sympy
            tagL = tagS.strip().split("[s]_")
            spS = tagL[0].strip()
            txS = latex(S(spS))
            uS = ".. raw:: math\n\n   " + txS + "\n"
        elif tag == "[f]_":        # figure caption                    
            tagL = tagS.strip().split("[f]_")
            fnumI = int(self.setsectD["fnumI"]) + 1
            self.setsectD["fnumI"] = fnumI
            refS = self._refs(fnumI, "[ Fig: ") + " ]"
            uS = tagL[0].strip() + " \\hfill " + refS        
        elif tag == "[e]_":         # equation label
            tagL = tagS.strip().split("[e]_")
            enumI = int(self.setsectD["enumI"]) + 1
            self.setsectD["enumI"] = enumI
            refS = self._refs(enumI, "[ Equ: ")
            uS = tagL[0].strip() + " \\hfill " + refS                
        elif tag == "[t]_":         # table label
            tagL = tagS.strip().split("[t]_")
            tnumI = int(self.setsectD["tnumI"]) + 1
            self.setsectD["tnumI"] = tnumI
            refS = self._refs(tnumI, "[Table: ") + "]"
            uS = tagL[0].strip() + " \\hfill " + refS
        elif tag == "[foot]_":      # footnote label
            tagS = tagS.strip("[foot]_").strip()
            uS = ".. [*] " + tagS
        else:
            uS = tagS

        return uS
    
    def _parseRST(self, typeS: str, cmdL: list, methL: list, tagL: list ):
        """parse rivt-string to reST

        Args:
            typeS (str): rivt-string type
            cmdL (list): command list
            methL (list): method list
            tagL (list): tag list
        """
        locals().update(self.rivtD)        
        uL = []                     # command arguments
        indxI = -1                  # method index
        _rgx = r'\[([^\]]+)]_'      # find tags

        self.calcS+= ".. target-notes::\n\n"
        for uS in self.strL:                     
            if uS[0:2] == "##":  continue                   # remove comment
            uS = uS[4:]                                     # remove indent
            if len(uS) == 0 : 
                if len(self.valL) > 0:                      # print value table
                    hdrL = ["variable", "value", "[value]", "description"]
                    alignL = ['left','right','right','left' ]            
                    self._vtable(self.valL, hdrL, "rst", alignL)
                    self.valL = []; print(uS.rstrip(" ")); self.calcS += " \n" 
                    self.rivtD.update(locals()) 
                    continue
                else: self.calcS += "\n"; continue
            try: 
                if uS[0] == "#" : continue                   # remove comment      
            except:
                self.calcS += "\n"; continue
            if uS.strip() == "[literal]_" : continue
            if re.search(_rgx, uS):                          # check for tag
                utgS = self._tags(uS, tagL)
                self.calcS += utgS.rstrip() + "\n"
                continue     
            if typeS == "values":                            # chk for values
                self.setcmdD["saveB"] = False  
                if "=" in uS and uS.strip()[-2] == "||":     # value to file
                    uS = uS.replace("||"," "); self.setcmdD["saveB"] = True                      
                if "=" in uS:                                # assign value
                    uL = uS.split('|'); self._vassign(uL)
                    continue
            if typeS == "table":                             # check for table
                if uS[0:2] == "||":           
                    uL = uS[2:].split("|")
                    indxI = cmdL.index(uL[0].strip())
                    methL[indxI](uL); continue 
                else:
                    exec(uS); continue                       # exec table code 
            if uS[0:2] == "||":                              # check for cmd
                uL = uS[2:].split("|")
                indxI = cmdL.index(uL[0].strip())
                methL[indxI](uL); continue                   # call any cmd
                
            self.rivtD.update(locals())
            if typeS != "table":                             # skip table prnt
                print(uS); self.calcS += uS.rstrip() + "\n"

    def r_rst(self) -> str:
        """ parse repository string
       
       Returns:
            calcS (list): utf formatted calc-string (appended)
            setsectD (dict): section settings
        """
        
        rcmdL = ["head", "search", "keys", "info", "pdf",  "text", "table",]
        rmethL = [self._rhead,self._rsearch,self._rkeys,self._rinfo,self._rpdf,
                                    self.itext,self.itable]
        rtagL = ["[links]_", "[literal]_", "[foot]_", "[#]__"]

        self._parseUTF("report", rcmdL, rmethL, rtagL)
        
        return self.calcS, self.setsectD

    def _rhead(self, rL):
        if len(rL) < 5: rL += [''] * (5 - len(rL))      # pad parameters
        if rL[1]: calctitleS = rL[1].strip()
        if rL[2] == "toc": pass
        if rL[3] == "readme": pass
        if rL[4] : pass

    def _rsearch(self, rsL):
        a = 4

    def _rkeys(self, rsL):
        a = 4

    def _rinfo(self, rsL):
        b = 5

    def _rpdf(self, rsL):
        b = 5

    def i_rst(self) -> tuple:                 
        """ parse insert-string
       
        Returns:
            calcS (list): utf formatted calc-string (appended)
            setsectD (dict): section settings
            setcmdD (dict): command settings
        """

        icmdL = ["text", "table", "image"]
        imethL = [self._itext, self._itable, self._iimage, ]
        itagL =  ["[page]_", "[line]_", "[link]_", "[literal]_", "[foot]_", 
                  "[s]_","[x]_","[r]_", "[c]_", "[e]_", "[t]_", "[f]_", "[#]_"] 
        
        self._parseUTF("insert", icmdL, imethL, itagL)
        
        return self.calcS, self.setsectD, self.setcmdD

    def _itext(self, iL: list):
        """insert text from file
        
        Args:
            iL (list): text command list
        """
        calP = "r"+self.setsectD["cnumS"]
        txtpath = Path(self.folderD["xpath"]/calP/iL[1].strip())
        with open(txtpath, 'r') as txtf1:
            uL = txtf1.readlines()
        if iL[2].strip() == "indent":
            txtS = "".join(uL)
            widthI = self.setcmdD["cwidth"]
            inS = " "*4
            uL = textwrap.wrap(txtS, width=widthI)
            uL = [inS+S1+"\n" for S1 in uL]
            uS = "".join(uL)
        elif iL[2].strip() == "literal":
            txtS = "  ".join(uL)
            uS = "::\n\n" + txtS + "\n"
        else:
            txtS = "".join(uL)
            uS = "\n" + txtS

        self.calcS += uS + "\n"

    def _itable(self, iL: list):
        """insert table from csv file 
        
        Args:
            ipl (list): parameter list
        """
        alignD = {"s":"", "d":"decimal", "c":"center", "r":"right", "l":"left"}  
        itagL =  ["[page]_", "[line]_", "[link]_", "[literal]_", "[foot]_", 
                        "[r]_", "[c]_", "[e]_", "[t]_", "[f]_", "[#]_"] 
        if len(iL) < 5: iL += [''] * (5 - len(iL))          # pad parameters
        utfS = ""; contentL = []; sumL = []
        fileS = iL[1].strip()
        calpS = "r"+self.setsectD["cnumS"]
        tfileS = Path(self.folderD["tpath"]/calpS/fileS)                           
        with open(tfileS,'r') as csvfile:                   # read csv file
            readL = list(csv.reader(csvfile))
        incl_colL = list(range(len(readL[0])))
        widthI = self.setcmdD["cwidthI"]
        alignS = self.setcmdD["calignS"]
        if iL[2].strip():
            widthL = iL[2].split(",")                       # new max col width
            widthI = int(widthL[0].strip())
            self.setcmdD.update({"cwidthI":widthI})
            saS = alignD[widthL[1].strip()]                 # new alilgnment
            self.setcmdD.update({"calignS":saS})
        naS = saS
        if saS == "decimal":
            saS = ""; naS="decimal"      
        ttitleS = ""
        ttitleS = self.setcmdD["titleS"]
        if iL[3].strip():                                   # title
            ttitleS =  iL[3].strip()
            self.setcmdD.update({"titleS":ttitleS})
        totalL = [""]*len(incl_colL)
        if iL[4].strip():                                   # columns
            if iL[4].strip() == "[:]":
                totalL = [""]*len(incl_colL)
        else:
            incl_colL =  eval(iL[4].strip())
            totalL = [""]*len(incl_colL)
        for row in readL:
            if ttitleS == "title":                          # first row title
                ttitleS = row[0].strip() + " [t]_"
                utgS = self._tags(ttitleS, itagL)
                print(utgS.rstrip()+"\n"); self.calcS += utgS.rstrip() + "\n\n"
                ttitleS = ""; continue
            contentL.append([row[i] for i in incl_colL])
        wcontentL = []
        for rowL in contentL:
            wrowL=[]
            for iS in rowL:
                templist = textwrap.wrap(str(iS), int(widthI)) 
                templist = [i.replace("""\\n""","""\n""") for i in templist]
                wrowL.append("""\n""".join(templist))
            wcontentL.append(wrowL)
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(tabulate(wcontentL, tablefmt="rst", headers="firstrow", 
                    numalign=naS, stralign=saS))            
        utfS = output.getvalue()
        sys.stdout = old_stdout

        self.calcS += utfS + "\n"  

    def _iimage(self, iL: list):
        """insert one or two images from file
        
        Args:
            il (list): image parameters
        """        
        rstS = ""
        if "," in iL[1]:                                        # two images
            scaleF = iL[2].split(",")
            scale1F = float(scaleF[0]); scale2F = float(scaleF[1])
            self.setcmdD.update({"scale1F":scale1F})
            self.setcmdD.update({"scale2F":scale2F})
            fileS = iL[1].split(",")
            file1S = fileS[0].strip(); file2S = fileS[1].strip()
            calpS = "r"+self.setsectD["cnumS"]
            img1S = str(Path(self.folderD["hpath"]/calpS/file1S))
            img2S = str(Path(self.folderD["hpath"]/calpS/file2S))                
            rstS += (".. image:: " + img1S + "\n" +
                    "   :width: " + scale1F + "\n" +
                    ".. :image:: " + img2S + "\n" +
                    "   :width: " + scale2F + "\n" +
                    )
        else:                                                   # one image
            scale1F = float(iL[2]); self.setcmdD.update({"scale1F":scale1F})
            fileS = iL[1].split(","); file1S = fileS[0].strip() 
            calpS = "r"+self.setsectD["cnumS"]
            img1S = str(Path(self.folderD["hpath"]/calpS/file1S))  
            rstS += (".. image:: " + img1S + "\n" +
                    "   :width: " + scale1F + "\n" +
                    "   :align: center \n"
                    )
            self.calcS += rstS + "\n"

    def v_rst(self)-> tuple:
        """parse value-string and set method

        Return:
            calcS (list): utf formatted calc-string (appended)
            setsectD (dict): section settings
            setcmdD (dict): command settings
            rivtD (list): calculation results
            exportS (list): value strings for export
         """

        locals().update(self.rivtD)
        vcmdL = ["config", "value", "data", "func", 
                    "text", "table", "image"]
        vmethL = [self._vconfig, self._vvalue, self._vdata, self._vfunc, 
                             self._itext, self._itable, self._iimage]

        vtagL =  ["[page]_", "[line]_", "[link]_", "[literal]_", "[foot]_", 
                "[s]_","[x]_","[r]_", "[c]_", "[e]_", "[t]_", "[f]_", "[#]_"] 

        self._parseUTF("values", vcmdL, vmethL, vtagL)
        self.rivtD.update(locals())
        return self.calcS, self.setsectD, self.setcmdD, self.rivtD, self.exportS

    def _vconfig(self, vL: list):
        """update dictionary format values

        Args:
            vL (list): configuration parameters
        """
        
        if vL[1].strip() == "sub": self.setcmdD["subB"] = True
        self.setcmdD["trmrI"] = vL[2].split(",")[0].strip()
        self.setcmdD["trmtI"] = vL[2].split(",")[1].strip()

    def _vassign(self, vL: list):
        """assign values to variables and equations
        
        Args:
            vL (list): list of assignments
        """
        
        locals().update(self.rivtD)                                                  
        if len(vL) <= 2:                                           # equation
            unitL = vL[1].split(",")
            unit1S, unit2S = unitL[0].strip(),unitL[1].strip()
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            val1U = val2U = array(eval(valS))
            if unit1S != "-": 
                if type(eval(valS)) == list: 
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS 
                    exec(cmdS, globals(), locals())
                    valU = eval(varS).cast_unit(eval(unit1S))                
                    val1U = str(valU.number()) + ' ' + str(valU.unit()) # case=1
                    val2U = valU.cast_unit(eval(unit2S))
            utfS = vL[0]; spS = "Eq(" + varS + ",(" + valS + "))"  # pretty prnt   
            try: utfS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
            except: pass
            print("\n" + utfS + "\n"); self.calcS += "\n"+ utfS + "\n"
            eqS = sp.sympify(valS)
            eqatom = eqS.atoms(sp.Symbol)
            if self.setcmdD["subst"]: self._vsub(vL)
            else:
                hdrL=[] ; valL=[]
                hdrL.append(varS); hdrL.append("[" + varS + "]")
                valL.append(str(val1U))
                valL.append(str(val2U))
                for sym in eqatom:
                    hdrL.append(str(sym))
                    valL.append(eval(str(sym)))
                alignL = ['center']*len(valL)            
                self._vtable([valL], hdrL, "rst", alignL)
            if self.setcmdD["saveB"] == True:  
                pyS = vL[0] + vL[1] + "  # equation" + "\n" ;#print(pyS)
                self.exportS += pyS
            locals().update(self.rivtD)
        elif len(vL) >= 3:                                          # value
            descripS = vL[2].strip()
            unitL = vL[1].split(",")
            unit1S, unit2S = unitL[0].strip(),unitL[1].strip()
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            val1U = val2U = array(eval(valS))
            if unit1S != "-": 
                if type(eval(valS)) == list: 
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS + "*" + unit1S
                    exec(cmdS, globals(), locals())
                    valU = eval(varS)                
                    val1U = str(valU.number()) + ' ' + str(valU.unit()) # case=1
                    val2U = valU.cast_unit(eval(unit2S))
            self.valL.append([varS, val1U, val2U, descripS])
            if self.setcmdD["saveB"] == True:  
                pyS = vL[0] + vL[1] + vL[2] + "\n"; #print(pyS)
                self.exportS += pyS
        self.rivtD.update(locals())   

    def _vtable(self, tbl, hdrL, tblfmt, alignL):
        """write value table"""

        locals().update(self.rivtD)
        sys.stdout.flush()                                      
        old_stdout = sys.stdout; output = StringIO()
        output.write(tabulate(tbl, tablefmt=tblfmt, headers=hdrL, 
                    showindex=False, colalign=alignL))                    
        valS = output.getvalue()
        sys.stdout = old_stdout; sys.stdout.flush()
        utfS = output.getvalue(); sys.stdout = old_stdout            
        print(utfS); self.calcS += utfS + "\n"  
        self.rivtD.update(locals())            

    def _vvalue(self, vL: list):
        """import values from files

        Args:
            vL (list): value command arguments
        """
        
        locals().update(self.rivtD)
        valL = [] 
        if len(vL) < 5: vL += [''] * (5 - len(vL))            # pad command                                                        
        calpS = "r"+self.setsectD["cnumS"]
        vfileS = Path(self.folderD["tpath"]/calpS/vL[1].strip())
        with open(vfileS,'r') as csvfile:
            readL = list(csv.reader(csvfile))
        for vaL in readL[1:]:                 
            if len(vaL) < 5: vaL += [''] * (5 - len(vL))     # pad values
            varS = vaL[0].strip(); valS = vaL[1].strip()
            unit1S, unit2S = vaL[2].strip(), vaL[3].strip()
            descripS = vaL[4].strip()
            if not len(varS):
                valL.append(['---------', ' ', ' ', ' '])    # totals
                continue
            val1U = val2U = array(eval(valS))
            if unit1S != "-": 
                if type(eval(valS)) == list: 
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS + "*" + unit1S
                    exec(cmdS, globals(), locals())
                    valU = eval(varS)                
                    val1U = str(valU.number()) + ' ' + str(valU.unit())
                    val2U = valU.cast_unit(eval(unit2S))
            valL.append([varS, val1U, val2U, descripS])
        hdrL = ["variable", "value", "[value]", "description"]
        alignL = ['left','right','right','left' ]            
        self._vtable(valL, hdrL, "rst", alignL)
        self.rivtD.update(locals()) 
 
    def _vdata(self, vL: list):
        """import data from files

        Args:
            vL (list): data command arguments
        """
        
        locals().update(self.rivtD)
        valL = [] 
        if len(vL) < 5: vL += [''] * (5 - len(vL))            # pad command                                                        
        valL.append(["variable", "values"])                   
        vfileS = Path(self.folderD["tpath"] / vL[2].strip())
        vecL = eval(vL[3].strip())
        with open(vfileS,'r') as csvF:
            reader = csv.reader(csvF)
        vL = list(reader)
        for i in vL:
            varS = i[0]; varL = array(i[1:])
            cmdS = varS + "=" + str(varL)
            exec(cmdS, globals(), locals())
            if len(varL) > 4: varL= str((varL[:2]).append(["..."]))
            valL.append([varS, varL])    
        hdrL = ["variable", "values"]
        alignL = ['left','right']            
        self._vtable(valL, hdrL, "rst", alignL)
        self.rivtD.update(locals()) 

    def _vsub(self, eqL: list, eqS: str):
        """substitute numbers for variables in printed output
        
        Args:
            epL (list): equation and units
            epS (str): [description]
        """

        locals().update(self.rivtd)

        eformat =""
        utfS = eqL[0].strip(); descripS = eqL[3]; parD = dict(eqL[1])
        varS = utfS.split("=")
        resultS = vars[0].strip() + " = " + str(eval(vars[1]))
        try: 
            eqS = "Eq(" + eqL[0] +",(" + eqL[1] +"))" 
            #sps = sps.encode('unicode-escape').decode()
            utfs = sp.pretty(sp.sympify(eqS, _clash2, evaluate=False))
            print(utfs); self.calcl.append(utfs)
        except:
            print(utfs); self.calcl.append(utfs)
        try:
            symeq = sp.sympify(eqS.strip())                                                 # substitute                            
            symat = symeq.atoms(sp.Symbol)
            for _n2 in symat:
                evlen = len((eval(_n2.__str__())).__str__())  # get var length
                new_var = str(_n2).rjust(evlen, '~')
                new_var = new_var.replace('_','|')
                symeq1 = symeq.subs(_n2, sp.Symbols(new_var))
            out2 = sp.pretty(symeq1, wrap_line=False)
            #print('out2a\n', out2)
            symat1 = symeq1.atoms(sp.Symbol)       # adjust character length
            for _n1 in symat1:                   
                orig_var = str(_n1).replace('~', '')
                orig_var = orig_var.replace('|', '_')
                try:
                    expr = eval((self.odict[orig_var][1]).split("=")[1])
                    if type(expr) == float:
                        form = '{:.' + eformat +'f}'
                        symeval1 = form.format(eval(str(expr)))
                    else:
                        symeval1 = eval(orig_var.__str__()).__str__()
                except:
                    symeval1 = eval(orig_var.__str__()).__str__()
                out2 = out2.replace(_n1.__str__(), symeval1)
            #print('out2b\n', out2)
            out3 = out2                         # clean up unicode 
            out3.replace('*', '\\u22C5') 
            #print('out3a\n', out3)
            _cnt = 0
            for _m in out3:
                if _m == '-':
                    _cnt += 1
                    continue
                else:
                    if _cnt > 1:
                        out3 = out3.replace('-'*_cnt, u'\u2014'*_cnt)
                    _cnt = 0
            #print('out3b \n', out3)
            self._write_utf(out3, 1, 0)         # print substituted form
            self._write_utf(" ", 0, 0)
        except:
            pass   

    def _vfunc(self, vL: list):
        pass

    def t_rst(self) -> tuple:
        """parse table-strings

        Return:
            calcS (list): utf formatted calc-string (appended)
            setsectD (dict): section settings
            setcmdD (dict): command settings
            rivtD (list): calculation values         
        """
        
        tcmdL = ["text", "table", "image"]
        tmethL = [self._itext, self._itable, self._iimage]
        ttagL =  ["[page]_", "[line]_", "[link]_", "[literal]_", "[foot]_", 
                "[s]", "[x]", "[r]_", "[c]_", "[e]_", "[t]_", "[f]_", "[#]_"] 
        
        self._parseUTF("table", tcmdL, tmethL, ttagL)
        
        return self.calcS, self.setsectD, self.setcmdD, self.rivtD