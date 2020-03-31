#! python
"""convert rivet strings to utf-8 calcs

This module converts each rivet string to a utf-8 calc string, using
a class for each of the 5 string types. String markup inlcudes commands and 
tags.  See parse_tag function for tag summary.

List of commands by string type {notes in braces}:
type    : commands
----      --------
repro   : summary {block}, labels {block}, append {block}, link
insert  : text, tex, sym, img {block}, table {block}, cite, foot, link,   
values  : link
equation: format, link
table   : create, write, read, plot, add, save, {plus insert commands}

detail {notes}
--------------
r__('''r-string''') {repository and calc data}
    || summary | {toc} sections / functions  | {include} docstrings  
        {paragraph text}
    || labels 
        {csv list}
    || append           
        x.pdf {pdf file name}, {appendix title text}
i__('''i-string''') {insert text and images}
    || latex : ss  {scale} | {latex equation text}
    || sympy : ss | {sympy equation text}
    || image2 : ss {scale} | x.png/x.jpg {image file} 
    figure title text
    || image : ss | x.png/x.jpg {image file} 
    figure title text
    || table : ww {width} | x.txt {text file} 
    || table : ww | n.csv {file name} 
    table title text
    || table  | x.rst {file name}
    table title text
    || table  | inline 
    table title text
v__('''v-string''') {define values}
    || values | 
e__('''e-string''') {define equations}
    || format | {decimals}e:n, {result}r:n, {check}c:0, {print}p:0/1/2, #:t/f  
    || func   | {decimals}e:n, {result}r:n, {check}c:0, {print}p:0/1/2, #:t/f  
t__('''t-string''') (define tables and plots)
    || read   | .csv file name | table name
    || save   | .csv file name | table name 
    || data   | table name

    || plot   | f.csv {file name} |(col names)x:c1,y:c2,(rows)r:[],(kind)k:line,(grid)g:t/f
    || add (data to plot) | (col names) x:c3, y:c4, (color)c:blue        
    || save | n.png / n.jpg {file names} | f {name from plot command} 
    {plus all insert commands}

List of tags {notes}:
---------------------
    [xyz123]_               {citation}   
    [cite]_                 {citation description}
    [#]_                    {footnote (auto)} 
    [foot]_                 {footnote description}
    [page]_                 {new page in docs)
    [line]_                 {draw horizontal line)
    [link]_  http://xyz     {url link}
    [r]_                    {right justify line of text)
    [re]_                   {right justify line of text and add equation number)
    [c]_                    {center line of text)
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
from io import StringIO
from numpy import *
import numpy.linalg as la
import pandas as pd
import sympy as sp
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
from sympy.parsing.latex import parse_latex
from sympy.abc import _clash2
from tabulate import tabulate 
from pathlib import Path
from rivet.rivet_unit import *

logging.getLogger("numexpr").setLevel(logging.WARNING)


def _tags(tagS: str, calcS: str, setsectD: dict) -> str:
    """parse tags
    
    Args:
        tagS (str): line from rivet string
    
    List of tags :
    [abc]_      (citation name)   
    [page]_     (new doc page)
    [line]_     (draw horizontal line)
    [link]_     (url link)
    [foot]_     (footnote reference)
    [r]_        (right justify line of text)
    [c]_        (center line of text)

    """
    if "[page]_" in tagS:
        utfS = int(setsectD["swidth"]) * "."
        print(utfS); calcS += utfS + "\n"
        return calcS
    elif "[line]_" in tagS:
        utfS = int(setsectD["swidth"]) * '-'   
        print(utfS); calcS += utfS + "\n"
        return calcS        
    elif "[r]_" in tagS:
        tagL = tagS.split("[r]")
        utfS = (tagL[0].strip()).rjust(int(setsectD["swidth"]-1))
        print(utfS); calcS += utfS + "\n"       
        return calcS
    elif "[link]_" in tagS:
        rL = tagS.split("]_")
        utfS = "link: "+ rL[1].strip()
        print(utfS); calcS += utfS + "\n"
        return calcS
    elif "[foot]_" in tagS:
        rL = tagS.split("]_")
        utfS = "[" + str(setsectD["footqueL"].popleft()) + "] " + rL[1].strip()
        print(utfS); calcS += utfS + "\n"
        return calcS
    elif "[cite]_" in tagS:
        rL = tagS.split("]_")
        utfS = rL[1]
        print(utfS); calcS += utfS + "\n"
        return calcS
    else:
        return tagS
        #tag = re.search(r"\[.*?\]_", tagS)
        #tagx = tag.group(0)
        #modline = tagS.replace(" " + tagx,"")

class R_utf:
    """convert repo-string to utf-calc string

    Attributes:
        rstrL (list): rivet-strings
        folderD (dict): folder structure
        sectD (dict): header information
    """
    def __init__(self, strL :list, folderD :dict, setsectD :dict) -> str:
        self.calcS = """"""
        self.strL = strL
        self.folderD = folderD
        self.setsectD = setsectD

    def r_parse(self) -> str:
        """ parse repo string
       
       Returns:
            string :  formatted utf-calc string
        """
        endflgB = False; rtmpS = ""; rL = []; indxI = -1
        rcmdL = ["summary", "label", "append" ]
        methodL =  [self.r_summary, self.r_label, self.r_append]
        tagL =  ["[page]_", "[line]_", "[r]_", "[rn]_", "[c]_",  
                    "[link]_", "[cite]_", "[foot]_"] 
        
        for rS in self.strL:
            if rS[0:2] == "##":  continue           # remove review comment
            rS = rS[4:]                             # remove indent
            if len(rS.strip()) == 0:                # blank line, end block
                if endflgB:
                    rL.append(rtmpS.strip())
                    methodL[indxI](rL)              # call attribute from list                          
                    endflgB = False; rtmpS = ""; rL = []; indxI = -1      
                print("\n"); self.calcS += "\n" 
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
                        str(self.setsectD["footqueL"][-1]) + "]" )
                    print(rS); self.calcS += rS + "\n"
                    incrI = self.setsectD["footqueL"][-1] + 1
                    self.setsectD["footqueL"].append(incrI); continue
            elif any(tag in rS for tag in tagL):
                self.calcS = _tags(rS, self.calcS, self.setsectD); continue 
            else:
                utfS = rS.replace("]_","]")
                print(utfS); self.calcS += utfS + "\n"; continue
            print(rS); self.calcS += rS + "\n"     

        return (self.calcS, self.setsectD)


    def r_summary(self, rL):
        utfS = "Summary\n"
        utfS += "-------\n"
        utfS += rL[2]
        print(utfS + "\n"); self.calcS += utfS
        
    def r_append(self, rL):
        utfS = "Appendices\n"
        utfS += "----------\n" 
        utfS += rL[2].strip()
        print(utfS + "\n"); self.calcS += utfS

    def r_label(self, rL):
        csvL = rL[2].split("\n")
        tabL = [x.split(",") for x in csvL]
        maxlenI = max(len(x) for x in tabL)
        for idx,val in enumerate(tabL):
            if len(val) < maxlenI:
                addL = maxlenI - len(val)
                tabL[idx].extend("-"*addL)
        headers = ["category"]
        for i in range(maxlenI-1) : headers.append("label") 
        old_stdout = sys.stdout
        output = StringIO()
        output.write(tabulate(tabL, headers, tablefmt="grid"))            
        utfS = output.getvalue()
        print(utfS + "\n"); self.calcS += utfS
        sys.stdout = old_stdout    
    
class I_utf:  
    """convert insert-string to utf-calc string 

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
        attribL =  [self.i_sympy, self.i_latex, self.i_table, 
                            self.i_image, self.i_image2]
        tagL =  ["[page]_", "[line]_", "[r]_", "[rn]_", "[c]_",  
                    "[link]_", "[cite]_", "[foot]_"] 
        
        for iS in self.strL:
            iS = iS[4:]                             # remove 4 space indent
            if len(itmpL) > 0:                       # call image or image2
                itmpL.append(iS.strip())
                if indxI == 3:
                    self.i_image(itmpL)
                    itmpL =[]; indxI = -1; continue
                if len(itmpL) == 5:
                    self.i_image2(itmpL)
                    itmpL =[]; continue
                else: continue
            if len(iS.strip()) == 0:                # if empty line                   
                print("\n"); self.calcS += "\n"; continue      
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
                        str(self.setsectD["footqueL"][-1]) + "]" )
                    print(iS); self.calcS += iS + "\n"
                    incrI = self.setsectD["footqueL"][-1] + 1
                    self.setsectD["footqueL"].append(incrI); continue
                if any(tag in iS for tag in tagL):
                    self.calcS = _tags(iS, self.calcS, self.setsectD); continue 
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
            scaleI = int(iL[0].split(":")[1])
        except:
            scaleI = self.setcmdD["scale1"]
        self.setcmdD.update({"scale1":scaleI})
        txS = iL[1].strip()
        #txs = txs.encode('unicode-escape').decode()
        ltxS = parse_latex(txS)
        utfS = sp.pretty(sp.sympify(ltxS, _clash2, evaluate=False))
        print(utfS+"\n"); self.calcS += utfS + "\n"   

    def i_sympy(self,iL):
        """insert formated equation from SymPy string 
        
        Args:
            ipL (list): parameter list
        """
        try:
            scaleI = int(iL[0].split(":")[1])
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
            scaleI = int(iL[0].split(":")[1])
        except:
            scaleI = self.setcmdD["scale1"]
        self.setcmdD.update({"scale1":scaleI})
        self.setsectD["fignum"] += 1
        figI = self.setsectD["fignum"]
        sectI = self.setsectD["sectnum"]
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
            scaleI= iL[0].split(":")[1]
            scale1I = int(scaleI.split(","))[0].strip()
            scale2I = int(scaleI.split(","))[1].strip()
            self.setcmdD.update({"scale1":scale1I})
            self.setcmdD.update({"scale2":scale2I})
        except:
            scale1I = self.setcmdD["scale1"]
            scale2I = self.setcmdD["scale2"]
        self.setsectD["fignum"] += 1                     # image 1
        figI = self.setsectD["fignum"]
        sectI = self.setsectD["sectnum"]
        fileS = iL[1].strip()
        captionS = iL[3].strip()
        imgP = str(Path(self.folderD["fpath"], fileS))
        utfS = ("Figure " + str(sectI) + '.' + str(figI) + "  "  
               + captionS + "\npath: " + imgP)
        print(utfS); self.calcS += utfS + "\n"

        self.setsectD["fignum"] += 1                     # image 2
        figI = self.setsectD["fignum"]
        sectI = self.setsectD["sectnum"]
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
            widthI = int(iL[0].split(":")[1])
        except:
            widthI = int(self.setcmdD["cwidth"])
        self.setcmdD.update({"cwidth":widthI})
        tableS = ""; utfS = ""
        fileS = iL[1].strip()
        tfileS = Path(self.folderD["tpath"], fileS)   
        tableI = self.setsectD["tablenum"] + 1
        self.setsectD.update({"tablenum":tableI})
        sectI = self.setsectD["sectnum"]
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
            old_stdout = sys.stdout
            output = StringIO()
            output.write(tabulate(format1, tablefmt="grid", headers="firstrow"))            
            utfS = output.getvalue()
            titleS = "  \n"
            sys.stdout = old_stdout
            try: titleS = iL[2].strip() + titleS
            except: pass        
        elif ".rst" in iL[1]:                        # rst file
            with open(tfileS,'r') as rst: 
                utfS = rst.read()
            titleS = "  \n"
            try: titleS = iL[2].strip() + titleS
            except: pass
        else:                                       # inline reST table 
            utfs = ""
            titleS = "  "
            try: titleS = iL[2].strip() + titleS
            except: pass
        utfS = ("\nTable " + str(sectI)+'.' + str(tableI) + 
                        "  " + titleS ) + utfS                                              
        print(utfS); self.calcS += utfS + "\n"  

    def i_text(self, iL: list):
        """insert text from file
        
        Args:
            iL (list): text command list
        """
        try: 
            widthI = int(iL[0].split(":")[1])
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

class V_utf:
    """convert value-string to utf-calc string
        
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
        self.rivetD = rivetD
        self.folderD = folderD
        self.setsectD = setsectD
        self.setcmdD = setcmdD

    def v_parse(self)-> tuple:
        """parse strings of type value

        Return:
            calcS (list): utf formatted calc strings
            exportS (list): 
            rivetD (list): calculation values
            setsectD (dict): section settings
            setcmdD (dict): command settings
         """

        vL = []; endflgB = False; indxI = -1 
        vcmdL = ["values"]; methodL =  [self.v_assign]
        tagL =  ["[page]_", "[line]_", "[r]_", "[rn]_", "[c]_",  
                    "[link]_", "[cite]_", "[foot]_"] 
        for vS in self.strL:
            locals().update(self.rivetD)
            if vS[0:2] == "##":  continue           # remove review comment
            vS = vS[4:]                             # remove 4 space indent
            if len(vS.strip()) == 0:                # insert blank line
                print("\n"); self.calcS += "\n"            
                if endflgB:                         # end block
                    methodL[indxI](vL)              # call attribute from list                          
                    endflgB = False; vL = []; indxI = -1      
                continue
            if endflgB:                             # add values
                vL.append(vS); continue
            if vS[0:2] == "||":                     # find command
                vpL = vS[2:].split("|")
                indxI = vcmdL.index(vpL[0].strip())
                vL.append(vS[2:])            
                endflgB = True; continue
            if vS[0] == "#" : continue             # remove comment 
            if vS[0:2] == "::" : continue          # remove preformat 
            if "==" in vS:                         # print value
                varS = vS.split("==")[0].strip()
                descripS = vS.split("|")[1].strip()
                valS = str(eval(varS))
                utfS = str.ljust(varS + " = " + valS, 40) + " | " + descripS
                print(utfS); self.calcS += utfS + "\n" ; continue
            if "]_" in vS:                          # process a tag
                if "[#]_" in vS:                    # find footnote tag
                    vS = vS.replace("[#]_", "[" + 
                        str(self.sectD["footqueL"][-1]) + "]" )
                    print(vS); self.calcS += vS + "\n"
                    incrI = self.setsectD["footqueL"][-1] + 1
                    self.setsectD["footqueL"].append(incrI); continue
                else:
                    self.calcS = _tags(vS, self.calcS, self.setsectD); continue  
            print(vS); self.calcS += vS + "\n"  
        
        return (self.calcS, self.setsectD, self.rivetD, self.exportS, )
        
    def v_assign(self, vL: list):
        """assign values to variables
        
        Args:
            vL (list): list of values
        """
        
        locals().update(self.rivetD)

        pyS = """"""
        valL =[]                            # value list for table
        vpL = vL[0].split("|")
        if "inline" in vpL[1]:
            for vS in vL[1:]:
                vL = vS.split("|")
                if "<" in vL[0]:
                    varlS = vL[0].split("<=")[0].strip()
                    cmdS, descripS = self.v_rlookup(vS)
                    exec(cmdS, globals(), self.rivetD)
                    locals().update(self.rivetD)
                    tempS = cmdS.split("array")[1].strip()
                    tempS = eval(tempS.strip(")").strip("("))
                    if len(tempS) > 3:
                        trimL= tempS[:3]
                        trimL.append("...")
                    else:
                        trimL = tempS
                    valL.append([varlS, trimL, descripS]); continue
                if "#" in vL[0]:
                    varlS = vL[0].split("<=")[0].strip()
                    cmdS, descripS = self.v_clookup(vS)
                    exec(cmdS, globals(), self.rivetD)
                    locals().update(self.rivetD)
                    tempS = cmdS.split("array")[1].strip()
                    tempS = eval(tempS.strip(")").strip("("))
                    if len(tempS) > 3:
                        trimL= tempS[:3]
                        trimL.append("...")
                    else:
                        trimL = tempS
                    valL.append([varlS, trimL, descripS]); continue                
                varS = vL[0].split("=")[0].strip()
                valS = vL[0].split("=")[1].strip()
                arrayS = "array(" + valS + ")"
                descripS = vL[1].strip()
                cmdS = str(varS + " = " + arrayS + "   # " + descripS + "\n")
                pyS += cmdS
                exec(cmdS,globals(),self.rivetD)
                locals().update(self.rivetD)
                valL.append([varS, valS, descripS])
        elif ".py" in vpL[1]:
            tfileS = Path(self.folderD["spath"], vpL[1].strip())
            with open(tfileS,'r') as pyfile:
                readL = pyfile.readlines()
            for v in readL:
                vS = v.split("#")
                varS = vS[0].split("=")[0].strip()
                valS = vS[0].split("=")[1].strip()
                arrayS = "array(" + valS + ")"                
                descripS = vS[1].strip()
                cmdS = str(varS + " = " + arrayS + "   # " + descripS + "\n")
                exec(cmdS, globals(), self.rivetD)
                locals().update(self.rivetD)
                valL.append([varS, valS, descripS])
        else:
            print(vL[0]); self.calcS += vL[0] + "\n"
        
        df = pd.DataFrame(valL)               
        hdrL = ["variable", "value", "description"]
        old_stdout = sys.stdout
        output = StringIO()
        output.write(tabulate(df, tablefmt="grid", headers=hdrL, showindex=False))            
        valueS = output.getvalue()
        sys.stdout = old_stdout
        print(valueS +"\n"); self.calcS += valueS + "\n"
        self.exportS += pyS
        
        

    def v_rlookup(self, vS: str ):
        """assign row vector from csv file to variable
        
        Args:
            vS (string): value-string
        """
        
        locals().update(self.rivetD)
        
        varS = vS.split("<")[0].strip()
        descripS = vS.split("|")[1].strip()
        fileL = vS.split("<")[1].strip()
        fileS = fileL.split("[")[0].strip()
        rowS = vS.split("[")[1]
        rowI = int(rowS.split("]")[0].strip())
        fileP = os.path.join(self.folderD["tpath"], fileS)
        with open(fileP,'r') as csvf:
            reader = csv.reader(csvf)
            for i in range(rowI):
                rowL = next(reader)
            rowL = list(next(reader))
        cmdS = varS + "= array(" + str(rowL) + ")"

        return (cmdS, descripS)

    def v_clookup(self, vS: str ):
        """assign row vector from csv file to variable
        
        Args:
            vS (string): value-string
        """
        
        locals().update(self.rivetD)
        
        varS = vS.split("#")[0].strip()
        descripS = vS.split("|")[1].strip()
        fileL = vS.split("#")[1].strip()
        fileS = fileL.split("[")[0].strip()
        rowS = vS.split("[")[1]
        rowI = int(rowS.split("]")[0].strip())
        fileP = os.path.join(self.folderD["tpath"], fileS)
        with open(fileP,'r') as csvf:
            reader = csv.reader(csvf)
            for i in range(rowI):
                rowL = next(reader)
            rowL = list(next(reader))
        cmdS = varS + "= array(" + str(rowL) + ")"

        return (cmdS, descripS)

class E_utf:
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
        """parse strings of type equation
        
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
        tagL =  ["[page]_", "[line]_", "[r]_", "[rn]_", "[c]_",  
                            "[link]_", "[cite]_", "[foot]_"] 

        for eS in self.strL:
            eS = eS[4:].strip()                    # remove 4 space indent
            if len(eS.strip()) == 0:               # empty line                   
                print("\n"); self.calcS += "\n"; continue
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
                        str(self.setsectD["footqueL"][-1]) + "]" )
                    print(eS); self.calcS += eS + "\n"
                    incrI = self.setsectD["footqueL"][-1] + 1
                    self.setsectD["footqueL"].append(incrI)
                    continue
                elif any(tag in eS for tag in tagL):
                    self.calcS = _tags(eS, self.calcS, self.setsectD)
                    continue 
                else:
                    utfS = eS.replace("]_","]")
                    print(utfS); self.calcS += utfS + "\n"
                    continue
            print(eS); self.calcS += eS + "\n"     
        
        return (self.calcS, self.setsectD, self.rivetD, self.exportS)
    
    def e_symbol(self, eL: list):
        """[summary]
    
        Args:
            eL (list): list of equation plus parameters
        
        """
        locals().update(self.rivetD)
        
        eS =""""""
        eqS = eL[0].strip()

        eqnumI = int(self.setsectD["eqnum"]) + 1
        self.setsectD["eqnum"] = eqnumI
        eqnumS = (" [ " + str(self.setsectD["sectnum"]) + "." + 
                    str(self.setsectD["eqnum"]) + " ] ")
        utfS = eqnumS.rjust(self.setsectD["swidth"])
        print(utfS); self.calcS += utfS + "\n"  
        varS = eqS.split("=")[1].strip()
        resultS = eqS.split("=")[0].strip()
        spS = "Eq(" + resultS + ",(" + varS + "))" 
        #sps = sps.encode('unicode-escape').decode()
        try: utfS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        except: pass
        print(utfS); self.calcS += utfS + "\n"   

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

class T_utf:
    """Process table_strings to utf-calc

    Returns utf string of table results
    """
 
    def __init__(self, strL: list, folderD: dict, 
                        setcmdD: dict, setsectD: dict, rivetD: dict):       
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
        self.tcalc = []
        self.tlist = []

        try:
            plt.close()
        except:
            pass

    def t_parse(self) -> tuple:
        """compose utf calc string for values

        Return:
            vcalc (list): list of calculated strings
            local_dict (list): local() dictionary
        """
             
        tL = []; indxI = -1; ttmpL=[]
        tcmdL = ["read", "save", "data", "table", "plot", "image", "image2" ]
        attribL = [self.t_read, self.t_save, self.t_data, self.t_table,
                                self.t_plot, self.t_image, self.t_image2]
        tagL =  ["[page]_", "[line]_", "[r]_", "[rn ]_", "[c]_",  
                            "[link]_", "[cite]_", "[foot]_"] 

        for tS in self.strL:
            locals().update(self.rivetD)
            tS = tS[4:].strip()                         # remove 4 space indent
            if len(ttmpL) > 0:                          # call image or image2
                ttmpL.append(iS.strip())
                if indxI == 3:
                    self.t_image(ttmpL)
                    ttmpL =[]; indxI = -1; continue
                if len(ttmpL) == 5:
                    self.t_image2(ttmpL)
                    ttmpL =[]; continue
                else: continue
            if len(tS.strip()) == 0:                    # if empty line                   
                print("\n"); self.calcS += "\n"; continue      
            if tS[0:2] == "||":                         # command
                tL = tS[2:].split("|")
                callS = ((tL[0].split(":"))[0]).strip()
                print(100,callS)
                indxI = tcmdL.index(callS)            
                if tcmdL[indxI] == "image":
                    ttmpL = tL; continue
                if tcmdL[indxI] == "image2":
                    ttmpL = tL; continue                
                attribL[indxI](tL); continue            
            if "=" in tS:                               # equation
                utfS = tS.strip()
                exec(utfS)
                print(utfS); self.calcS += utfS + "\n"; continue       
            if tS[0] == "#" : continue                  # remove comment 
            if tS[0:2] == "::" : continue               # remove preformat 
            if "]_" in tS:                              # process a tag
                if "[#]_" in tS:
                    tS = tS.replace("[#]_", "[" + 
                        str(self.setsectD["footqueL"][-1]) + "]" )
                    print(tS); self.calcS += tS + "\n"
                    incrI = self.setsectD["footqueL"][-1] + 1
                    self.setsectD["footqueL"].append(incrI)
                    continue
            elif any(tag in tS for tag in tagL):
                self.calcS = _tags(tS, self.calcS, self.setsectD)
                continue 
            else:
                utfS = tS.replace("]_","]")
                print(utfS); self.calcS += utfS + "\n"
                continue       
        
        self.rivetD.update(locals())
        return (self.calcS, self.setsectD, self.rivetD, self.exportS)
       
    def t_read(self, tL: str) -> str:
        """[summary]
        
        Args:
            tl (str): [description]
        """
        locals().update(self.rivetD)
        
        df = tL[2].strip
        filename = tL[3].strip()
        pathname = Path(self.folderd["tpath"], filename).as_posix()
        exec(str(df) + "= pd.read_csv(" + str(pathname) + ")")     
        
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
        pathnameS =  Path(self.folderD["tpath"], filenameS ).as_posix()
        cmdlineS =  dfS + ".to_csv('" + str(pathnameS) +  "',index = False)"
        exec(cmdlineS)

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
        try:
            widthI = int(tL[0].split(":")[1])
        except:
            widthI = int(self.setcmdD["cwidth"])
        self.setcmdD.update({"cwidth":widthI})
        tableS = ""; utfS = ""
        files = tL[1].strip()
        tfiles = Path(self.folderD["tpath"], files)   
        tableI = self.setsectD["tablenum"] + 1
        self.setsectD.update({"tablenum":tableI})
        sectI = self.setsectD["sectnum"]
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
            old_stdout = sys.stdout
            output = StringIO()
            output.write(tabulate(format1, tablefmt="grid", headers="firstrow"))            
            utfS = output.getvalue()
            titleS = "  \n"
            sys.stdout = old_stdout
            try: titleS = tL[2].strip() + titleS
            except: pass        
        utfS = ("\nTable " + str(sectI)+'.' + str(tableI) + 
                        "  " + titleS ) + utfS                                              
        print(utfS); self.calcS += utfS + "\n"  

    def t_plot(self, tL: str)-> list:
        """[summary]
        
        Args:
            tLine (str): [description]
        """                
        tLa = tL.split("|")
        tLb = (tLa[1].strip()).split(" ")
        if len(tLb) > 1:
            self.pltname = tLb[1]
            filename = self.pltname + ".png"
            filepath = self.folderd["fpath"]
            self.pltfile = Path(filepath, filename).as_posix()
            pltcmd = tLa[2].strip()
            cmdline1 = "ax = plt.gca()"
            cmdline2 = self.pltname + ".plot(" + pltcmd + ", ax=ax)"
        else:
            pltcmd = tLa[2].strip()
            cmdline1 = ""
            cmdline2 = self.pltname + ".plot(" + pltcmd + ", ax=ax)"

        globals().update(locals())
        return cmdline1, cmdline2

    def t_image(self, tL: list):
        """insert image from fiLe
        
        Args:
            ipl (list): parameter list
        """
        try:
            scaleI = int(tL[0].split(":")[1])
        except:
            scaleI = self.setcmdD["scale1"]
        self.setcmdD.update({"scale1":scaleI})
        self.setsectD["fignum"] += 1
        figI = self.setsectD["fignum"]
        sectI = self.setsectD["sectnum"]
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
            scaleI= tL[0].split(":")[1]
            scale1I = int(scaleI.split(","))[0].strip()
            scale2I = int(scaleI.split(","))[1].strip()
            self.setcmdD.update({"scale1":scale1I})
            self.setcmdD.update({"scale2":scale2I})
        except:
            scale1I = self.setcmdD["scale1"]
            scale2I = self.setcmdD["scale2"]
        self.setsectD["fignum"] += 1                     # image 1
        figI = self.setsectD["fignum"]
        sectI = self.setsectD["sectnum"]
        files = tL[1].strip()
        captionS = tL[3].strip()
        imgP = str(Path(self.folderD["fpath"], files))
        utfS = ("Figure " + str(sectI) + '.' + str(figI) + "  "  
               + captionS + "\npath: " + imgP)
        print(utfS); self.calcS += utfS + "\n"

        self.setsectD["fignum"] += 1                     # image 2
        figI = self.setsectD["fignum"]
        sectI = self.setsectD["sectnum"]
        files = tL[2].strip()
        captionS = tL[4].strip()
        imgP = str(Path(self.folderD["fpath"], files))
        utfS = ("Figure " + str(sectI) + '.' + str(figI) + "  "  
               + captionS + "\npath: " + imgP)
        print(utfS); self.calcS += utfS + "\n"

