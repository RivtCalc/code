#! python
"""transform rivet-string to calc-string

A separate class transforms each rivet-string type to a utf-8 calc-string. 
Commands are single lines except where noted as block below.

-------  --------  -----  ----------------------------------------------------
string   function  class
type     name      name    commands {comments}
-------  --------  -----   ---------------------------------------------------
Repo      R       _R_utf   scope, toc, summary {block}, attach {block}
Insert    I       _I_utf   tex, sym, table, image {block}, image2 {block} 
Values    V       _V_utf   =, values, 
Equation  E       _E_utf   =, format, function
Table     T       _T_utf   table, image, image2, {any Python simple statement}

Command syntax  
---------------
R(''' r-string defines repository and report data
    
    May include arbitrary text that does not start with double bar.  It
    will be treated as a comment and will not be processed.
    
    || summary | calc title
    paragraph
    
    || toc | section or string

    || scope | # csv list used in repo read.me and other databases
    
    || attach | calccover.pdf         
    pdf_file1 | A. Appendix label
    pdf_file2 | B. Appendix label
    functions {or} docstrings | C. Appendix label
    ''')

I(''' # i-string inserts static text, tables and images
    
    May include arbitrary text that does not start a line with double bar.
    
    || tex | \gamma = x + 3 # latex equation | 1. # image scale
    || sym | x = y/2 # sympy equation | 1.
    || table | x.txt | 60 # max paragraph width - characters 
    || table | x.csv | 60,[:] # max column width - characters, line range  
    || table | x.rst | [:] # line range

    || image | x.png/x.jpg {image file} | 1. {scale}
    figure caption

    || image2  | x1.png, x2.jpg  | 1., 1.
    figure1 caption
    figure2 caption
    ''')

V('''v-string''') {define values}

    May include arbitrary text that does not start line with a double bar
    or include equal sign.

    x = 10.1*IN, M  {alt units} | description  

    || vector | x.csv | VECTORNAME r[n] {assign row in file to vector}
    || vector | x.csv | VECTORNAME c[n] {assign column in file to vector}    
    || values | vfile.py  | [:] {assignment lines to read}

E('''e-string''') {define equations}
    
    May include arbitrary text that does not start a line with double bar
    or include equal sign.

    || format | prec:2 {result precision}, trim:2, replace:False, code:False    

     x = v1 + 4*M               | units, alt units {apply to result}
     y = v2 / 4                 | units, alt units

    || script | x.py | func_name | units, alt  {import function from file}

T('''t-string''') {define tables and plots}
    
    May include arbitrary text that does not start a line with a double bar
    or include equal sign.

    || data | VAR1 {define} | description   
    || read | VAR2 {assign} | file.csv 
    || save | VAR1 | file.csv or file.png {table or plot}
    || plot | VAR2 | x:c1 {col}, y:c2 {col}, kind:line, grid:True
    || add  | VAR2 | x:c3, y:c4
    
    VAR3 = pandas_function(VARS)    {pandas library operations}
    
    || table | x.csv | 60
    
    || image | x.png | 1.
    figure caption
    
    || image2 | x1.png, x2.jpg  | 1., 1.
    figure1 caption
    figure2 caption

Tags Syntax {comment}
-------------------
some text in line [abc123]_     {citation}
some text in line [#]_          {autoincremented footnote}
some text in line [r]_          {right justify line}
some text in line [c]_          {center line}
table title [t]_                {autoincremented table number}   
label for equation [e]_         {autoincremented equation number}
[s]_  section title             {first line in string function}
[cite]_  citation text          {citation description (FIFO)}    
[foot]_  foot note text         {footnote description (FIFO)}
[link]_  http:\\url             {http link}
[page]_                         {start new doc page}
[line]_                         {insert horizontal line}

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
from rivet.rivet_unit import *
from io import StringIO
from sympy.parsing.latex import parse_latex
from sympy.abc import _clash2
from tabulate import tabulate 
from pathlib import Path

logging.getLogger("numexpr").setLevel(logging.WARNING)

def _refs(onumI: int, setsectD: dict, typeS: str) -> str:
    """[summary]
    
    Args:
        refS (str): [description]
        setsectD (dict): [description]
        typeS (str): [description]
    
    Returns:
        str: [description]
    """

    ofillS = str(onumI).zfill(2)
    sfillS = str(setsectD["snum"]).strip().zfill(2)
    rnumS = str(setsectD["rnum"])
    refS = "[" + typeS + rnumS + "." + sfillS + "." + ofillS + "]"

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
        tagL = tagS.strip().split("]_")
        utfS = "link: "+ tagL[1].strip()
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
    """
    def __init__(self, strL :list, folderD :dict, setsectD :dict) -> str:
        self.calcS = """"""
        self.strL = strL
        self.folderD = folderD
        self.setsectD = setsectD

    def r_parse(self) -> str:
        """ parse repository string
       
       Returns:
            string :  formatted utf-calc string
        """
        endflgB = False; rtmpS = ""; rL = []; indxI = -1
        rcmdL = ["summary", "scope", "attach", "toc" ]
        methodL =  [self.r_summary, self.r_label, self.r_append]
        tagL =  [ "[r]_", "[c]_", "[link]_"] 
        
        for rS in self.strL:
            if rS[0:2] == "##":  continue           # remove review comment
            rS = rS[4:]                             # remove indent
            if len(rS.strip()) == 0:                # blank line, end block
                if endflgB:
                    rL.append(rtmpS.strip())
                    methodL[indxI](rL)              # call attribute from list                          
                    endflgB = False; rtmpS = ""; rL = []; indxI = -1      
                print(""); self.calcS += "\n" 
                continue
            if endflgB:                             # add lines until blank
                rtmpS = rtmpS + rS + "\n"; continue
            if rS[0:2] == "||":                     # find command
                rL = rS[2:].split("|")
                indxI = rcmdL.index(rL[0].strip())            
                endflgB = True; continue
            # commands
            if rS[0] == "#" : continue              # remove comment 
            if rS[0:2] == "::" : continue           # remove preformat 
            if "]_" in rS:                          # process a tag
                if "[#]_" in rS:
                    rS = rS.replace("[#]_", "[" + 
                        str(self.setsectD["ftqueL"][-1]) + "]" )
                    print(rS); self.calcS += rS + "\n"
                    incrI = self.setsectD["ftqueL"][-1] + 1
                    self.setsectD["ftqueL"].append(incrI); continue
            elif any(tag in rS for tag in tagL):
                self.calcS, self.setsectD = _tags(rS, self.calcS, self.setsectD)
                continue 
            else:
                utfS = rS.replace("]_","]")
                print(utfS); self.calcS += utfS + "\n"; continue
                citeS = utfS.strip("[]_")
                self.setsectD["ftqueL"].append(citeS); continue
            print(rS); self.calcS += rS + "\n"     

        return (self.calcS, self.setsectD)

    def r_summary(self, rL):
        utfS = "Summary\n"
        utfS += "-------\n"
        utfS += rL[2]
        print(utfS + "\n"); self.calcS += utfS
        
    def r_append(self, rL):
        utfS = "Attach\n"
        utfS += "------\n" 
        utfS += rL[2].strip()
        print(utfS + "\n"); self.calcS += utfS

    def r_scope(self, rL):
        csvL = rL[2].split("\n")
        tabL = [x.split(",") for x in csvL]
        maxlenI = max(len(x) for x in tabL)
        for idx,val in enumerate(tabL):
            if len(val) < maxlenI:
                addL = maxlenI - len(val)
                tabL[idx].extend("-"*addL)
        headers = ["category"]
        for i in range(maxlenI-1) : headers.append("label") 
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(tabulate(tabL, headers, tablefmt="grid"))            
        utfS = output.getvalue()
        print(utfS + "\n"); self.calcS += utfS
        sys.stdout = old_stdout    
    
class _I_utf:  
    """convert Insert-string to utf-calc string 

    Attributes:
        strL (list): rivet-string
        folderD (dict): folder structure
        sectD (dict):  header information
        cmdD (dict): command settings
    """

    def __init__(self, strL: list, folderD: dict, setcmdD: dict, setsectD: dict):
        self.calcS = """"""
        self.strL = strL
        self.folderD = folderD
        self.setsectD = setsectD
        self.setcmdD = setcmdD

    def i_parse(self) -> tuple:
        """ parse insert-string
       
       Returns:
            tuple :  a string and 3 dictionaries
        """
        iL = []; itmpL=[]; indxI =-1 
        icmdL = ["sympy", "latex", "table", "image", "image2"]
        attribL = [self.i_sympy, self.i_latex, self.i_table, 
                            self.i_image, self.i_image2]
        tagL =  ["[page]_", "[line]_", "[link]_", "[cite]_", "[foot]_",   
                    "[r]_", "[c]_", "[e]_","[t]" ] 
        
        for iS in self.strL:
            iS = iS[4:]                             # remove 4 space indent
            if len(itmpL) > 0:                      # call image or image2
                itmpL.append(iS.strip())
                if indxI == 3:
                    self.i_image(itmpL)
                    itmpL =[]; indxI = -1; continue
                if len(itmpL) == 5:
                    self.i_image2(itmpL)
                    itmpL =[]; continue
                else: continue
            if len(iS.strip()) == 0:                # if empty line                   
                print(""); self.calcS += "\n"; continue      
            if iS[0:2] == "||":                     # process a command
                iL = iS[2:].split("|")
                callS = ((iL[0].split(":"))[0]).strip()
                indxI = icmdL.index(callS)
                if icmdL[indxI] == "image":
                    itmpL = iL; continue
                if icmdL[indxI] == "image2":
                    itmpL = iL; continue                
                attribL[indxI](iL); continue
            if iS[0] == "#" : continue              # remove comment 
            if iS[0:2] == "::" : continue           # remove preformat 
            if "]_" in iS:                          # process a tag
                if "[#]_" in iS:
                    iS = iS.replace("[#]_", "[" + 
                        str(self.setsectD["ftqueL"][-1]) + "]" )
                    print(iS); self.calcS += iS + "\n"
                    incrI = self.setsectD["ftqueL"][-1] + 1
                    self.setsectD["ftqueL"].append(incrI); continue
                if any(tag in iS for tag in tagL):
                    self.calcS, self.setsectD = _tags(iS, self.calcS, self.setsectD)
                    continue 
                else:
                    utfS = iS.replace("]_","]")
                    print(utfS); self.calcS += utfS + "\n"; continue    
            print(iS); self.calcS += iS + "\n"

        return self.calcS, self.setsectD, self.setcmdD
        
    def i_latex(self,iL: list):
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
        ltxS = parse_latex(txS)
        utfS2 = sp.pretty(sp.sympify(ltxS, _clash2, evaluate=False))
        utfS = ""
        for iS in utfS2.split('\n'):
            if "ANTLR runtime and generated code versions" in iS: continue
            utfS += (iS+"\n")
        print(utfS+"\n"); self.calcS += utfS + "\n"   

    def i_sympy(self,iL):
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
        fileS = iL[1].strip()
        try:
            captionS = iL[2].strip()
            imgpathS = str(Path(self.folderD["fpath"], fileS))
            utfS = ("Figure " + str(sectI) + '.' + str(figI) + "  "  
               + captionS + "\npath: " + imgpathS + "\n")
        except:
            imgpathS = str(Path(self.folderD["fpath"], fileS))
            utfS = ("Figure: " + imgpathS + "\n")
        print(utfS); self.calcS += utfS + "\n"

    def i_image2(self, iL: list):
        """insert two images side by side from files
        
        Args:
            iL (list): image parameter list
        """
        try:                                            # update default scale
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

    def i_table(self, iL: list):
        """insert table from inline or csv, rst file 
        
        Args:
            ipl (list): parameter list
        """       
        try:
            widthI = int(iL[2].strip())
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
            try: titleS = iL[2].strip() + titleS
            except: pass        
        elif ".rst" in iL[1]:                        # rst file
            with open(xfileS,'r') as rst: 
                utfS = rst.read()
            titleS = "  \n"
            try: titleS = iL[2].strip() + titleS
            except: pass
        else:                                       # inline reST table 
            utfs = ""
            titleS = "  "
            try: titleS = iL[2].strip() + titleS
            except: pass
        print(utfS); self.calcS += utfS + "\n"  

    def i_text(self, iL: list):
        """insert text from file
        
        Args:
            iL (list): text command list
        """
        try: 
           widthI = int(iL[2].strip())
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
            exportS (list): 
            rivetD (list): calculation values
            setsectD (dict): section settings
            setcmdD (dict): command settings
         """

        valL=[]
        tagL =  ["[page]_", "[line]_", "[link]_", "[cite]_", "[foot]_",   
                        "[r]_", "[c]_", "[e]_","[t]" ] 

        locals().update(self.rivetD)

        for vS in self.strL:
            self.rivetD.update(locals())
            if vS[0:2] == "##":  continue               # remove review comment
            vS = vS[4:]                                 # remove 4 space indent
            if len(vS.strip()) == 0:                    # insert blank line
                print(""); self.calcS += "\n"; continue
            if vS[0] == "#" : continue                  # remove comment 
            if vS[0:2] == "::" : continue               # remove preformat 
            if "=" in vS:                               # find assign
                vL = vS.split("|")                 
                valL += self.v_assign(vL)
                continue
            if vS[0:2] == "||":                         # find command
                vL = vS[2:].split("|")
                if vL[0].strip() == "value":
                    valL += self.v_value(vL)                                
                elif vL[0].strip() == "vector":
                    valL += self.v_vector(vL)
                continue
            if "]_" in vS:                              # process a tag
                if "[#]_" in vS:
                    vS = vS.replace("[#]_", "[" + 
                        str(self.setsectD["ftqueL"][-1]) + "]" )
                    print(vS); self.calcS += vS + "\n"
                    incrI = self.setsectD["ftqueL"][-1] + 1
                    self.setsectD["ftqueL"].append(incrI); continue
                elif any(tag in vS for tag in tagL):
                    self.calcS, self.setsectD = _tags(vS, self.calcS, self.setsectD)
                    continue 
                else:
                    utfS = vS.replace("]_","]")
                    print(utfS); self.calcS += utfS + "\n"
                    continue
            valL=[]
            print(vS); self.calcS += vS + "\n"     

        df = pd.DataFrame(valL)                             # write table
        hdrL = ["variable", "value", "description"]
        old_stdout = sys.stdout
        output = StringIO()
        output.write(tabulate(df, tablefmt="grid", headers=hdrL, showindex=False))            
        valueS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()
        print(valueS + "\n"); self.calcS += valueS + "\n"

        self.rivetD.update(locals())
        return (self.calcS, self.setsectD, self.rivetD, self.exportS, )
        
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

class _Eutf:
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
        ecmdL = ["equation", "func", "format" ]
        attribL = [self.e_symbol, self.e_function, self.e_format]
        tagL =  ["[page]_", "[line]_", "[link]_", "[cite]_", "[foot]_",   
                        "[r]_", "[c]_", "[e]_","[t]" ] 

        for eS in self.strL:
            eS = eS[4:].strip()                    # remove 4 space indent
            if len(eS.strip()) == 0:               # empty line                   
                print(""); self.calcS += "\n"; continue
            if "||" in eS:                         # command
                eL = eS[2:].split("|")
                callS = eL[0].strip()
                indxI = ecmdL.index(callS)
                attribL[indxI](eL); continue            
            if "=" in eS:                          # equation
                eL = eS.split("|")
                callS = "equation"
                indxI = ecmdL.index(callS)
                attribL[indxI](eL)
                #if self.setcmdD["sub"]:
                #    e_sub(eL)
                #else:
                #    e_table(eL)           
                continue            
            if eS[0] == "#" : continue             # remove comment 
            if eS[0:2] == "::" : continue          # remove preformat 
            if "]_" in eS:                         # process a tag
                if "[#]_" in eS:
                    eS = eS.replace("[#]_", "[" + 
                        str(self.setsectD["ftqueL"][-1]) + "]" )
                    print(eS); self.calcS += eS + "\n"
                    incrI = self.setsectD["ftqueL"][-1] + 1
                    self.setsectD["ftqueL"].append(incrI)
                    continue
                elif any(tag in eS for tag in tagL):
                    self.calcS, self.setsectD = _tags(eS, self.calcS, self.setsectD)
                    continue 
                else:
                    utfS = eS.replace("]_","]")
                    print(utfS); self.calcS += utfS + "\n"
                    continue
            print(eS); self.calcS += eS + "\n"     
        
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

class _Tutf:
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
        tcmdL = ["read", "save", "data", "table", "plot", "add", 
                                                "image", "image2" ]
        attribL = [self.t_read, self.t_save, self.t_data, self.t_table,
                     self.t_plot, self.t_add, self.t_image, self.t_image2]
        tagL =  ["[page]_", "[line]_", "[link]_", "[cite]_", "[foot]_",   
                        "[r]_", "[c]_", "[e]_","[t]" ] 

        for tS in self.strL:
            locals().update(self.rivetD)
            tS = tS[4:].strip()                         # remove 4 space indent
            if len(ttmpL) > 0:                          # call image or image2
                ttmpL.append(tS.strip())
                if indxI == 6:
                    self.t_image(ttmpL)
                    ttmpL =[]; indxI = -1; continue
                if len(ttmpL) == 7:
                    self.t_image2(ttmpL)
                    ttmpL =[]; continue
                else: continue
            if len(tS.strip()) == 0:                    # if empty line                   
                print(""); self.calcS += "\n"; continue      
            if tS[0:2] == "||":                         # command
                tL = tS[2:].split("|")
                callS = ((tL[0].split(":"))[0]).strip()
                indxI = tcmdL.index(callS)            
                if tcmdL[indxI] == "image":
                    ttmpL = tL; continue
                if tcmdL[indxI] == "image2":
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