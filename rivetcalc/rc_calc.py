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
    
    def _refs(self, objnumI: int, setsectD: dict, typeS: str) -> str:
        """reference labels for equations, tables and figures

        Args:
            objnumI (int): equation, table or figure numbers
            setsectD (dict): section dictionary
            typeS (str): label type

        Returns:
            str: [description]
        """

        objfillS = str(objnumI).zfill(2)
        sfillS = str(setsectD["snum"]).strip().zfill(2)
        rnumS = str(setsectD["rnum"])
        refS = typeS + rnumS + "." + sfillS + "." + objfillS 

        return refS

    def _tags(self, tagS: str, calcS: str, setsectD: dict) -> str:
        """parse tag
        
        Args:
            tagS (str): line from rivet-string with included tag
        
        Tag list:
        [page]_                   {new doc page)
        [line]_                   {draw horizontal line)
        [cite]_  citation description
        [foot]_  footnote description
        [link]_  http:\\www.abc.org
        line of text   [r]_       {right justify line of text)
        line of text   [c]_       {center line of text)
        equation label [e]_       {right justify line of text with equation number)
        table title    [t]_       {right justify line of text with table number)
        """

        tagS = tagS.strip()
        if "[page]_" in tagS:
            utfS = int(setsectD["swidth"]) * "."
            print(utfS); calcS += utfS + "\n"
            return calcS, setsectD
        elif "[line]_" in tagS:
            utfS = int(setsectD["swidth"]) * '-'   
            print(utfS); calcS += utfS + "\n"
            return calcS, setsectD        
        elif "[link]_" in tagS:
            tgS = tagS.strip("[link]_").strip()
            utfS = "link: "+ tgS
            print(utfS); calcS += utfS + "\n"
            return calcS, setsectD
        elif "[r]_" in tagS:
            tagL = tagS.strip().split("[r]_")
            utfS = (tagL[0].strip()).rjust(int(setsectD["swidth"]-1))
            print(utfS); calcS += utfS + "\n"       
            return calcS, setsectD    
        elif "[c]_" in tagS:
            tagL = tagS.strip().split("[c]_")
            utfS = (tagL[0].strip()).rjust(int(setsectD["swidth"]-1))
            print(utfS); calcS += utfS + "\n"       
            return calcS, setsectD
        elif "[e]_" in tagS:
            tagL = tagS.strip().split("[e]_")
            enumI = int(setsectD["enum"]) + 1
            setsectD["enum"] = enumI
            refS = _refs(enumI, setsectD, "Equ: ")
            utfS = (tagL[0].strip() + " " + refS).rjust(int(setsectD["swidth"]-1))
            print(utfS); calcS += utfS + "\n"       
            return calcS, setsectD
        elif "[t]_" in tagS:
            tagL = tagS.strip().split("[t]_")
            tnumI = int(setsectD["tnum"]) + 1
            setsectD["tnum"] = tnumI
            refS = _refs(tnumI, setsectD, "Table: ")
            utfS = (tagL[0].strip() + " " + refS).rjust(int(setsectD["swidth"]-1))
            print(utfS); calcS += utfS + "\n"       
            return calcS, setsectD
        elif "[foot]_" in tagS:
            tagL = tagS.strip().split("]_")
            utfS = "[" + str(setsectD["ftqueL"].popleft()) + "] " + tagL[1].strip()
            print(utfS); calcS += utfS + "\n"
            return calcS, setsectD
        elif "[cite]_" in tagS:    
            tagL = tagS.strip().split("]_")
            utfS = "[" + str(setsectD["ctqueL"].popleft()) + "] " + tagL[1].strip()
            print(utfS); calcS += utfS + "\n"
            return calcS, setsectD
        else:
            return tagS, setsectD
    
    def _parseutf(self, typeS: str, cmdL: list, attrL: list, tagL: list ):
        """parse rivet-string

        Args:
            typeS (str): rivet-string type
            cmdL (list): command list
            attrL (list): attribute list
            tagL (list): tag list
        """
        
        usL = []; indxI = -1; blkflgB = False

        for uS in self.strL:
            if uS[0:2] == "##":  continue              # remove review comment
            uS = uS[4:]                                # remove indent
            try: 
                if uS[0] == "#" : continue             # remove comment 
                if uS[0:2] == "::" : continue          # remove preformat         
            except:
                print(" "); self.calcS += "\n"
                continue
            if blkflgB:
                if uS[0:2] == "||":
                    attrL[0](usL)
                    blkflgB = False
                    usL = []
                    usL.append(uS[2:].split("|"))    
                    indxI = cmdL.index(usL[0][0].strip())
                    attrL[indxI](usL)                 # call attribute                          
                    continue
                usL.append(uS.strip())
                continue
            if uS[0:2] == "||":
                usL = []
                usL.append(uS[2:].split("|"))
                indxI = cmdL.index(usL[0][0].strip()) 
                if usL[0][indxI].strip() == "image":       # check image block
                    blkflgB = True
                    continue
                attrL[indxI](usL)                     # call attribute                          
                continue
            if "]_" in uS:                              # process a tag
                if "[#]_" in uS:
                    uS = uS.replace("[#]_", "[" + 
                        str(self.setsectD["ftqueL"][-1]) + "]" )
                    print(uS); self.calcS += uS + "\n"
                    incrI = self.setsectD["ftqueL"][-1] + 1
                    self.setsectD["ftqueL"].append(incrI); continue
                chk = any(tag in tagL for tag in uS)
                if True in chk:
                    self.calcS, self.setsectD = self._tags(uS, self.calcS, self.setsectD)
                    continue 
                else:
                    utfS = uS.replace("]_","]")
                    print(utfS); self.calcS += utfS + "\n"
                    continue
            print(uS.rstrip()); self.calcS += uS.rstrip() + "\n"

    def r_utf(self) -> str:
        """ parse repository string
       
       Returns:
            calcS (list): utf formatted calc strings
            setsectD (dict): section settings
        """
        
        rcmdL = ["calc", "scope", "attach"]
        rtagL = ["[links]_", "[literal]_"]
        rattrL = [self._rcalc, self._rscope, self._rattach]
        
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
        itagL =  ["[page]_", "[line]_", "[link]_", "[cite]_", "[foot]_",   
                    "[r]_", "[c]_", "[t]_", "[f]_" ] 
        
        self._parseutf("insert", icmdL, iattrL, itagL)
        
        return self.calcS, self.setsectD, self.setcmdD

    def _ilatex(self,iL: list):
        """insert formated equation from LaTeX string
        
        Args:
            ipL (list): parameter list

        """
        try:
            scaleI = int(iL[0][2].strip)
        except:
            scaleI = self.setcmdD["scale1"]
        self.setcmdD.update({"scale1":scaleI})
        txS = iL[0][1].strip()
        #txs = txs.encode('unicode-escape').decode()
        ltxS = parse_latex(txS)
        utfS2 = sp.pretty(sp.sympify(ltxS, _clash2, evaluate=False))
        print(utfS2+"\n"); self.calcS += utfS2 + "\n"   

    def _isympy(self,iL):
        """insert formated equation from sympy string 
        
        Args:
            ipL (list): parameter list
        """
        try:
            scaleI = int(iL[0][2].strip())
        except:
            scaleI = self.setcmdD["scale1"]
        self.setcmdD.update({"scale1":scaleI})
        spS = iL[0][1].strip()
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
        try: 
           widthI = int(iL[0][2].strip())
        except:
            widthI = self.setcmdD["cwidth"]
        self.setcmdD.update({"cwidth": widthI})
        txtpath = Path(self.folderD["xpath"] /  iL[1].strip())
        with open(txtpath, 'r') as txtf1:
                utfL = txtf1.readlines()
        txtS = "".join(utfL)
        indI = int((80-widthI)/2)
        indS = " "*indI
        utfL = textwrap.wrap(txtS, width=widthI)
        utfL = [s+"\n" for s in utfL]
        utfS = indS + indS.join(utfL)
        print(utfS); self.calcS += utfS + "\n"

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

        vcmdL = ["values", "vector", "func", "table", "image"]
        attrL = [self._vvalues, self._vvector, self._vfunc, self._vformat, 
                                self._utable, self._uimage,]
        vtagL =  ["[page]_", "[line]_", "[link]_", "[cite]_", "[foot]_",   
                    "[r]_", "[c]_", "[t]_", "[f]_"] 

        self._parseutf("value", vcmdL, attrL, vtagL)

        """  df = pd.DataFrame(vsL)                      # write value table
        hdrL = ["variable", "value", "value" "description"]
        old_stdout = sys.stdout
        output = StringIO()
        output.write(tabulate(df, tablefmt="grid", headers=hdrL, showindex=False))            
        valueS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()
        print(valueS + "\n"); self.calcS += valueS + "\n" """

        self.rivetD.update(locals())
        return self.calcS, self.setsectD, self.setcmdD, self.rivetD, self.exportS
        
    def _vassign(self, vL: list):
        """assign values to variables
        
        Args:
            vL (list): list of values
        """
        
        locals().update(self.rivetD)

        pyS = """"""; valL =[]                              # values        
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
                trimL= tempS[:3]
                trimL.append("...")
                valS = str(trimL)
            else:
                valS = str(tempS)
        valL.append([varS, valS, descripS])

        self.rivetD.update(locals())
        self.exportS += pyS
        return(valL)        

    def _vvalues(self, vL: list):
        """read values from file
        
        Args:
            vL (list): list of values
        """
        
        locals().update(self.rivetD)

        pyS = """"""; valL =[]                   # value list for table
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
            pyS = str(varS + " = " + arrayS + "   # " + descripS + "\n")
            exec(cmdS, globals(), locals())
            tempS = cmdS.split("array")[1].strip()
            tempS = eval(tempS.strip("()"))
            if len(tempS) > 3:
                trimL= tempS[:3]
                trimL.append("...")
                valS = str(trimL)
            else:
                valS = str(tempS)
            valL.append([varS, valS, descripS])
        
        self.exportS += pyS
        self.rivetD.update(locals())                        # update rivetD
        return(valL)        

    def _vvector(self, vL: list):
        """read vector from file
        
        Args:
            vL (list): list of values
        """
        
        locals().update(self.rivetD)
        pyS = """"""; valL =[]                            # value list for table
        tfileS = Path(self.folderD["tpath"], vL[1].strip())
        varS = vL[2].split(":")[0].strip()
        vecS = vL[2].split(":")[1].strip()
        if "r" in vecS:
            veS = vecS.strip("r"); valL =[]
            with open(tfileS,'r') as csvf:
                reader = csv.reader(csvf)
                for row in range(int(veS)):
                    val = next(reader)
            valL = valL + list(val)
            arrayS = "array(" + str(valL) + ")"  
        if "c" in vecS:
            veS = vecS.strip("c"); valL =[]
            with open(tfileS,'r') as csvf:
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

    def _vfunc(self):
        pass

    def _vformat(self, eL):        
        eupL = eL[1].strip()
        eD = dict(i.split(":") for i in eupL.split(","))
        self.setcmdD.update(eD)

    def t_utf(self) -> tuple:
        """parse table-strings

        Return:
            calcS (list): utf formatted calc strings
            setsectD (dict): section settings
            setcmdD (dict): command settings
            rivetD (list): calculation values        
            
        """
        tcmdL = ["table", "image", ]
        attribL = [self._utable, self._uimage]
        ttagL =  ["[page]_", "[line]_", "[link]_", "[cite]_", "[foot]_",   
                        "[r]_", "[c]_", "[f]_","[t]" ] 
    
        self._parseutf("table", tcmdL, attrL, ttagL)
        
        return (self.calcS, self.setsectD, self.rivetD)

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
        fileS = iL[0][1].strip()
        tfileS = Path(self.folderD["tpath"], fileS)
        xfileS = Path(self.folderD["xpath"], fileS)  
        if ".csv" in iL[0][1]:                        # csv file       
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
        elif ".rst" in iL[0][1]:                      # rst file
            with open(xfileS,'r') as rst: 
                utfS = rst.read()
            titleS = "  \n"
            try: titleS = iL[0][2].strip() + titleS
            except: pass
        else:                                         # inline reST table 
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


