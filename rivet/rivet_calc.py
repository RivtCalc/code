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

detail
------
r__('''r-string''') {repository and calc data}
    || summary | {toc} sections / functions  | {include} docstrings  
        {paragraph text}
    || labels 
        {csv list}
    || append           
        x.pdf {pdf file name}, {appendix title text}
    || link | http:\\www.x {link text}
i__('''i-string''') {insert text and images}
    || text | x.txt {text file} | {indent n} i:n, (max width) w:65 
    || tex  | {latex equation text}
    || sym  | {sympy equation text}
    || img  | x.png/x.jpg {image file} | {scale} s:1, {fig number} #:t(rue)/f(alse) 
        figure title text
    || table | inline | {table number} #:t{rue}/f{alse} 
        table title text
    || table | x.rst {file name} | {table number} #:t/f 
        table title text
    || table | n.csv {file name} | {row}r:[], {col}c:[], {max width}m:30, #:t/f  
        table title text
    || link | {http link text}
    || cite | {citation text} | citation description text   
    || foot | footnote description text
v__('''v-string''') {define values}
e__('''e-string''') {define equations}
    || format | {decimals}e:n, {result}r:n, {check}c:0, {print}p:0/1/2, #:t/f  
t__('''t-string''') (define tables and plots)
    || create| table name
    || write | .csv file name | table name 
    || read  | .csv file name | table name
    || plot | f.csv {file name} |(col names)x:c1,y:c2,(rows)r:[],(kind)k:line,(grid)g:t/f
    || add (data to plot) | (col names) x:c3, y:c4, (color)c:blue        
    || save | n.png / n.jpg {file names} | f {name from plot command} 
    {plus all insert commands}

List of tags {notes in braces}:
------------------------------
    [abc]_      {citation name}   
    [#]_        {# generates footnote number) 
    [page]_     {new doc page)
    [line]_     {draw horizontal line)
    [r]_        {right justify line of text)
    [c]_        {center line of text)
"""
import os
import sys
import csv
import textwrap
import subprocess
import tempfile
import re
import io
from io import StringIO
from numpy import *
import numpy.linalg as la
import pandas as pd
import sympy as sp
from sympy.parsing.latex import parse_latex
from sympy.abc import _clash2
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
from tabulate import tabulate 
from pathlib import Path
from rivet.rivet_unit import *


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
            if "]_" in iS:                          # process a tag
                if "[#]_" in iS:
                    iS = iS.replace("[#]_", "[" + 
                        str(self.setsectD["footqueL"][-1]) + "]" )
                    print(iS); self.calcS += iS + "\n"
                    incrI = self.setsectD["footqueL"][-1] + 1
                    self.setsectD["footqueL"].append(incrI)
                    continue
            elif any(tag in iS for tag in tagL):
                self.calcS = _tags(iS, self.calcS, self.setsectD)
                continue 
            else:
                utfS = iS.replace("]_","]")
                print(utfS); self.calcS += utfS + "\n"
                continue    

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
        endflgB = False; itmpS = ""; iL = []; indxI = -1
        icmdL = ["sympy", "latex", "table", "image", "image2"]
        tagL =  ["[page]_", "[line]_", "[r]_", "[c]_", "[link]_", 
                                "[cite]_", "[foot]_"] 
        attribL =  [self.i_sympy, self.i_latex, self.i_table, 
                    self.i_image, self.i_image2]
        for iS in self.strL:
            iS = iS[4:]                            # remove 4 space indent
            if len(iS.strip()) == 0:               # if empty line                   
                if endflgB:                            # add next line 
                    iL.append(iS.strip())
                    attribL[indxI](iL)                  # call attribute from list                           
                    endflgB = False; itmpS = ""; iL = []; indxI = -1
                    continue
                print("\n"); self.calcS += "\n"; continue      
            if endflgB:
                iL.append(iS); continue
            if iS[0:2] == "||":                     # process a command
                iL = iS[2:].split("|")
                callS = ((iL[0].split(":"))[0]).strip()
                indxI = icmdL.index(callS)            
                endflgB = True; continue
            if iS[0] == "#" : continue              # remove comment 
            if iS[0:2] == "::" : continue           # remove preformat 
            if "]_" in iS:                          # process a tag
                if "[#]_" in iS:
                    iS = iS.replace("[#]_", "[" + 
                        str(self.setsectD["footqueL"][-1]) + "]" )
                    print(iS); self.calcS += iS + "\n"
                    incrI = self.setsectD["footqueL"][-1] + 1
                    self.setsectD["footqueL"].append(incrI)
                    continue
            elif any(tag in iS for tag in tagL):
                self.calcS = _tags(iS, self.calcS, self.setsectD)
                continue 
            else:
                utfS = iS.replace("]_","]")
                print(utfS); self.calcS += utfS + "\n"
                continue    

        return self.calcS, self.setsectD, self.setcmdD

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
        captionS = iL[2].strip()
        imgpathS = str(Path(self.folderD["fpath"], fileS))
        utfS = ("Figure " + str(sectI) + '.' + str(figI) + "  "  
               + captionS + "\npath: " + imgpathS + "\n")
        print(utfS+"\n"); self.calcS += utfS + "\n"

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

        endflgB = False; vL = []; indxI = -1
        vcmdL = ["values"]
        methodL =  [self.v_assign]

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
            if "]_" in iS:                          # process a tag
                if "[#]_" in iS:
                    iS = iS.replace("[#]_", "[" + 
                        str(self.setsectD["footqueL"][-1]) + "]" )
                    print(iS); self.calcS += iS + "\n"
                    incrI = self.setsectD["footqueL"][-1] + 1
                    self.setsectD["footqueL"].append(incrI)
                    continue
            elif any(tag in iS for tag in tagL):
                self.calcS = _tags(iS, self.calcS, self.setsectD)
                continue 
            else:
                utfS = iS.replace("]_","]")
                print(utfS); self.calcS += utfS + "\n"
                continue    
        
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
            for v in vL[1:]:
                vS = v.split("|")
                if "<=" in vS[0]:
                    varlS = vS[0].split("<=")[0].strip()
                    cmdS, descripS = self.v_lookup(v)
                    print(99,cmdS)
                    exec(cmdS, globals(), self.rivetD)
                    locals().update(self.rivetD)
                    tempS = cmdS.split("array")[1].strip()
                    tempS = eval(tempS.strip(")").strip("("))
                    print(90, len(tempS))
                    if len(tempS) > 3:
                        trimL= tempS[:3]
                        trimL.append("...")
                    else:
                        trimL = tempS
                        print(94)
                    valL.append([varlS, trimL, descripS])
                    continue
                varS = vS[0].split("=")[0].strip()
                valS = vS[0].split("=")[1].strip()
                arrayS = "array(" + valS + ")"
                descripS = vS[1].strip()
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
        
        

    def v_lookup(self, v: str ):
        """assign vector from csv file to variable
        
        Args:
            vpl (list): list of value string items
        """
        
        locals().update(self.rivetD)
        
        varS = v.split("<=")[0].strip()
        descripS = v.split("|")[1].strip()
        fileL = v.split("<=")[1].strip()
        fileS = fileL.split("[")[0].strip()
        rowS = v.split("[")[1]
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
    """Convert rivet string type **equation** to utf-calc string

    """

    def __init__(self, strL: list, folderD: dict, setcmdD: dict,
                setsectD: dict, rivetD: dict, exportS: str):     
        """convert rivet string type **equation** to utf-calc string
        
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

        endflgB = False; eL = []; indxI = -1
        ecmdL = ["equation", "func" ]
        attribL = [self.e_symbol, self.e_function]

        for eS in self.strL:
            eS = eS[4:].strip()                    # remove 4 space indent
            if len(eS.strip()) == 0:               # empty line                   
                if endflgB:                        # accumulate next line
                    eL.append(eS.strip())
                    attribL[indxI](eL)             # call attribute                           
                    if indxI ==1:
                        if self.setcmdD["sub"]:
                            e_sub(eL)
                        else:
                            e_table(eL)   
                    endflgB = False; etmpS = ""; eL = []; indxI = -1
                continue
                print("\n"); self.calcS += "\n"
            if endflgB:
                eL.append(eS.strip()); continue
            if "||" in eS:                         # command
                eL = eS[2:].split("|")
                callS = ((eL[0].split(":"))[0]).strip()
                indxI = ecmdL.index(callS)            
            if "=" in eS:                          # equation
                eL.append(eS.strip())
                callS = "equation"
                indxI = ecmdL.index(callS)         
                endflgB = True; continue            
            if eS[0] == "#" : continue             # remove comment 
            if eS[0:2] == "::" : continue          # remove preformat 
            if "]_" in iS:                          # process a tag
                if "[#]_" in iS:
                    iS = iS.replace("[#]_", "[" + 
                        str(self.setsectD["footqueL"][-1]) + "]" )
                    print(iS); self.calcS += iS + "\n"
                    incrI = self.setsectD["footqueL"][-1] + 1
                    self.setsectD["footqueL"].append(incrI)
                    continue
            elif any(tag in iS for tag in tagL):
                self.calcS = _tags(iS, self.calcS, self.setsectD)
                continue 
            else:
                utfS = iS.replace("]_","]")
                print(utfS); self.calcS += utfS + "\n"
                continue    
        
        return (self.calcS, self.setsectD, self.rivetD, self.exportS)
  
    def e_hdr(self):
        eqnumI = int(self.setsectD["eqnum"]) + 1
        self.setsectD["eqnum"] = eqnumI
        eqnumS = (" [ " + str(self.setsectD["sectnum"]) + "." + 
                    str(self.setsectD["eqnum"]) + " ] ")
        utfS = eqnumS.rjust(self.setsectD["swidth"])
        print(utfS); self.calcS += utfS + "\n"  
    
    def e_symbol(self, eL: list):
        """[summary]
    
        Args:
            eL (list): list of equation plus parameters
        
        """
        locals().update(self.rivetD)
        
        eS =""""""
        eqS = eL[0].strip()

        try:
            epS = eL[1].strip()                        # update command settings
            cmdD = dict(epS.split(":") for epS in epS.split(","))
            self.tmpD = self.setcmdD.update(cmdD)
            if tmpD["default"]:
                self.sectcmdD = tmpD
        except: pass
        
        if self.setcmdD["num"]:                     # add equation number
           self.e_hdr()                               
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
        locals().update(self.rivet)

        locals().update(self.rivetD)                

        endflgB = False; tL = []; indxI = -1
        ecmdL = ["read", "save", "data", "table", "plot", "image", "image2" ]
        attribL = [self.t_symbol, self.t_save, self.t_data, self.t_table,
                                self.t_plot, self.t_image, self.t_image2]

        for tS in self.strL:
            tS = tS[4:].strip()                    # remove 4 space indent
            if len(tS.strip()) == 0:               # empty line                   
                if endflgB:                        # accumulate next line
                    tL.append(tS.strip())
                    attribL[indxI](tL)             # call attribute                           
                    endflgB = False; ttmpS = ""; tL = []; indxI = -1
                continue
                print("\n"); self.calcS += "\n"
            if endflgB:
                eL.append(eS.strip()); continue
            if "||" in eS:                         # command
                eL = eS[2:].split("|")
                callS = ((eL[0].split(":"))[0]).strip()
                indxI = ecmdL.index(callS)            
            if "=" in eS:                          # equation
                eL.append(eS.strip())
                callS = "equation"
                indxI = ecmdL.index(callS)         
                endflgB = True; continue            
            if eS[0] == "#" : continue             # remove comment 
            if eS[0:2] == "::" : continue          # remove preformat 
            if "]_" in iS:                         # process a tag
                if "[#]_" in iS:
                    iS = iS.replace("[#]_", "[" + 
                        str(self.setsectD["footqueL"][-1]) + "]" )
                    print(iS); self.calcS += iS + "\n"
                    incrI = self.setsectD["footqueL"][-1] + 1
                    self.setsectD["footqueL"].append(incrI)
                    continue
            elif any(tag in iS for tag in tagL):
                self.calcS = _tags(iS, self.calcS, self.setsectD)
                continue 
            else:
                utfS = iS.replace("]_","]")
                print(utfS); self.calcS += utfS + "\n"
                continue       
        
        return (self.calcS, self.setsectD, self.rivetD, self.exportS)
       
    def t_read(self, tline1: str) -> str:
        """[summary]
        
        Args:
            tline1 (str): [description]
        """
        tline1a = tline1.split("|")
        temp1 = tline1a[1].split("read")
        temp2 = temp1[1].split("to")
        filename = temp2[0].strip() + ".csv"
        tablename = temp2[1].strip()
        pathname = Path(self.folderd["tpath"], filename).as_posix()
        cmdline = tablename + " = pd.read_table(" + '"' + \
                        pathname + '"' +", sep=',')" 
        
        df = pd.read_csv(csvfiles, usecols = lambda x: x in list(col), 
                       skiprows = lambda x: x in list(rowl))     
        globals().update(locals())        
        
        return cmdline

    def t_save(self, tline1: str) -> str:
        """[summary]
        
        Args:
            tline1 (str): [description]
        """
        tline1a = tline1.split("|")
        temp1 = tline1a[1].split("write")
        temp2 = temp1[1].split("to")
        filename = temp2[1].strip() + ".csv"
        tablename = temp2[0].strip()
        pathname =  Path(self.folderd["tpath"], filename ).as_posix()
        cmdline = tablename + ".to_csv(" +  '"' + \
                        pathname +  '"' + ", sep=',')"
        
        return cmdline

    def t_data(self, tline1:str) -> str:
        """[summary]
        
        Args:
            tline (str): [description]
        """
        tline1a = tline1.split("|")
        temp = tline1a[1].split("new")
        tablename = temp[1].strip()
        cmdline = tablename + " = pd.DataFrame()"
        
        globals().update(locals())
        return cmdline

    def t_table(self, tline1: str):
        """[summary]
        
        Args:
            tline (str): [description]
        """
        tline1a = tline1.split("|")
        if ("png" in tline1a[1]) or ("jpg" in tline1a[1]):
            plt.close()
            filename = tline1a[1].split("insert")[1].strip()
            filepath = self.folderd["fpath"]
            imgfile = Path(filepath, filename).as_posix()
            img = mpimg.imread(imgfile)
            imgplot = plt.imshow(img)
            plt.pause(0.5)
            plt.draw()
            plt.pause(2)
        else:       
            tablename = tline1a[1].split("insert")[1].strip()
            print("ti", tablename)
            tabletitle = tline1a[2] + "\n"
            tname = eval(tablename)
            old_stdout = sys.stdout
            output = StringIO()
            output.write(tabulate(tname, tablefmt="grid", headers="firstrow"))            
            rstout = output.getvalue()
            sys.stdout = old_stdout

            self.tcalc.append(tabletitle)
            self.tcalc.append(rstout)

            globals().update(locals())

    def t_plot(self, tline1: str)-> list:
        """[summary]
        
        Args:
            tline (str): [description]
        """                
        tline1a = tline1.split("|")
        tline1b = (tline1a[1].strip()).split(" ")
        if len(tline1b) > 1:
            self.pltname = tline1b[1]
            filename = self.pltname + ".png"
            filepath = self.folderd["fpath"]
            self.pltfile = Path(filepath, filename).as_posix()
            pltcmd = tline1a[2].strip()
            cmdline1 = "ax = plt.gca()"
            cmdline2 = self.pltname + ".plot(" + pltcmd + ", ax=ax)"
        else:
            pltcmd = tline1a[2].strip()
            cmdline1 = ""
            cmdline2 = self.pltname + ".plot(" + pltcmd + ", ax=ax)"

        globals().update(locals())
        return cmdline1, cmdline2
