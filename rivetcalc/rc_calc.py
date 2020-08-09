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
from IPython.display import display as _display
from IPython.display import Image as _Image
from io import StringIO
from sympy.parsing.latex import parse_latex
from sympy.abc import _clash2
from tabulate import tabulate 
from pathlib import Path
from numpy import *
from rivetcalc.rc_unit import *

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
        self.valL = []
    
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
        if "]__" in tagS:   
            if "[#]__" in tagS:                 # auto increment footnote mark                    
                uS = tagS.replace("[#]__", "[" + 
                            str(self.setsectD["ftqueL"][-1]) + "]")
                incrI = self.setsectD["ftqueL"][-1] + 1
                self.setsectD["ftqueL"].append(incrI)
            else:                               # citation mark
                indxstrtI = tagS.index("[")
                indxendI = tagS.index("]__")
                uS = tagS[indxstrtI:indxendI]
                self.setsectD["ctqueL"].append(uS)
        else:
            for tag in tagL:
                if tag in tagS:
                    if tag == "[page]_":        # new page
                        uS = int(self.setsectD["swidth"]) * "." ; break
                    elif tag == "[line]_":      # horizontal line
                        uS = int(self.setsectD["swidth"]) * '-' ; break   
                    elif tag == "[link]_":      # url link
                        tgS = tagS.strip("[link]_").strip()
                        uS = "link: "+ tgS ; break
                    elif tag == "[literal]_":   # literal text
                        uS = "" ; break
                    elif tag == "[r]_":         # right adjust text
                        tagL = tagS.strip().split("[r]_")
                        uS = (tagL[0].strip()).rjust(
                                    int(self.setsectD["swidth"]-1)); break
                    elif tag ==  "[c]_":        # center text  
                        tagL = tagS.strip().split("[c]_")
                        uS = (tagL[0].strip()).rjust(
                                    int(self.setsectD["swidth"]-1)); break
                    elif tag == "[f]_":         # figure label
                        tagL = tagS.strip().split("[e]_")
                        enumI = int(self.setsectD["enum"]) + 1
                        self.setsectD["enum"] = enumI
                        refS = self._refs(enumI, "[ Figure: ")
                        uS = (tagL[0].strip("[f]_") + " " + refS + " ]").rjust(
                                    int(self.setsectD["swidth"]-1)); break
                    elif tag == "[e]_":         # equation label
                        tagL = tagS.strip().split("[e]_")
                        enumI = int(self.setsectD["enum"]) + 1
                        self.setsectD["enum"] = enumI
                        refS = self._refs(enumI, "[ Equ: ")
                        uS = (tagL[0].strip() + " " + refS + " ]").rjust(
                                    int(self.setsectD["swidth"]-1)); break
                    elif tag == "[t]_":         # table label
                        tagL = tagS.strip().split("[t]_")
                        tnumI = int(self.setsectD["tnum"]) + 1
                        self.setsectD["tnum"] = tnumI
                        refS = self._refs(tnumI, "[ Table: ")
                        uS = (tagL[0].strip() + " " + refS + " ]").rjust(
                                    int(self.setsectD["swidth"]-1)); break
                    elif tag == "[foot]_":      # footnote label
                        tagL = tagS.strip().split("]_")
                        uS = "[" + str(self.setsectD["ftqueL"].popleft()
                                        ) +  "] " + tagL[1].strip(); break
                    elif tag == "[cite]_":      # citation label   
                        tagL = tagS.strip().split("]_")
                        uS = "[" + str(self.setsectD["ctqueL"].popleft()
                                        ) + "] " + tagL[1].strip(); break
                else:
                    uS = tagS

        return uS, self.setsectD
    
    def _parseutf(self, typeS: str, cmdL: list, methL: list, tagL: list ):
        """parse rivet-string`

        Args:
            typeS (str): rivet-string type
            cmdL (list): command list
            methL (list): method list
            tagL (list): tag list
        """
        uL = []                     # command arguments
        indxI = -1                  # method index
        _rgx = r'\[([^\]]+)]_'      # tags

        for uS in self.strL:                       
            if uS[0:2] == "##":  continue           # remove review comment
            uS = uS[4:]                             # remove indent
            if len(uS) == 0 : uS = " "
            try: 
                if uS[0] == "#" : continue          # remove comment 
                if uS[0:2] == "::" : continue       # remove preformat         
            except:
                print(" "); self.calcS += "\n"
                continue
            if re.search(_rgx, uS):                 # check for tag
                uS, self.setsectD = self._tags(uS, tagL)
                print(uS.rstrip()); self.calcS += uS.rstrip() + "\n"
                continue     
            if typeS == "value":
                self.setcmdD["saveB"] = False  
                if "=" in uS:
                    if uS.strip()[-2] == "||":      # write value to file
                        uS = uS.replace("||"," ")
                        self.setcmdD["saveB"] = True                      
                    uL = uS.split('|')
                    self._vassign(uL)
                    continue
                if len(uS.strip()) == 0:            # blank line - write table
                    if len(self.valL) > 0: self._vtable()
                    self.valL = []
                    print(uS.rstrip(" ")); self.calcS += " \n"
                    continue
            if typeS == "table":
                pass
            if uS[0:2] == "||":                     # command
                uL = uS[2:].split("|")
                indxI = cmdL.index(uL[0].strip())
                #print(typeS, indxI) 
                methL[indxI](uL)                    # call attribute                          
                continue

            print(uS.rstrip()); self.calcS += uS.rstrip() + "\n"

    def r_utf(self) -> str:
        """ parse repository string
       
       Returns:
            calcS (list): utf formatted calc-string (appended)
            setsectD (dict): section settings
        """
        rcmdL = ["header", "codes", "scope", "attach"]
        rmethL = [self._rheader, self._rcodes, self._rscope, self._rattach]
        rtagL = ["[links]_", "[literal]_", "[foot]_", "[cite]_", "[#]__"]
        
        self._parseutf("repo", rcmdL, rmethL, rtagL)
        
        return self.calcS, self.setsectD

    def _rheader(self, rsL):
        c = 2
    
    def _rcodes(self, rsL):
        d = 2

    def _rscope(self, rsL):
        a = 4
    
    def _rattach(self, rsL):
        b = 5
    
    def i_utf(self) -> tuple:                
        """ parse insert-string
       
        Returns:
            calcS (list): utf formatted calc-string (appended)
            setsectD (dict): section settings
            setcmdD (dict): command settings
        """

        icmdL = ["text", "sym", "tex", "table", "image"]
        imethL = [self._itext, self._isympy, self._ilatex, 
                            self._itable, self._iimage, ]
        itagL =  ["[page]_", "[line]_", "[link]_", "[literal]_", "[cite]_",
            "[foot]_", "[r]_", "[c]_", "[e]_", "[t]_", "[f]_", "[#]__"] 
        
        self._parseutf("insert", icmdL, imethL, itagL)
        
        return self.calcS, self.setsectD, self.setcmdD

    def _ilatex(self,iL: list):
        """insert formated equation from LaTeX string
        
        Args:
            ipL (list): parameter list

        """
        try:
            scaleI = int(iL[2].strip)
        except:
            scaleI = self.setcmdD["scale1F"]
        self.setcmdD.update({"scale1F":scaleI})
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
            scaleI = self.setcmdD["scale1F"]
        self.setcmdD.update({"scale1F":scaleI})
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

    def _itable(self, iL: list):
        """insert table from csv file 
        
        Args:
            ipl (list): parameter list
        """       
        if len(iL) < 6: iL += [''] * (6 - len(iL))      # pad parameters
        utfS = ""; contentL = []; sumL = []
        fileS = iL[1].strip(); tfileS = Path(self.folderD["tpath"], fileS)
        if ".csv" in fileS:                             # read csv file       
            with open(tfileS,'r') as csvfile:
                readL = list(csv.reader(csvfile))
            if iL[2].strip():                           # max col width
                widthI = int(iL[2].strip())
                self.setcmdD.update({"cwidth":widthI})
            else:
                widthI = int(self.setcmdD["cwidth"])
            if iL[3].strip():                           # columns
                incl_colL =  eval(iL[3].strip())
                totalL = [""]*len(incl_colL)
            else: incl_colL = range(len(readL[0]))            
            if iL[4].strip():                           # column totals
                sumL = eval(iL[4].strip())
            if iL[5].strip():                           # total units
                colL = eval(iL[5].strip()) 
                unitL = [readL[1][i].strip() for i in colL]
                zipL = list(zip(colL,unitL))
                for i in zipL:
                    colI = incl_colL.index(i[0])
                    totalL[colI] = i[1]
                    totalL[0] = "Totals"
            for row in readL:
                contentL.append([row[i] for i in incl_colL])
            if sumL:
                sumF = 0.
                for colS in sumL:
                    for row in readL:
                        try: sumF += float(row[int(colS)])
                        except: pass
                    colI = int(incl_colL.index(colS))
                    totalL[colI] = sumF
                contentL.append(totalL)             
            wcontentL = []
            for rowL in contentL:
                wrowL=[]
                for iS in rowL:
                    templist = textwrap.wrap(iS, int(widthI)) 
                    wrowL.append("""\n""".join(templist))
                wcontentL.append(wrowL)
            sys.stdout.flush()
            old_stdout = sys.stdout
            output = StringIO()
            output.write(tabulate(wcontentL, tablefmt="grid", headers="firstrow"))            
            utfS = output.getvalue()
            sys.stdout = old_stdout
        else: pass
        
        print(utfS); self.calcS += utfS + "\n"  

    def _iimage(self, iL: list):
        """insert one or two images from file
        
        Args:
            ipl (list): image parameters
        """        
        imgflgI = 0
        if "," in iL[1]: imgflgI = 1                     # double image flag
        if imgflgI:
            scaleF = iL[2].split(",")
            scale1F = float(scaleF[0])
            scale2F = float(scaleF[1])
            self.setcmdD.update({"scale1F":scale1F})
            self.setcmdD.update({"scale2F":scale2F})
            self.setsectD["fnum"] += 1
            fig1I = self.setsectD["fnum"]                
            self.setsectD["fnum"] += 1
            fig2I = self.setsectD["fnum"]                
            fileS = iL[1].split(",")
            file1S = fileS[0].strip()
            file2S = fileS[1].strip()
            img1S = str(Path(self.folderD["fpath"] / file1S))
            img2S = str(Path(self.folderD["fpath"] / file1S))                
            pthshort1S = str(Path(*Path(img1S).parts[-4:]))
            pthshort2S = str(Path(*Path(img2S).parts[-4:]))
        else:
            scale1F = float(iL[2])
            self.setcmdD.update({"scale1F":scale1F})
            self.setsectD["fnum"] += 1
            fig1I = self.setsectD["fnum"]
            file1S = iL[1].strip()
            img1S = str(Path(self.folderD["fpath"] / file1S))
            pthshort1S = str(Path(*Path(img1S).parts[-4:]))
        
        _display(_Image(img1S))
        if imgflgI:  _display(_Image(img2S))
        uS = ("Figure path: " + pthshort1S + "\n")
        print(uS); self.calcS += uS + "\n"
        if imgflgI:    
            uS = ("Figure path: " + pthshort2S + "\n")
            print(uS); self.calcS += uS + "\n"

    def v_utf(self)-> tuple:
        """parse value-string

        Return:
            calcS (list): utf formatted calc-string (appended)
            setsectD (dict): section settings
            setcmdD (dict): command settings
            rivetD (list): calculation results
            exportS (list): value strings for export
         """

        locals().update(self.rivetD)

        vcmdL = ["value", "func", "text", 
                    "sym", "tex", "table", "image"]
        vmethL = [self._vvalues, self._vfunc, self._itext, 
                    self._isympy, self._ilatex, self._itable, self._iimage, ]
        vtagL =  ["[page]_", "[line]_", "[link]_", "[cite]_", "[foot]_",   
                      "[r]_", "[c]_", "[t]_", "[e]_", "[f]_", "[x]_"] 

        self._parseutf("value", vcmdL, vmethL, vtagL)

        self.rivetD.update(locals())
        return self.calcS, self.setsectD, self.setcmdD, self.rivetD, self.exportS

    def _vassign(self, vL: list):
        """assign values to variables
        
        Args:
            vL (list): list of assignments
        """
        
        locals().update(self.rivetD)
                                                        
        if len(vL) < 3:                             # equation
            self._vsymbol(vL)
        elif len(vL) > 2:                           # value
            descripS = vL[1].strip()
            unitL = vL[2].split(",")
            varS = vL[0].split("=")[0].strip()
            val1S = vL[0].split("=")[1].strip()
            val2S = vL[0].split("=")[1].strip()
            arrayS = "array(" + val1S + ")"
            cmdS = str(varS + " = " + arrayS)
            exec(cmdS, globals(), locals())
            tempS = cmdS.split("array(")[1].strip()
            tempS = eval(tempS.strip(")"))
            if type(tempS) == list:
                if len(eval(varS)) > 3:
                    trimL= tempS[:3]; trimL.append("...")
                    val1S = str(trimL)
                else:
                    val1S = str(tempS)
            self.valL.append([varS, val1S, val2S, descripS])          
            pyS = str.ljust(varS + " = " + arrayS, 40) + " # " + descripS + "\n"
            #print(pyS)
            if self.setcmdD["saveB"] == True:  self.exportS += pyS
        
        self.rivetD.update(locals())   

    def _vvalues(self, vL: list):
        """import values and set parameters

        Args:
            vL (list): value command arguments
        """
        locals().update(self.rivetD)
    
        if len(vL) < 5: vL += [''] * (5 - len(vL))                    # pad
        self.valL = []                                                # values
        if vL[1].strip() == "sub" or vL[1].strip() == "nosub":        # sub      
            self.setcmdD["values"] = vL[1].strip() 
            self.setcmdD["trmrI"] = vL[2].split(",")[0].strip()
            self.setcmdD["trmtI"] = vL[2].split(",")[1].strip()
        elif vL[1].strip() == "file":                                 # file
            vfileS = Path(self.folderD["tpath"] / vL[2].strip())
            with open(vfileS,'r') as csvfile:
                readL = list(csv.reader(csvfile))
            #print(f"{readL=}")
            for vaL in readL[1:]:                         # skip first line
                if len(vaL) < 5: vaL += [''] * (5 - len(vL))  # pad missing 
                varS = vaL[0].strip()
                valS = vaL[1].strip()
                descripS = vaL[2].strip()
                unit1S = vaL[3].strip()
                unit2S = vaL[4].strip()
                try: valU = unum.Unum.coerceToUnum(float(valS))
                except TypeError:
                    try: valU = unum.Unum.coerceToUnum(list(valS))
                    except:
                        raise TypeError
                if len(unit1S):
                    if valU.strUnit(): valS1 = valU.asUnit(eval(unit1S))
                    else: valU1 = valU*eval(unit1S)                                    
                valU2 = unum.Unum.coerceToUnum(valS)
                if len(unit2S): 
                    valU2 = valU1.asUnit(eval(unit2S))
                else:
                    valU2 = valU1
                if type(eval(valS)) == list:
                    if len(eval(valS)) > 3:
                        trimL= eval(valU1)[:3]
                        trimL.append("... " + unit1S)
                        valU1 = str(trimL)
                        trimL= eval(valU2)[:3]
                        trimL.append("... " + unit2S)
                        valU2 = str(trimL)
                    else: pass 
                self.valL.append([varS, valU1, valU2, descripS])
        elif vL[1].strip() == "list":                                  # list 
            vfileS = Path(self.folderD["tpath"] / vL[3].strip())
            vecS = vL[4].strip()
            varS = vL[5].strip()
            rL = []
            veS = vecS.strip("r")
            with open(vfileS,'r') as csvF:
                reader = csv.reader(csvF)
                for row in range(int(veS)): val = next(reader)
            rL = rL + list(val)
            arrayS = "array(" + str(rL) + ")"  
            cmdS = varS + "=" + arrayS
            exec(cmdS, globals(), locals())
            tempS = cmdS.split("array")[1].strip()
            tempS = eval(tempS.strip("()"))
            if len(tempS) > 3:
                trimL= tempS[:2]
                trimL.append(["..."])
                valS = str(trimL)
            else: valS = str(tempS)
            self.valL.append([varS, valS, valS, descripS])    
        else: pass            

        self.rivetD.update(locals()) 

    def _vtable(self):
        """write value table"""

        locals().update(self.rivetD)
    
        df = pd.DataFrame(self.valL)                            
        hdrL = ["variable", "value", "[value]", "description"]
        old_stdout = sys.stdout; output = StringIO()
        output.write(tabulate(df, tablefmt="grid", headers=hdrL, showindex=False))            
        valS = output.getvalue()
        sys.stdout = old_stdout; sys.stdout.flush()

        self.rivetD.update(locals())                        
        print(valS.rstrip()); self.calcS += valS.rstrip() + "\n"

    def _vsymbol(self, eL: list):
        """write symbolic equation
    
        Args:
            eL (list): equation and units
        """
        
        locals().update(self.rivetD)
        
        eqS = eL[0].strip()
        varS = eqS.split("=")[1].strip()
        resultS = eqS.split("=")[0].strip()
        spS = "Eq(" + resultS + ",(" + varS + "))" 
        #sps = sps.encode('unicode-escape').decode()
        try: utfS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        except: pass
        print(utfS); self.calcS += utfS + "\n"

        self.rivetD.update(locals())   

    def _vsub(self, eqL: list, eqS: str):
        """substitute numbers for variables in printed output
        
        Args:
            epL (list): equation and units
            epS (str): [description]
        """

        locals().update(self.rivetd)

        utfS = eql[0].strip(); descripS = eql[3]; parD = dict(eqL[1])
        varS = utfS.split("=")
        resultS = vars[0].strip() + " = " + str(eval(vars[1]))
        try: 
            epS = "Eq(" + epL[0] +",(" + epL[1] +"))" 
            #sps = sps.encode('unicode-escape').decode()
            utfs = sp.pretty(sp.sympify(eps, _clash2, evaluate=False))
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

    def t_utf(self) -> tuple:
        """parse table-strings

        Return:
            calcS (list): utf formatted calc-string (appended)
            setsectD (dict): section settings
            setcmdD (dict): command settings
            rivetD (list): calculation values         
        """
        tcmdL = ["table", "image", ]
        methL = [self._itable, self._iimage]
        ttagL =  ["[page]_", "[line]_", "[link]_", 
                "[cite]_", "[foot]_", "[f]_","[t]_" ] 
    
        self._parseutf("table", tcmdL, methL, ttagL)
        
        return self.calcS, self.setsectD, self.setcmdD, self.rivetD