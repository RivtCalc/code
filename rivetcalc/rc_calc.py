#! python
"""transform model-string to calc-string

The ParseUTF class converts model-strings to calc-string.
Model-strings must be indented 4 spaces. Commands start with
a double bar (||) and are single line, except where noted. Tags
are included inline, with the associated text.
"""

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
from numpy import *
from rivetcalc.rc_unit import *
from io import StringIO
from sympy.parsing.latex import parse_latex
from sympy.abc import _clash2
from tabulate import tabulate 
from pathlib import Path

logging.getLogger("numexpr").setLevel(logging.WARNING)

class ParseUTF:
    """transform model-string to calc-string

    """
    
    def __init__(self, strL: list, folderD: dict, setcmdD: dict,
         setsectD: dict, rivetD: dict, exportS: str):
        
        """transform model-string to calc-string

        The ParseUTF class converts model-strings to calc-string.
        Model-strings must be indented 4 spaces. Commands start with
        a double bar (||) and are single line, except where noted. Tags
        are included inline, with the associated text.
        
        Args:
            exportS (str): exportS
            strL (list): strL
            folderD (dict): folderD
            setsectD (dict): setsectD
            setcmdD (dict): setcmdD
            rivetD (dict): rivetD
        """
    
        self.calcS = """"""
        self.exportS = exportS
        self.strL = strL
        self.folderD = folderD
        self.setsectD = setsectD
        self.setcmdD = setcmdD
        self.rivetD = rivetD
    
    def _refs(self, objnumI: int, typeS: str) -> str:
        """reference labels for equations, tables and figures

        Args:
            objnumI (int): equation, table or figure numbers
            setsectD (dict): section dictionary
            typeS (str): label type

        Returns:
            str: [description]
        """

        objfillS = str(objnumI).zfill(2)
        sfillS = str(self.setsectD["snum"]).strip().zfill(2)
        rnumS = str(self.setsectD["rnum"])
        refS = typeS + rnumS + "." + sfillS + "." + objfillS 

        return refS

    def _tags(self, tagS: str, tagL: list) -> tuple:
        """parse tag
        
        Args:
            tagS (str): rivet-string with tag
            tagL (list): list of tags for string type
            setsectD (dict): section dictionary
            
        Return:
            uS (str): utf string 
            setsectD (dict): section dictinoary
        """

        tagS = tagS.rstrip()
        for tag in tagL:
            if tag in tagS:
                if tag == "[page]_":
                    uS = int(self.setsectD["swidth"]) * "." ; break
                elif tag == "[line]_":
                    uS = int(self.setsectD["swidth"]) * '-' ; break   
                elif tag == "[link]_":
                    tgS = tagS.strip("[link]_").strip()
                    uS = "link: "+ tgS ; break
                elif tag == "[literal]_":
                    uS = "" ; break
                elif tag == "[r]_":
                    tagL = tagS.strip().split("[r]_")
                    uS = (tagL[0].strip()).rjust(int(self.setsectD["swidth"]-1))
                    break
                elif tag ==  "[c]_":
                    tagL = tagS.strip().split("[c]_")
                    uS = (tagL[0].strip()).rjust(int(self.setsectD["swidth"]-1))
                    break
                elif tag == "[f]_":
                    tagL = tagS.strip().split("[e]_")
                    enumI = int(self.setsectD["enum"]) + 1
                    self.setsectD["enum"] = enumI
                    refS = self._refs(enumI, "[ Figure: ")
                    uS = (tagL[0].strip() + " " + refS + " ]").rjust(int(self.setsectD["swidth"]-1))
                    break
                elif tag == "[e]_":
                    tagL = tagS.strip().split("[e]_")
                    enumI = int(self.setsectD["enum"]) + 1
                    self.setsectD["enum"] = enumI
                    refS = self._refs(enumI, "[ Equ: ")
                    uS = (tagL[0].strip() + " " + refS + " ]").rjust(int(self.setsectD["swidth"]-1))
                    break
                elif tag == "[t]_":
                    tagL = tagS.strip().split("[t]_")
                    tnumI = int(self.setsectD["tnum"]) + 1
                    self.setsectD["tnum"] = tnumI
                    refS = self._refs(tnumI, "[ Table: ")
                    uS = (tagL[0].strip() + " " + refS + " ]").rjust(int(self.setsectD["swidth"]-1))
                    break
                elif tag == "[#]_":
                    uS = uS.replace("[#]_", "[" + str(self.setsectD["ftqueL"][-1]) + "]")
                    incrI = self.setsectD["ftqueL"][-1] + 1
                    self.setsectD["ftqueL"].append(incrI)
                    break
                elif tag == "[foot]_":
                    tagL = tagS.strip().split("]_")
                    uS = "[" + str(self.setsectD["ftqueL"].popleft()) + "] " + tagL[1].strip()
                    break
                elif tag == "[cite]_":    
                    tagL = tagS.strip().split("]_")
                    uS = "[" + str(self.setsectD["ctqueL"].popleft()) + "] " + tagL[1].strip()
                    break
                else:
                    pass
            else:
                uS = tagS
        return uS, self.setsectD
    
    def _parseutf(self, typeS: str, cmdL: list, attrL: list, tagL: list ):
        """parse rivet-string`

        Args:
            typeS (str): rivet-string type
            cmdL (list): command list
            attrL (list): attribute list
            tagL (list): tag list
        """
        uL = []            # command arguments
        indxI = -1         # attribute index
        uvL = []           # value list 

        for uS in self.strL:
            if uS[0:2] == "##":  continue              # remove review comment
            uS = uS[4:]                                # remove indent
            try: 
                if uS[0] == "#" : continue             # remove comment 
                if uS[0:2] == "::" : continue          # remove preformat         
            except:
                print(" "); self.calcS += "\n"
                continue
            if uS[0:2] == "||":                        # command
                uL = uS[2:].split("|")
                indxI = cmdL.index(uL[0].strip()) 
                attrL[indxI](uL)                      # call attribute                          
                continue
            if "]_" in uS:                             # call tag
                uS, self.setsectD = self._tags(uS, tagL)     
            if typeS == "values":
                if "=" in uS:
                    uL = uS[2:].split("|")
                    if uL[1].strip == "s": uL.insert(0,"symbol")
                    elif uL[1].strip == "r": uL.insert(0,"replace")
                    elif uL[1].strip == "t": uL.insert(0,"table")
                    else: 
                        uvL.append(uL)
                        continue
                    self._vassign(uL); uvL = []
            if len(uvL) > 0 : 
                self._vassign(uL); uvL = []                   
            print(uS.rstrip()); self.calcS += uS.rstrip() + "\n"

    def r_utf(self) -> str:
        """ parse repository string
       
       Returns:
            calcS (list): utf formatted calc strings
            setsectD (dict): section settings
        """
        
        rcmdL = ["calc", "scope", "attach"]
        rattrL = [self._rcalc, self._rscope, self._rattach]
        rtagL = ["[links]_", "[literal]_", "[foot]_", "[cite]_", "[#]_"]
        
        self._parseutf("repo", rcmdL, rattrL, rtagL)
        
        return self.calcS, self.setsectD

    def _rcalc(self, rsL):
        c = 2

    def _rscope(self, rsL):
        a = 4
    
    def _rattach(self, rsL):
        b = 5
    
    def i_utf(self) -> tuple:                
        """ parse insert-string
       
        Returns:
            calcS (list): utf formatted calc strings
            setsectD (dict): section settings
            setcmdD (dict): command settings
        """

        icmdL = ["text", "sym", "tex", "table", "image"]
        iattrL = [self._itext, self._isympy, self._ilatex, 
                            self._utable, self._uimage, ]
        itagL =  ["[page]_", "[line]_", "[link]_", "[literal]_", "[cite]_",
            "[foot]_", "[#]_", "[r]_", "[c]_", "[e]_", "[t]_", "[f]_"] 
        
        self._parseutf("insert", icmdL, iattrL, itagL)
        
        return self.calcS, self.setsectD, self.setcmdD

    def _ilatex(self,iL: list):
        """insert formated equation from LaTeX string
        
        Args:
            ipL (list): parameter list

        """
        try:
            scaleI = int(iL[2].strip)
        except:
            scaleI = self.setcmdD["scale1"]
        self.setcmdD.update({"scale1":scaleI})
        txS = iL[1].strip()
        #txs = txs.encode('unicode-escape').decode()
        ptxS = parse_latex(txS)
        utfS2 = sp.pretty(sp.sympify(ptxS, _clash2, evaluate=False))
        print(utfS2+"\n"); self.calcS += utfS2 + "\n"   

    def _isympy(self,iL):
        """insert formated equation from sympy string 
        
        Args:
            ipL (list): parameter list
        """
        try:
            scaleI = int(iL[2].strip())
        except:
            scaleI = self.setcmdD["scale1"]
        self.setcmdD.update({"scale1":scaleI})
        spS = iL[1].strip()
        spL = spS.split("=")
        spS = "Eq(" + spL[0] +",(" + spL[1] +"))" 
        #sps = sps.encode('unicode-escape').decode()
        utfS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        print(utfS); self.calcS += utfS + "\n"   
            
    def _itext(self, iL: list):
        """insert text from file
        
        Args:
            iL (list): text command list
        """
        wrapB = 1
        if iL[2].strip() == "*":
            wrapB = 0
        elif isinstance(iL[2].strip(), int):
            widthI = int(iL[2].strip())
            self.setcmdD.update({"cwidth": widthI})
        else:
            widthI = self.setcmdD["cwidth"]
        txtpath = Path(self.folderD["xpath"]/iL[1].strip())
        with open(txtpath, 'r') as txtf1:
                uL = txtf1.readlines()
        txtS = "".join(uL)
        if wrapB:
            inxI = int((80-widthI)/2)
            inS = " "*inxI
            uL = textwrap.wrap(txtS, width=widthI)
            uL = [s+"\n" for s in uL]
            uS = inS + inS.join(uL)
        else:
            uS = txtS
        print(uS); self.calcS += uS + "\n"

    def v_utf(self)-> tuple:
        """parse value-string

        Return:
            calcS (list): utf formatted calc strings
            setsectD (dict): section settings
            setcmdD (dict): command settings
            rivetD (list): calculation values
            exportS (list): value strings for export
         """

        locals().update(self.rivetD)

        vcmdL = ["value", "vector", "func", "format", "table", "image"]
        attrL = [self._vassign, self._vvector, self._vfunc, self._vformat,
                                self._utable, self._uimage,]
        vtagL =  ["[page]_", "[line]_", "[link]_", "[cite]_", "[foot]_",   
                "[r]_", "[c]_", "[t]_", "[e]_", "[f]_", "[x]_"] 

        self._parseutf("values", vcmdL, attrL, vtagL)

        self.rivetD.update(locals())
        return self.calcS, self.setsectD, self.setcmdD, self.rivetD, self.exportS
        
    def _vformat(self, vL: list):        
        self.setcmdD["tres"] = vL[1].split(",")[0].strip()
        self.setcmdD["ttrm"] = vL[1].split(",")[1].strip()
        
    def _vassign(self, vL: list):
        """assign values to variables
        
        Args:
            vL (list): list of values
        """
        
        locals().update(self.rivetD)

        pyS = """"""; valL = []                                    
        if vL[0] in ["s","r","t"]:                              # equations
            descripS = vL[1].strip()
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            arrayS = "array(" + valS + ")"
            cmdS = str(varS + " = " + arrayS)
            pyS = str.ljust(varS + " = " + arrayS, 40) + " # " + descripS + "\n"
            exec(cmdS, globals(), locals())
            tempS = cmdS.split("array")[1].strip()
            tempS = eval(tempS.strip("())"))
            if type(tempS) == list:
                if len(eval(varS)) > 3:
                    trimL= tempS[:3]; trimL.append("...")
                    valS = str(trimL)
                else:
                    valS = str(tempS)
            valL.append([varS, valS, descripS])
        elif vL[0].strip() == "value":                           # value file
            tfileS = Path(self.folderD["spath"], vL[1].strip())
            with open(tfileS,'r') as pyfile:
                readL = pyfile.readlines()
            for v in readL:
                vS = v.split("#")
                varS = vS[0].split("=")[0].strip()
                valS = vS[0].split("=")[1].strip()
                arrayS = "array(" + valS + ")"                
                descripS = vS[1].strip()
                cmdS = str(varS + " = " + arrayS)
                exec(cmdS, globals(), locals())
                tempS = cmdS.split("array")[1].strip()
                tempS = eval(tempS.strip("()"))
            if type(tempS) == list:
                if len(eval(varS)) > 3:
                    trimL= tempS[:3]
                    trimL.append("...")
                    valS = str(trimL)
                else:
                    valS = str(tempS)
                valL.append([varS, valS, descripS])
            try:
                if len(vL[0]) > 0:                       # value strings
                    pass
            except:
                    pass
        df = pd.DataFrame(valL)                            # write value table
        hdrL = ["variable", "value", "value" "description"]
        old_stdout = sys.stdout
        output = StringIO()
        output.write(tabulate(df, tablefmt="grid", headers=hdrL, showindex=False))            
        valS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        self.exportS += pyS
        self.rivetD.update(locals())                        
        print(valS.rstrip()); self.calcS += valS.rstrip() + "\n"
    
    def _vsymbol(self, eL: list):
        """[summary]
    
        Args:
            eL (list): list of equation plus parameters
        
        """
        locals().update(self.rivetD)
        
        eS =""""""
        eqS = eL[0].strip()
        varS = eqS.split("=")[1].strip()
        resultS = eqS.split("=")[0].strip()
        spS = "Eq(" + resultS + ",(" + varS + "))" 
        #sps = sps.encode('unicode-escape').decode()
        try: utfS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        except: pass
        print(utfS); self.calcS += utfS + "\n"

        self.rivetD.update(locals())   

    def _vsub(self, epl: list, eps: str):
        """process equations and substitute variables
        
        Args:
            epl (list): [description]
            eps (str): [description]
        """

        locals().update(self.rivetd)
        utfs = epl[0].strip(); descrips = epl[3]; pard = dict(epl[1])
        vars = utfs.split("=")
        results = vars[0].strip() + " = " + str(eval(vars[1]))
        try: 
            eps = "Eq(" + epl[0] +",(" + epl[1] +"))" 
            #sps = sps.encode('unicode-escape').decode()
            utfs = sp.pretty(sp.sympify(eps, _clash2, evaluate=False))
            print(utfs); self.calcl.append(utfs)
        except:
            print(utfs); self.calcl.append(utfs)
        try:
            symeq = sp.sympify(eps.strip())                                                 # substitute                            
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

    def _vvector(self, vL: list):
        """read vector from file
        
        Args:
            vL (list): list of values
        """
        
        locals().update(self.rivetD)
        pyS = """"""; valL =[]                            # value list for table
        vfileS = Path(self.folderD["tpath"], vL[1].strip())
        varS = vL[3].strip()
        vecS = vL[2].strip()
        if "r" in vecS:
            veS = vecS.strip("r"); valL =[]
            with open(vfileS,'r') as csvf:
                reader = csv.reader(csvf)
                for row in range(int(veS)):
                    val = next(reader)
            valL = valL + list(val)
            arrayS = "array(" + str(valL) + ")"  
        if "c" in vecS:
            veS = vecS.strip("c"); valL =[]
            with open(vfileS,'r') as csvf:
                reader = csv.reader(csvf)
                for row in reader:
                    valL.append(row[int(veS)])
            arrayS = "array(" + str(valL) + ")"  
        cmdS = varS + "=" + arrayS
        exec(cmdS, globals(), locals())
        pyS = cmdS
        tempS = cmdS.split("array")[1].strip()
        tempS = eval(tempS.strip("()"))
        if len(tempS) > 3:
            trimL= tempS[:3]
            trimL.append(["..."])
            valS = str(trimL)
        else:
            valS = str(tempS)
        
        descripS = "vector from " + vL[1].strip()
        self.exportS += pyS
        self.rivetD.update(locals())                        # update rivetD
        return([[varS, valS, descripS]])        
    
    def t_utf(self) -> tuple:
        """parse table-strings

        Return:
            calcS (list): utf formatted calc strings
            setsectD (dict): section settings
            setcmdD (dict): command settings
            rivetD (list): calculation values         
        """
        tcmdL = ["table", "image", ]
        attrL = [self._utable, self._uimage]
        ttagL =  ["[page]_", "[line]_", "[link]_", 
                "[cite]_", "[foot]_", "[f]_","[t]" ] 
    
        self._parseutf("table", tcmdL, attrL, ttagL)
        
        return self.calcS, self.setsectD, self.setcmdD, self.rivetD

    def _utable(self, iL: list):
        """insert table from inline or csv, rst file 
        
        Args:
            ipl (list): parameter list
        """       
        try:
            widthI = int(iL[0][2].strip())
        except:
            widthI = int(self.setcmdD["cwidth"])

        self.setcmdD.update({"cwidth":widthI})
        tableS = ""; utfS = ""
        fileS = iL[1].strip()
        tfileS = Path(self.folderD["tpath"], fileS)
        xfileS = Path(self.folderD["xpath"], fileS)  
        if ".csv" in iL[1]:                        # csv file       
            format1 = []
            with open(tfileS,'r') as csvfile:
                readL = list(csv.reader(csvfile))
            for row in readL:
                wrow=[]
                for i in row:
                    templist = textwrap.wrap(i, widthI) 
                    wrow.append("""\n""".join(templist))
                format1.append(wrow)
            sys.stdout.flush()
            old_stdout = sys.stdout
            output = StringIO()
            output.write(tabulate(format1, tablefmt="grid", headers="firstrow"))            
            utfS = output.getvalue()
            titleS = "  \n"
            sys.stdout = old_stdout
            try: titleS = iL[0][2].strip() + titleS
            except: pass        
        else:                                       
            utfS = ""
            titleS = "  "
            try: titleS = iL[0][2].strip() + titleS
            except: pass
        print(utfS); self.calcS += utfS + "\n"  

    def _uimage(self, iL: list):
        """insert image from file
        
        Args:
            ipl (list): parameter list
        """
        try:
            scaleI = int(iL[3].strip)
        except:
            scaleI = self.setcmdD["scale1"]
        self.setcmdD.update({"scale1":scaleI})
        self.setsectD["fnum"] += 1
        figI = self.setsectD["fnum"]
        sectI = self.setsectD["snum"]
        fileS = iL[0][1].strip()
        try:
            captionS = iL[0][2].strip()
            imgpaths = str(Path(self.folderD["fpath"], fileS))
            imgpathS = str(Path(*Path(imgpaths).parts[-5:]))
            utfS = ("Figure " + str(sectI) + '.' + str(figI) + "  "  
               + captionS + "\npath: " + imgpathS + "\n")
        except:
            imgpaths = str(Path(self.folderD["fpath"], fileS))
            imgpathS = str(Path(*Path(imgpaths).parts[-5:]))
            utfS = ("Figure: " + imgpathS + "\n")
        print(utfS); self.calcS += utfS + "\n"

        """       
                try:                                 # update default scale
                scaleL= iL[3].split(",")
                scale1I = int(scaleL[0].strip())
                scale1I = int(scaleL[0].strip())
                self.setcmdD.update({"scale1":scale1I})
                self.setcmdD.update({"scale2":scale2I})
            except:
                scale1I = self.setcmdD["scale1"]
                scale2I = self.setcmdD["scale2"]
            self.setsectD["fnum"] += 1                     # image 1
            figI = self.setsectD["fnum"]
            sectI = self.setsectD["snum"]
            fileS = iL[1].strip()
            captionS = iL[3].strip()
            imgP = str(Path(self.folderD["fpath"], fileS))
            utfS = ("Figure " + str(sectI) + '.' + str(figI) + "  "  
                + captionS + "\npath: " + imgP)
            print(utfS); self.calcS += utfS + "\n"

            self.setsectD["fnum"] += 1                     # image 2
            figI = self.setsectD["fnum"]
            sectI = self.setsectD["snum"]
            fileS = iL[2].strip()
            captionS = iL[4].strip()
            imgP = str(Path(self.folderD["fpath"], fileS))
            utfS = ("Figure " + str(sectI) + '.' + str(figI) + "  "  
                + captionS + "\npath: " + imgP)
            print(utfS); self.calcS += utfS + "\n"
        """


