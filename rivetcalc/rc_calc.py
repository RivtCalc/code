#! python
"""transform model-string to calc-string

A separate class transforms each model-string type to a utf-8 calc-string.
Commands within strings start with a double bar (||) in an indented (4 spaces)
and are single lines, except where noted as a block.

------- -------- ------ -------- --------------------------------------------
string  function  class  general
type     name      name   text            commands {comment}
------- -------- ------ -------- --------------------------------------------
Repo       R()   _R_utf   no     scope, attach, summary {block}
Insert     I()   _I_utf   yes    table, tex, sym, image {block}
Values     V()   _V_utf   yes    =, table, values, vector, image {block}
Equation   E()   _E_utf   yes    =, table, format, func, image {block}
Table      T()   _T_utf   no     table, image {blk}, {Python simple statement} 

Command syntax  
---------------
R(''' r-string defines repository and report data
    || summary | calc title | toc
    May include general text. Text is read until encountering the next
    command. The |toc argument generates a table of contents from section
    tags. The first paragraph is included in the Github README.rst file.
    
    || scope | discipline, object, state, intent, assembly, component 
    
    || attach | front | calccover.pdf         
    || attach | back | functions 
    || attach | back | docstrings
    || attach | back | appendix1.pdf 
    ''')

I(''' i-string inserts static text, tables and images  
    May include arbitrary text.
    
    || tex | \gamma = x + 3 # latex equation | 1. # image scale
    || sym | x = y/2 # sympy equation | 1.
    || table | x.txt | 60 # max paragraph width - characters 
    || table | x.csv | 60,[:] # max column width - characters, line range  
    || table | x.rst | [:] # line range

    || image | x.png {image file} | 1. {scale}
    figure caption
    ''')

V(''' v-string defines values
    May include arbitrary text that does not include an equal sign.

    x = 10.1*IN      | units, alt units  | description 

    || vector | x.csv | VECTORNAME r[n] {row in file to vector}
    || vector | x.csv | VECTORNAME c[n] {column in file to vector}    
    || values | vfile.py | [:] {assignment lines to read}
    || table | x.csv | 60    
    ''')

E(''' e-string defines equations
    May include arbitrary text that does not include an equal sign.

    || format | 2 {truncate result}, 2 {truncate terms}     

     x = v1 + 4*M               | units, alt units {applied to result}
     y = v2 / 4                 | units, alt units

    || func | x.py | func_name | units, alt  {import function from file}
    || table | x.csv | 60    
    || image | x.png | 1.
    ''') 

T('''t-string defines tables and plots
    May include any simple Python statement (single line). 

    || table | x.csv | 60    
    || image | x.png, y.jpg | 0.5,0.5
    figure1 caption
    figure2 caption
    ''')

--------------------- ----------- -------------------------------------------  
   Tag Syntax          Type          Comment           
--------------------- ----------- -------------------------------------------
[nn]_  section title   all           first line in string function
[page]_                all           start new doc page
[link]_  url           R,E,V,I       http link
[line]_                E,V,I,T       insert horizontal line
some text [abc123]_    E,V,I         citation
[cite]_  text          E,V,I         citation description (FIFO)    
some text [#]_         E,V,I         footnote autoincremented 
[foot]_  text          E,V,I         footnote description (FIFO)
figure caption [f]_    E,V,I         figure number autoincremented 
table title [t]_       E,V,I         table number autoincremented    
some text [r]_         E,V,I         right justify line
some text [c]_         E,V,I         center line
equation label [e]_    E             autoincremented equation number
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

def _refs(objnumI: int, setsectD: dict, typeS: str) -> str:
    """[summary]
    
    Args:
        refS (str): [description]
        setsectD (dict): [description]
        typeS (str): [description]
    
    Returns:
        str: [description]
    """

    objfillS = str(objnumI).zfill(2)
    sfillS = str(setsectD["snum"]).strip().zfill(2)
    rnumS = str(setsectD["rnum"])
    refS = "[" + typeS + rnumS + "." + sfillS + "." + objfillS + "]"

    return refS

def _tags(tagS: str, calcS: str, setsectD: dict) -> str:
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

class _R_utf:
    """transform Repository-string to calc-string

    Attributes:
        strL (list): rivet-strings
        folderD (dict): folder names
        sectD (dict): header information

    Commands: summary, scope, attach
    Tags: [nn]_, [page]_, [link]_
    """
    def __init__(self, strL :list, folderD :dict, setsectD :dict) -> str:
        self.calcS = """"""         # calc string
        self.strL = strL            # list of model strings
        self.folderD = folderD      
        self.setsectD = setsectD

    def r_parse(self) -> str:
        """ parse repository string
       
       Returns:
            calcS (list): utf formatted calc strings
            setsectD (dict): section settings
            setcmdD (dict): command settings
        """
        blkflgB = False; rsL = []; indxI = -1
        rcmdL = ["summary", "scope", "attach" ]
        attribL =  [self.r_summary, self.r_scope, self.r_attach]
        tagL =  ["[page]_", "[link]_" ] 
        
        for rS in self.strL:
            if rS[0:2] == "##":  continue               # remove review comment
            rS = rS[4:]                                 # remove indent
            try: 
                if rS[0] == "#" : continue              # remove comment 
                if rS[0:2] == "::" : continue           # remove preformat         
            except:
                print(" "); self.calcS += "\n"
            if blkflgB:
                if rS[0:2] == "||":
                    attribL[0](rsL)
                    blkflgB = False
                    rsL = []
                    rsL.append(rS[2:].split("|"))    
                    indxI = rcmdL.index(rsL[0][0].strip())    
                    attribL[indxI](rsL)                 # call attribute                          
                    continue
                rsL.append(rS.strip())
                continue
            if rS[0:2] == "||":
                rsL = []
                rsL.append(rS[2:].split("|"))
                indxI = rcmdL.index(rsL[0][0].strip())
                if rsL[0][indxI].strip() == "summary":   # check summary block
                    blkflgB = True
                    continue
            attribL[indxI](rsL)                          # call attribute                          
  
        return self.calcS, self.setsectD

    def r_summary(self, rsL, tagL):
        for utfS in rsL[1:]:
            chk = any(tgS in utfS for tgS in tagL)
            if True in chk:
                self.calcS, self.setsectD = _tags(utfS, self.calcS, self.setsectD)
                continue 
            elif "]_" in utfS:
                utfS = utfS.replace("]_","]")           # command not recognized
                print(utfS); self.calcS += utfS + "\n"
                continue
            else:
                print(utfS); self.calcS += utfS + "\n"

    def r_scope(self, rsL):
        pass
    
    def r_attach(self, rsL):
        pass

    def r_readme(self, rsL):
        pass
    
class _I_utf:  
    """convert Insert-string to utf-calc string 

    Attributes:
        strL (list): rivet-string
        folderD (dict): folder structure
        sectD (dict):  header information
        cmdD (dict): command settings

    Commands: tex, sym, table, image
    Tags: all except [e]_
    """

    def __init__(self, strL: list, folderD: dict, setcmdD: dict, setsectD: dict):
        self.calcS = """"""             # calc string
        self.strL = strL                # list of model strings
        self.folderD = folderD
        self.setsectD = setsectD
        self.setcmdD = setcmdD

    def i_parse(self) -> tuple:
        """ parse insert-string
       
       Returns:
            tuple :  calc str, section dict, command dict
        """
        blkflgB = False; isL = []; indxI = -1
        icmdL = ["table","sym", "tex", "image"]
        attribL = [self.i_table, self.i_sympy, self.i_latex, self.i_image]
        tagL =  ["[page]_", "[line]_", "[link]_", "[cite]_", "[foot]_",   
                    "[r]_", "[c]_", "[t]_", "[f]_", "[#]_" ] 
                
        for iS in self.strL:
            if iS[0:2] == "##":  continue              # remove review comment
            iS = iS[4:]                                # remove indent
            try: 
                if iS[0] == "#" : continue             # remove comment 
                if iS[0:2] == "::" : continue          # remove preformat         
            except:
                print(" "); self.calcS += "\n"
                continue
            if blkflgB:
                if iS[0:2] == "||":
                    attribL[0](isL)
                    blkflgB = False
                    isL = []
                    isL.append(iS[2:].split("|"))    
                    indxI = icmdL.index(isL[0][0].strip())
                    attribL[indxI](isL)                 # call attribute                          
                    continue
                isL.append(iS.strip())
                continue
            if iS[0:2] == "||":
                isL = []
                isL.append(iS[2:].split("|"))
                indxI = icmdL.index(isL[0][0].strip()) 
                if isL[0][indxI].strip() == "image":       # check image block
                    blkflgB = True
                    continue
                attribL[indxI](isL)                     # call attribute                          
                continue
            if "]_" in iS:                              # process a tag
                if "[#]_" in iS:
                    iS = iS.replace("[#]_", "[" + 
                        str(self.setsectD["ftqueL"][-1]) + "]" )
                    print(iS); self.calcS += iS + "\n"
                    incrI = self.setsectD["ftqueL"][-1] + 1
                    self.setsectD["ftqueL"].append(incrI); continue
                chk = any(tag in tagL for tag in iS)
                if True in chk:
                    self.calcS, self.setsectD = _tags(vS, self.calcS, self.setsectD)
                    continue 
                else:
                    utfS = vS.replace("]_","]")
                    print(utfS); self.calcS += utfS + "\n"
                    continue
            print(iS.rstrip()); self.calcS += iS.rstrip() + "\n"

        return self.calcS, self.setsectD, self.setcmdD 

    def i_latex(self,iL: list):
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

    def i_sympy(self,iL):
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
            
    def i_image(self, iL: list):
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
            try:                                        # update default scale
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

    def i_table(self, iL: list):
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

    def i_text(self, iL: list):
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

class _V_utf:
    """convert Value-string to utf-calc string
        
    Attributes:
        strL (list): rivet strings
        exportS (string) : values for export
        folderD (dict): folder structure
        setsectD (dict): section settings
        setcmdD (dict): command settings
        rivetD (dict) : rivet calculation variables

    Commands: tex, sym, table, image
    Tags: all except [e]_
    """
 
    def __init__(self, strL: list, folderD: dict, setcmdD: dict,
                setsectD: dict, rivetD: dict, exportS: str):
        """convert value-string to utf-calc string
        
        """
        self.calcS = """"""
        self.exportS = exportS
        self.strL = strL
        self.folderD = folderD
        self.setsectD = setsectD
        self.setcmdD = setcmdD
        self.rivetD = rivetD

    def v_parse(self)-> tuple:
        """parse strings of type value

        Return:
            calcS (list): utf formatted calc strings
            exportS (list): value strings for export
            rivetD (list): calculation values
            setsectD (dict): section settings
            setcmdD (dict): command settings
         """

        blkflgB = False; vsL = []; indxI = -1
        vcmdL = ["image", "values", "vector", "table"]
        attribL = [self.v_image, self.v_values, self.v_vector, self.v_table]
        tagL =  ["[page]_", "[line]_", "[link]_", "[cite]_", "[foot]_",   
                    "[r]_", "[c]_","[t]_", "[f]_", "[#]_" ] 

        locals().update(self.rivetD)

        for vS in self.strL:
            if vS[0:2] == "##":  continue              # remove review comment
            vS = vS[4:]                                # remove indent
            try: 
                if vS[0] == "#" : continue             # remove comment 
                if vS[0:2] == "::" : continue          # remove preformat         
            except:
                print(" "); self.calcS += "\n"
                continue
            if blkflgB:
                if vS[0:2] == "||":
                    attribL[0](vsL)
                    blkflgB = False
                    vsL = []
                    vsL.append(vS[2:].split("|"))    
                    indxI = vcmdL.index(vsL[0][0].strip())
                    attribL[indxI](vsL)                 # call attribute                          
                    continue
                vsL.append(vS.strip())
                continue
            if vS[0:2] == "||":
                vsL = []
                vsL.append(vS[2:].split("|"))
                indxI = vcmdL.index(vsL[0][0].strip()) 
                if vsL[0][indxI].strip() == "image":       # check image block
                    blkflgB = True
                    continue
                attribL[indxI](vsL)                     # call attribute                          
                continue
            if "]_" in vS:                              # process a tag
                if "[#]_" in vS:
                    vS = vS.replace("[#]_", "[" + 
                        str(self.setsectD["ftqueL"][-1]) + "]" )
                    print(vS); self.calcS += vS + "\n"
                    incrI = self.setsectD["ftqueL"][-1] + 1
                    self.setsectD["ftqueL"].append(incrI); continue
                chk = any(tag in tagL for tag in vS)
                if True in chk:
                    self.calcS, self.setsectD = _tags(vS, self.calcS, self.setsectD)
                    continue 
                else:
                    utfS = vS.replace("]_","]")
                    print(utfS); self.calcS += utfS + "\n"
                    continue
            print(vS.rstrip()); self.calcS += vS.rstrip() + "\n"

        df = pd.DataFrame(vsL)                             # write value table
        hdrL = ["variable", "value", "value" "description"]
        old_stdout = sys.stdout
        output = StringIO()
        output.write(tabulate(df, tablefmt="grid", headers=hdrL, showindex=False))            
        valueS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()
        print(valueS + "\n"); self.calcS += valueS + "\n"

        self.rivetD.update(locals())
        return self.calcS, self.setsectD, self.rivetD, self.exportS
        
    def v_assign(self, vL: list):
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

    def v_values(self, vL: list):
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

    def v_vector(self, vL: list):
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

class _E_utf:
    """convert equation-string to utf-calc string

    """

    def __init__(self, strL: list, folderD: dict, setcmdD: dict,
                setsectD: dict, rivetD: dict, exportS: str):     
        """convert equation-string to utf-calc string
        
        Args:
            strL (list): rivet strings
            rivetD (dict): rivet calculation values
            folderD (dict): folders
            exportS (str): exported values
            setcmdD (dict): command settings
            setsectD (dict): section settings

    Commands: tex, sym, table, image
    Tags: all
        """
        self.calcS = """"""
        self.exportS = exportS
        self.strL = strL
        self.folderD = folderD
        self.rivetD = rivetD
        self.setsectD = setsectD
        self.setcmdD = setcmdD
        self.tmpD = setcmdD

    def e_parse(self) -> tuple:
        """parse equation-strings
        
        Return:  
            calcS (list): utf formatted calc strings
            exportS (list): 
            setsectD (dict): updated section settings
            setcmdD (dict): updated command settings
            rivetD (list): local() dictionary
        """
        locals().update(self.rivetD)                
        
        eL = []; indxI = -1
        ecmdL = ["table", "equation", "func", "format", "image" ]
        attribL = [self.e_symbol, self.e_function, self.e_format]
        tagL =  ["[page]_", "[line]_", "[link]_", "[cite]_", "[foot]_",   
                        "[r]_", "[c]_", "[e]_", "[t]_", "[f]_" ] 
        for eS in self.strL:
            if eS[0:2] == "##":  continue              # remove review comment
            eS = vS[4:]                                # remove indent
            try: 
                if vS[0] == "#" : continue             # remove comment 
                if vS[0:2] == "::" : continue          # remove preformat         
            except:
                print(" "); self.calcS += "\n"
                continue
            if blkflgB:
                if vS[0:2] == "||":
                    attribL[0](vsL)
                    blkflgB = False
                    vsL = []
                    vsL.append(vS[2:].split("|"))    
                    indxI = vcmdL.index(vsL[0][0].strip())
                    attribL[indxI](vsL)                 # call attribute                          
                    continue
                vsL.append(vS.strip())
                continue
            if vS[0:2] == "||":
                vsL = []
                vsL.append(vS[2:].split("|"))
                indxI = vcmdL.index(vsL[0][0].strip()) 
                if vsL[0][indxI].strip() == "image":       # check image block
                    blkflgB = True
                    continue
                attribL[indxI](vsL)                     # call attribute                          
                continue
            if "]_" in vS:                              # process a tag
                if "[#]_" in vS:
                    vS = vS.replace("[#]_", "[" + 
                        str(self.setsectD["ftqueL"][-1]) + "]" )
                    print(vS); self.calcS += vS + "\n"
                    incrI = self.setsectD["ftqueL"][-1] + 1
                    self.setsectD["ftqueL"].append(incrI); continue
                chk = any(tag in tagL for tag in vS)
                if True in chk:
                    self.calcS, self.setsectD = _tags(vS, self.calcS, self.setsectD)
                    continue 
                else:
                    utfS = vS.replace("]_","]")
                    print(utfS); self.calcS += utfS + "\n"
                    continue
            print(vS.rstrip()); self.calcS += vS.rstrip() + "\n" 
        
        self.rivetD.update(locals())
        return (self.calcS, self.setsectD, self.rivetD, self.exportS)
    
    def e_symbol(self, eL: list):
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

    def e_table(self, eL):
        """ process equations and write tables
        
        Args:
            eL (list): list of equation plus parameters
        
        """

        locals().update(self.rivetD)
        
        print(75,eL)
        resfS = str(self.setcmdD["prec"].strip())
        eqfS = str(self.setcmdD["trim"].strip()) 
        exec("set_printoptions(precision=" + eqfS + ")")
        exec("Unum.VALUE_FORMAT = '%." + resfS + "f'")
        eqS = eL[0].strip()
        exec(eqS, globals(), self.rivetD)
        locals().update(self.rivetD)


        varS = eqS.split("=")[0].strip()

        typeE = type(eval(resS))
        if typeE == list or typeE == tuple:
            eF = eval(resS)
            self._write_utf((var0 + " = "), 1)
            self._write_utf(' ', 0)
            plist1 = ppr.pformat(tmp1, width=40)
            self._write_utf(plist1, 0, 0)
        if typeE == Unum:
            exec("Unum.VALUE_FORMAT = '%." + rformat.strip() + "f'")
            if len(cunit) > 0:
                tmp = eval(var0).au(eval(cunit))
            else:
                tmp = eval(var0)
            tmp1 = tmp.strUnit()
            tmp2 = tmp.asNumber()
            chkunit = str(tmp).split()
            #print('chkunit', tmp, chkunit)
            if len(chkunit) < 2: tmp1 = ''
            resultform = "{:,."+ rformat + "f}"
            result1 = resultform.format(tmp2)
            tmp3 = result1 + ' '  + tmp1
            self._write_utf((var0 + " = " + tmp3).rjust(self.widthc-1), 1, 0)
        else:
            if type(eval(var0)) == float or type(eval(var0)) == float64:
                resultform = "{:,."+rformat + "f}"
                result1 = resultform.format(eval(var0))
                self._write_utf((var0 +"="+
                                 str(result1)).rjust(self.widthc-1), 1, 0)
            else:
                    self._write_utf((var0 +"="+
                                str(eval(var0))).rjust(self.widthc-1), 1, 0)
        
        print(eS); self.calcS += eS + "\n"


    def e_sub(self, epl: list, eps: str):
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

    def e_function(self):
        pass

    def e_format(self, eL):        
        eupL = eL[1].strip()
        eD = dict(i.split(":") for i in eupL.split(","))
        self.setcmdD.update(eD)

class _T_utf:
    """convert table-strings to utf-calc

    """
 
    def __init__(self, strL: list, folderD: dict, setcmdD: dict,
                 setsectD: dict, rivetD: dict, exportS: str):       
        """

        Args:
            tlist (list): list of input lines in table string
        """
        
        self.calcS = """"""
        self.strL = strL
        self.rivetD = rivetD
        self.folderD = folderD
        self.setcmdD = setcmdD
        self.setsectD = setsectD
        self.exportS = exportS
        self.tcalc = []
        self.tlist = []

    def t_parse(self) -> tuple:
        """parse table-strings

        Return:
            vcalc (list): list of calculated strings
            local_dict (list): local() dictionary
        """
             
        tL = []; indxI = -1; ttmpL=[]
        tcmdL = ["table", "image", ]
        attribL = [self.t_table, self.t_image]
        tagL =  ["[page]_", "[line]_", "[link]_", "[cite]_", "[foot]_",   
                        "[r]_", "[c]_", "[e]_","[t]" ] 

        for tS in self.strL:
            locals().update(self.rivetD)
            tS = tS[4:].strip()                         # remove 4 space indent
            if len(ttmpL) > 0:                          # call image
                ttmpL.append(tS.strip())
                if indxI == 2:
                    self.t_image(ttmpL)
                    ttmpL =[]; indxI = -1; continue
                else: continue
            if len(tS.strip()) == 0:                    # if empty line                   
                print(""); self.calcS += "\n"; continue      
            if tS[0:2] == "||":                         # command
                tL = tS[2:].split("|")
                callS = ((tL[0].split(":"))[0]).strip()
                indxI = tcmdL.index(callS)            
                if tcmdL[indxI] == "image":
                    ttmpL = tL; continue           
                attribL[indxI](tL); continue            
            if "=" in tS:                               # statement
                utfS = tS.strip()
                exec(utfS)
                print(utfS); self.calcS += utfS + "\n"; continue       
            if tS[0] == "#" : continue                  # remove comment 
            if tS[0:2] == "::" : continue               # remove preformat 
            if "]_" in tS:                              # process a tag
                if "[#]_" in tS:
                    tS = tS.replace("[#]_", "[" + 
                        str(self.setsectD["ftqueL"][-1]) + "]" )
                    print(tS); self.calcS += tS + "\n"
                    incrI = self.setsectD["ftqueL"][-1] + 1
                    self.setsectD["ftqueL"].append(incrI)
                    continue
                elif any(tag in tS for tag in tagL):
                    self.calcS, self.setsectD = _tags(tS, self.calcS, self.setsectD)
                    continue 
                else:
                    utfS = tS.replace("]_","]")
                    print(utfS); self.calcS += utfS + "\n"; continue
            print(tS); self.calcS += tS + "\n"         
            
        return (self.calcS, self.setsectD, self.exportS)
       
    def t_read(self, tL: str) -> str:
        """[summary]
        
        Args:
            tl (str): [description]
        """
        locals().update(self.rivetD)
        
        df = tL[1].strip()
        filenameS = tL[2].strip()
        pnameS = str(Path(self.folderD["tpath"], filenameS).as_posix())
        pnameS 
        cmdS = str(df) + "= pd.read_csv('" + pnameS + "')" 
        exec(cmdS)     
        
        self.rivetD.update(locals())

    def t_save(self, tL: str):
        """[summary]
        
        Args:
            tL (str): [description]
        """

        locals().update(self.rivetD)

        dfS = tL[1].strip()
        eval(dfS)
        filenameS = tL[2].strip()
        if ".csv" in filenameS:
            pathnameS =  Path(self.folderD["tpath"], filenameS ).as_posix()
            cmdlineS =  dfS + ".to_csv('" + str(pathnameS) +  "',index = False)"
            exec(cmdlineS)
        elif ".png" or ".jpg" in filenameS:
            pathnameS =  Path(self.folderD["fpath"], filenameS ).as_posix()
            cmdline1 = "fig =" + dfS + ".get_figure()"
            cmdline2 =  "fig.savefig('" + str(pathnameS) +  "')"
            exec(cmdline1)
            exec(cmdline2) 

        self.rivetD.update(locals())
        
    def t_data(self, tL:str) -> str:
        """[summary]
        
        Args:
            tLine (str): [description]
        """
        locals().update(self.rivetD)

        dfS = tL[1].strip()
        cmdlineS = dfS + " = pd.DataFrame()"
        exec(cmdlineS)        
    
        self.rivetD.update(locals())

    def t_table(self, tL: list):
        """insert table from inline or csv, rst file 
        
        Args:
            ipl (list): parameter list
        """       
        locals().update(self.rivetD)
        
        try:
            widthI = int(tL[0].split(":")[1])
        except:
            widthI = int(self.setcmdD["cwidth"])
        self.setcmdD.update({"cwidth":widthI})
        tableS = ""; utfS = ""
        files = tL[1].strip()
        tfiles = Path(self.folderD["tpath"], files)   
        if ".csv" in tL[1]:                        # csv ftLe       
            format1 = []
            with open(tfiles,'r') as csvfiLe:
                readL = list(csv.reader(csvfiLe))
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
            try: titleS = tL[2].strip() + titleS
            except: pass        
        print(utfS); self.calcS += utfS + "\n"  
    
    def t_plot(self, tL: str)-> list:
        """[summary]
        
        Args:
            tL (str): [description]
        """                
 
        locals().update(self.rivetD)
        
        pltL = tL[1].split(",")
        dfS, pltS = pltL[0].strip(),pltL[1].strip()
        pltcmd = tL[2].strip()
        cmdline1 = "ax = plt.gca()"
        cmdline2 = pltS + "=" + dfS + ".plot(" + pltcmd + ", ax=ax)"
        exec(cmdline1)
        exec(cmdline2)

        self.rivetD.update(locals())

    def t_add(self, tL: str)-> list:
        """[summary]
        
        Args:
            tL (str): [description]
        """                

        locals().update(self.rivetD)

        pltL = tL[1].split(",")
        dfS, pltS = pltL[0].strip(),pltL[1].strip()
        pltcmd = tL[2].strip()
        cmdline2 = pltS +"=" + dfS + ".plot(" + pltcmd + ", ax=ax)"
        exec(cmdline2)

        self.rivetD.update(locals())

    def t_image(self, tL: list):
        """insert image from fiLe
        
        Args:
            ipl (list): parameter list
        """
        try:
            scaleI = int(tL[2].strip())
        except:
            scaleI = self.setcmdD["scale1"]
        self.setcmdD.update({"scale1":scaleI})
        self.setsectD["fnum"] += 1
        figI = self.setsectD["fnum"]
        sectI = self.setsectD["snum"]
        files = tL[1].strip()
        try:
            captionS = tL[2].strip()
            imgpathS = str(Path(self.folderD["fpath"], files))
            utfS = ("Figure " + str(sectI) + '.' + str(figI) + "  "  
               + captionS + "\npath: " + imgpathS + "\n")
        except:
            imgpathS = str(Path(self.folderD["fpath"], files))
            utfS = ("Figure: " + imgpathS + "\n")
        print(utfS); self.calcS += utfS + "\n"

    def t_image2(self, tL: list):
        """insert two images side by side from fiLes
        
        Args:
            tL (list): image parameter list
        """
        try:                                            # update default scale
            scaleI= tL[2].strip()
            scale1I = int(scaleI.split(","))[0].strip()
            scale2I = int(scaleI.split(","))[1].strip()
            self.setcmdD.update({"scale1":scale1I})
            self.setcmdD.update({"scale2":scale2I})
        except:
            scale1I = self.setcmdD["scale1"]
            scale2I = self.setcmdD["scale2"]
        self.setsectD["fnum"] += 1                     # image 1
        figI = self.setsectD["fnum"]
        sectI = self.setsectD["snum"]
        files = tL[1].strip()
        captionS = tL[3].strip()
        imgP = str(Path(self.folderD["fpath"], files))
        utfS = ("Figure " + str(sectI) + '.' + str(figI) + "  "  
               + captionS + "\npath: " + imgP)
        print(utfS); self.calcS += utfS + "\n"

        self.setsectD["fnum"] += 1                     # image 2
        figI = self.setsectD["fnum"]
        sectI = self.setsectD["snum"]
        files = tL[2].strip()
        captionS = tL[4].strip()
        imgP = str(Path(self.folderD["fpath"], files))
        utfS = ("Figure " + str(sectI) + '.' + str(figI) + "  "  
               + captionS + "\npath: " + imgP)
        print(utfS); self.calcS += utfS + "\n"