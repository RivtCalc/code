#! python
"""convert rivet strings to utf-8 calcs

This module converts each rivet string type to a utf-8 calc string using
a class for each string type. 

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
from IPython.display import Image as ipyImage, display
from tabulate import tabulate 
from pathlib import Path

def _parse_cmd(cmdS :str) -> list:
    """parse a command string
    
    Args:
        rivS (str): string type
        cmdS (str): command string
    
    List of commands by string type (notes in paranthesis):
    summary
    -------
    all : link, cite, foot
    repro : summary, labels, append
    insert : text, tex, sym, img, table  
    equation : format
    table : create, write, read, table, plot, add, save, img

    detail
    ------
    all strings
        || link | http link text
        || cite | (citation) text | citation description text   
        || foot | footnote description text

    r__('''r-string''') (repository and calc data)
        || summary | (toc) sections / functions  | (include) docstrings | 
            paragraph text
        || labels |
            csv list
        || append |          
            pdf file name, appendix title text
    i__('''i-string''') (insert text and images)
        || text | .txt file | (indent) i:n, (width) w:30 
        || tex  | latex equation text 
        || sym  | sympy equation text
        || img  | image file | (scale) s:1, (fig number) #:t(rue) (or) f(alse) |
            figure title text
        || table | inline | (table number) #:t(rue)/f(alse) |
            table title text
        || table | .rst file name | (table number) #:t/f |
            table title text
        || table | .csv file | (row)r:[], (col)c:[], (max width)m:30, #:t/f | 
            table title text
    v__('''v-string''') (define values)
    e__('''e-string''') (define equations)
        || format | (decimal)e:n, (result)r:n, (check)c:0, (print)p:0/1/2, #:t/f  
    t__('''t-string''') (define tables and plots)
        || table | .csv file | (row)r:[], (col)c:[], (max width)m:30, #:t/f | 
            table title text          
        || create| table name
        || write | .csv file name | table name 
        || read  | .csv file name | table name
        || img  | image file | (scale) s:1, (fig number) n:t(rue) (or) f(alse)
            figure title text        
        || plot | .csv file |(col names)x:col,y:col,(rows):[],(kind)k:line,(grid)g:t/f
        || add  | (col names) x:col, y:col, (color)c:blue        
        || save | file name (.png or .jpg) | plot name (base name .csv file)
    """
    
    cmdL = cmdS.split("|")
    if cmdL[0] == "text":
        pass
    elif cmdL[0] == "tex":
        pass
    elif cmdL[0] == "sym":
        pass
    elif cmdL[0] == "format":
        pass
    elif cmdL[0] == "create":
        pass
    elif cmdL[0] == "write":
        pass
    elif cmdL[0] == "read":
        pass
    elif cmdL[0] == "add":
        pass
    elif cmdL[0] == "save":
        pass
    elif cmdL[0] == "link":
        pass
    elif cmdL[0] == "repolink":
        pass
    elif cmdL[0] == "cite":
        pass
    elif cmdL[0] == "foot":
        pass
    elif cmdL[0] == "plot":
        pass
    elif cmdL[0] == "img":
        pass
    elif cmdL[0] == "table":
        pass
    else:
        pass

def _parse_tag(tagS: str):
    """parse tags
    
    Args:
        tagS (str): line from rivet string
    
    List of tags (notes in paranthesis):
    [abc]_      (citation name)   
    [#]_        (footnote number, # generates number) 
    [page]_     (new doc page)
    [line]_     (draw horizontal line)
    [r]_        (right justify line of text)
    [c]_        (center line of text)

    """
    if "[#]_" in tagS:
        pass
    elif "[page]_" in tagS:
        pass
    elif "[line]_" in tagS:
        pass
    elif "[r]_" in tagS:
        pass
    else:
        tag = re.search(r"\[.*?\]_", tagS)
        tagx = tag.group(0)
        modline = tagS.replace(" " + tagx,"")

def _clean_string(xS :str):


class RepoU:
    """convert repo-string to utf-calc string

    """
    def __init__(self, strL: list,  hdrD: dict, folderD: dict):
        """convert rivet string of type insert to utf-calc string
        
        Args:
            strl (list): rivet string
            folderd (dict): folder structure
            hdrd (dict): header information
        """

        self.calcL = []
        self.strL = strL
        self.folderD = folderD
        self.hdrD = hdrD

    def r_parse(self) -> list:
        """ parse repo string
       
       Returns:
            list :  formatted utf-calc strings
        """
        endflg = False
        rtmpL = []
        for rS in self.strL:
            if rS[0:2] == "##":  continue          # remove review comment
            rS = rS[4:]                            # remove 4 space indent
            if rS[0] == "# " : continue            # remove comment 
            if rS[0:2] == "::" : continue          # remove preformat 
            if len(rS.strip()) == 0: continue      # empty line
            if "]_" in rS:                         # find tags
                rS = _parse_tag(rS)
                self.calcL.append(rs) 
                continue
            if rS[0:2] == "||":                    # find command tag
                ipl = ils[2:].split("|")
                print(2, ipl)            
                if endflg:                          # append line to block
                    itmpl.append(ipl[0])
                    print(6, itmpl)
                    ipl = itmpl
                    endflg = False
                    itmpl = []
                if ils.strip()[-1] == "|":          # set block flag
                    endflg = True
                    itmpl = ipl
                    print(7, itmpl)
                    continue
                print(3, ipl[0])
                i_updateparams(ipl)                               
            if  rpl[0].strip() == "summary": self.i_txt(ipl)
            elif  rpl[0].strip() == "": self.i_img(ipl)
            elif  rpl[0].strip() == "table": self.i_table(ipl)
            elif  rpl[0].strip() == "tex": self.i_tex(ipl)
            elif  rpl[0].strip() == "sym": self.i_sym(ipl)
            elif "[#]" in ipl: self.i_footnote(ipl)
            elif "[#]_" in ipl: self.i_footnote(ipl)
            else: 
                self.calcl.append(ils.strip())
            continue    
        else:
            print(0, ils)
            self.calcl.append(ils)

        return self.calcl        

class InsertU:
    """convert rivet-string to utf-calc string 

    Attributes:
        strl (list): rivet string
        folderd (dict): folder structure
        hdrd (dict):  header information    
    """

    def __init__(self, strl: list,  hdrd: dict, folderd: dict):
        """convert rivet string of type insert to utf-calc string
        
        Args:
            strl (list): rivet string
            folderd (dict): folder structure
            hdrd (dict): header information
        """
        self.calcl = []
        self.strl = strl
        self.folderd = folderd
        self.hdrd = hdrd
        self.paramd = { "i":5, "w":40,
                        "s":1, "n":"t",
                        "r":"[:]", "c":"[:]", "m":30}

    def i_parse(self) -> list:
        """ parse insert string
       
       Returns:
            list :  formatted utf-calc strings
        """
        endflg = False
        itmpl = []
        for ils in self.strl:
            if ils[0:2] == "##":  continue          # remove review comment
            ils = ils[4:]                           # remove 4 space indent
            if len(ils.strip()) == 0:
                self.calcl.append(" ")              # blank line
                print(1, ils)
                continue
            if ils[0] == "#" : continue             # remove comment 
            if ils[0:2] == "::" : continue          # remove preformat 
            if ils[0:2] == "||":                    # find parse tag
                ipl = ils[2:].split("|")
                print(2, ipl)            
                if endflg:                          # append line to block
                    itmpl.append(ipl[0])
                    print(6, itmpl)
                    ipl = itmpl
                    endflg = False
                    itmpl = []
                if ils.strip()[-1] == "|":          # set block flag
                    endflg = True
                    itmpl = ipl
                    print(7, itmpl)
                    continue
                print(3, ipl[0])
                i_updateparams(ipl)
                if  ipl[0].strip() == "text": self.i_txt(ipl)
                elif  ipl[0].strip() == "img": self.i_img(ipl)
                elif  ipl[0].strip() == "table": self.i_table(ipl)
                elif  ipl[0].strip() == "tex": self.i_tex(ipl)
                elif  ipl[0].strip() == "sym": self.i_sym(ipl)
                elif "[#]" in ipl: self.i_footnote(ipl)
                elif "[#]_" in ipl: self.i_footnote(ipl)
                else: 
                    self.calcl.append(ils.strip())
                continue    
            else:
                print(0, ils)
                self.calcl.append(ils)

        return self.calcl

    def i_updateparams(self, ipl: list):
        """update process parameters from tag
        
        Args:
            ipl (list): [description]
        """
        try:
            paraml = ipl[2].split(",")
            for i in paraml:
                key = i.split(":")[0].strip() 
                self.paramd[key] = i.split(":")[1]
        except:
            pass

    def i_footnote(self, ipl: list):
        
        pass

    def i_txt(self, ipl: list):
        """insert text from file
        
        Args:
            ipl (list): parameter list
        """
        pars = ipl[2]
        txtpath = Path(self.folderd["xpath"] /  ipl[1].strip())
        with open(txtpath, 'r') as txtf1:
                utfs = txtf1.read()
        self.calcl.append(utfs)
        
        print(utfs)

    def i_img(self, ipl: list):
        """insert image from file
        
        Args:
            ipl (list): parameter list
        """
        self.hdrd["fignum"] += 1
        fign = self.hdrd["fignum"]
        sectn = self.hdrd["sectnum"]
        captions = ipl[4].strip()
        files = ipl[1].strip()
        pars = ipl[2].strip()
        paths = str(Path(self.folderd["fpath"], files))
        utfs = ("Figure " + str(sectn) + '.' + str(fign) + "  "  
               + captions + "\npath: " + paths )
        self.calcl.append(utfs)
        print(utfs)
        try:
            display(ipyImage(filename = paths))
        except:
            pass

    def i_tex(self,ipl: list):
        """insert formated equation from LaTeX string
        
        Args:
            ipl (list): parameter list

        """
        print(5, ipl)
        txs = ipl[1].strip()
        #txs = txs.encode('unicode-escape').decode()
        ltxs = parse_latex(txs)
        utfs = sp.pretty(sp.sympify(ltxs, _clash2, evaluate=False))
        self.calcl.append(utfs)    
        print(utfs)

    def i_sym(self,ipl):
        """insert formated equation from SymPy string 
        
        Args:
            ipl (list): parameter list
        """
        #print(ipl)
        pars = ipl[2]
        sps = ipl[1].strip()
        spl = sps.split("=")
        sps = "Eq(" + spl[0] +",(" + spl[1] +"))" 
        #sps = sps.encode('unicode-escape').decode()
        utfs = sp.pretty(sp.sympify(sps, _clash2, evaluate=False))
        self.calcl.append(utfs)   
        print(utfs)
            
    def i_table(self, ipl):
        """insert table from inline or csv, rst file 
        
        Args:
            ipl (list): parameter list
        """       
        table = ""
        tfiles = ipl[1].strip()
        filep = Path(self.folderd["tpath"], tfiles)   
        self.hdrd["tablenum"] += 1
        tablenum = self.hdrd["tablenum"]
        sectnum = self.hdrd["sectnum"]
        utfs = "\n"

        if ".csv" in ipl[1]:                        # csv file       
            parse1 = []
            rowcol = ipl[2].strip().split("c")
            rowl = rowcol[0].strip("r")
            col = rowcol[1].split("w")[0]
            width = rowcol[1].split("w")[1]
            with open(filep,'r') as csvf:
                readl = list(csv.reader(csvf))
            readl = eval("readl" + rowl)
            for row in readl:
                xrow = []
                for j in eval(col):
                    xrow.append(row[j])
                wrow=[]
                for i in xrow:
                    templist = textwrap.wrap(i, int(width)) 
                    wrow.append("""\n""".join(templist))
                parse1.append(wrow)
            old_stdout = sys.stdout
            output = StringIO()
            output.write(tabulate(parse1, tablefmt="grid", headers="firstrow"))            
            utfs = output.getvalue()
            titles = "  \n"
            sys.stdout = old_stdout
            try: titles = ipl[4].strip() + titles
            except: pass
        elif ".rst" in ipl[1]:                        # rst file
            with open(filep,'r') as rstf1: 
                utfs = rstf1.read()
            titles = "  \n"
            try: titles = ipl[3].strip() + titles
            except: pass
        else:                                       # inline reST table 
            utfs = ""
            titles = "  "
            try: titles = ipl[1].strip() + titles
            except: pass

        utfs = ("\nTable " + str(sectnum)+'.' + str(tablenum) + 
                        "  " + titles ) + utfs                                              
        self.calcl.append(utfs)
        print(utfs)     

class ValueU:
    """convert rivet string of type value to utf-calc string

    """
 
    def __init__(self, strl: list,  hdrd: dict, folderd: dict, 
                                        rivetd: dict, equl: list):
        """convert rivet string of type value to utf-calc string
        
        Args:
            strl (list): rivet strings
            hdrd (dict): header information
            folderd (dict): folder structure
            rivetd (dict) : rivet calculation variables
            equl (list) : equations for export
        """
        self.calcl = []
        self.strl = strl
        self.folderd = folderd
        self.hdrd = hdrd
        self.equl = equl
        self.rivetd = rivetd
          
    def v_parse(self)-> tuple:
        """parse strings of type value

        Return:
            calcl (list): utf formatted calc strings
            rivetd (list): local() dictionary
        """
        locals().update(self.rivetd)

        endflg = False
        itmpl = []
        for vls in self.strl:
            if vls[0:2] == "##":  continue          # remove review comment
            vls = vls[4:]                           # remove 4 space indent
            if len(vls.strip()) == 0:
                self.calcl.append(" ")              # insert blank line
                print(21, vls)
                continue
            if vls[0] == "#" : continue             # remove comment 
            if vls[0:2] == "::" : continue          # remove preformat 
            if "|" in vls:                          # act on parse tag
                vpl = vls.split("|")
                if "=>" in vpl[0]: 
                    self.v_lookup(vpl)              # assign vector 
                elif ":" in vpl[0]:
                    self.v_reprint(vpl)             # reprint a value
                else: self.v_assign(vpl)            # assign a value
            else: 
                self.calcl.append(vls)
                print(vls)

        self.rivetd.append(locals())

        return (self.calcl, self.rivetd, self.equl)
        
    def v_assign(self, vpl: list):
        """assign value to variable
        
        Args:
            vpl (list): list of value string components
        """
        
        locals().update(self.rivetd)

        pys = str(vpl[0]) + "# " + vpl[1].strip()
        vl = vpl[0].split("=")[1].strip()
        exec(vpl[0].strip())
        chkl = ""
        if "[" in vl:
            chkl = vl.split("[")[0].strip()
            evalx = eval(chkl) 
            if isinstance(evalx, list):
                exts = str(vpl[0]).strip() + " = " + str(eval(vl))
                utfs = str.ljust(exts,40) + " | " + vpl[1].strip()
        else:
            utfs =  str.ljust(str(vpl[0]).strip(),40) + " | " + vpl[1].strip()
        
        self.equl.append(pys)
        self.calcl.append(utfs)
        self.rivetd.update(locals())
        
        print(utfs)


    def v_lookup(self, vpl: list):
        """assign vector from csv file to variable
        
        Args:
            vpl (list): list of value string items
        """
        
        locals().update(self.rivetd)
        
        files1 = vpl[0].split("=>")[0]
        files2 = files1.split("[")[0].strip()
        rows = files1.split(".csv")[1].strip()
        filep = os.path.join(self.folderd["tpath"], files2)

        with open(filep,'r') as csvf:
            readl = list(csv.reader(csvf))
        rowl = eval("readl" + rows)

        vars = vpl[0].split("=>")[1].strip()
        cmds = vars + "=" + str(rowl)
        exec(cmds)
        utfs = str.ljust(vpl[0].strip(),40) + " | " + vpl[1].strip()

        self.calcl.append(utfs)
        self.rivetd.update(locals())

        print(utfs)
    
    def v_reprint(self, vpl: list):
        """reprint a variable value
        
        Args:
            vpl (list): list of value string items
        """

        vars = vpl[0].split(":")[0].strip()
        ans = str(eval(vars))
        utfs = str.ljust(vars + " = " + ans, 40) + " | " + vpl[1].strip()

        print(utfs)

class EquationU:
    """Convert rivet string type **equation** to utf-calc string

    """

    def __init__(self, strl: list,  hdrd: dict, folderd: dict, 
                                        rivetd: dict, equl: list):     
        """convert rivet string type **equation** to utf-calc string
        
        Args:
            strl (list): rivet strings
            hdrd (dict): header information
            folderd (dict): folder structure
            rivetd (dict) : rivet calculation variables
            equl (list) : equations for export
        """
        self.calcl = []
        self.strl = strl
        self.folderd = folderd
        self.hdrd = hdrd
        self.equl = equl
        self.rivetd = rivetd
        self.paramd = { "e":2,"r":2,"c":0, "p":2, "n":"t"}

    def e_parse(self) -> tuple:
        """parse strings of type equation
        
        Return:
            ecalc (list): list of calculated equation lines
            local_dict (list): local() dictionary
        """
        locals().update(self.rivetd)                
        endflg = False
        etmpl = []                                  # block string

        for els in self.strl:
            if els[0:2] == "##":  continue          # remove review comment
            els = els[4:]                           # remove 4 space indent
            if len(els.strip()) == 0:
                self.calcl.append(" ")              # blank line
                print(" "); continue
            if els[0] == "#" : continue             # remove comment 
            if els[0:2] == "::" : continue          # remove preformat 
            if "=" in els:                          # find parse tag
                epl = els.split("|")
                print(32, epl)            
                if endflg:                          # append line to block
                    etmpl.append(epl[0]); epl = etmpl
                    print(36, etmpl)
                    endflg = False; etmpl = []
                if els.strip()[-1] == "|":          # set block flag
                    endflg = True
                    etmpl = epl
                    print(35, etmpl); continue
                print(37, epl[0,1])
                e_updateparams(epl[1].strip())
                exec(epl[0].strip())                # exec equation
                if self.paramd["p"] == 1:
                    eq_symbol(epl,1)
                if self.paramd["p"] == 2:
                    eq_symbol(epl,2)
            else:
                print(39, els)
                self.calcl.append(els)

        self.rivetd.update(locals())
        return self.calcl

    def e_updateparams(self, eps: string):
        """update process parameters from tag
        
        Args:
            eps (string): equation print parameters
        """
        try:
            paraml = eps.split(",")
            for i in paraml:
                key = i.split(":")[0].strip() 
                self.paramd[key] = i.split(":")[1]
        except:
            pass
        eformat = self.paramd["e"]
        rformat = self.paramd["r"]
        exec("set_printoptions(precision=" + eformat.strip() + ")")
        exec("Unum.VALUE_FORMAT = '%." + eformat.strip() + "f'")

    def eq_symbol(self, epl: list, flag: int):
        """[summary]
        
        Args:
            epl (list): [description]
        """
        locals().update(self.rivetd)
        utfs = epl[0].strip(); descrips = epl[3]; pard = dict(epl[1])
        vars = utfs.split("=")
        results = vars[0].strip() + " = " + str(eval(vars[1]))
        eqnums = (" [ " + self.paramd["sectnum"] + "." + 
                                self.paramd["eqnum"] + " ] ")
        print(" "); self.calcl.append(" ") 
        ehdr = (descrips + " [ " + results + " ] " + 
            " [ " + eqnums + " ] ").rjust(self.paramd["swidth"])
        print((ehdr)); self.calcl.append("ehdr") 
        print(" "); self.calcl.append(" ")       
        try: 
            eps = "Eq(" + epl[0] +",(" + epl[1] +"))" 
            #sps = sps.encode('unicode-escape').decode()
            utfs = sp.pretty(sp.sympify(eps, _clash2, evaluate=False))
            print(utfs); self.calcl.append(utfs)
        else:
            print(utfs); self.calcl.append(utfs)

        try: self.equl.append(" # " + epl[3].strip())       # export eq to py
        except: pass
        self.equl.append(epl[0].strip())
        self.rivetd.update(locals())
        if flag == 2: eq_sub(epl, eps)      # substitute variable with number
        if pard["c"] != 0: eq_chk(results, pard["c"])   # check result

    def eq_sub(self, epl: list, eps: str):

        locals().update(self.rivetd)
        utfs = epl[0].strip(); descrips = epl[3]; pard = dict(epl[1])
        vars = utfs.split("=")
        results = vars[0].strip() + " = " + str(eval(vars[1]))
        try: 
            eps = "Eq(" + epl[0] +",(" + epl[1] +"))" 
            #sps = sps.encode('unicode-escape').decode()
            utfs = sp.pretty(sp.sympify(eps, _clash2, evaluate=False))
            print(utfs); self.calcl.append(utfs)
        else:
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

        typev = type(eval(var0))                # print result right justified
        if typev == ndarray:
            tmp1 = eval(var0)
            self._write_utf((var0 + " = "), 1, 0)
            self._write_utf(' ', 0, 0)
            self._write_utf(tmp1, 0, 0)
        elif typev == list or typev == tuple:
            tmp1 = eval(var0)
            self._write_utf((var0 + " = "), 1)
            self._write_utf(' ', 0)
            plist1 = ppr.pformat(tmp1, width=40)
            self._write_utf(plist1, 0, 0)
        elif typev == Unum:
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
        tmp = int(self.widthc-2) * '-'           # print horizontal line
        self._write_utf((u'\u2514' + tmp + u'\u2518').rjust(self.widthc), 1, 0)
        self._write_utf(" ", 0, 0)

        self.equl.append(pys)
        self.calcl.append(utfs)
        self.rivetd.update(locals())

    def eq_chk(results, compare):
        pass

class TableU:
    """Process table_strings to utf-calc

    Returns utf string of table results
    """
 
    def __init__(self, tlist: list, rivet_dict: dict, \
                     folders: dict, strnum: list):    
        """

        Args:
            tlist (list): list of input lines in table string
        """
        self.rivet = rivet_dict
        self.tcalc = []
        self.tlist = tlist
        self.folderd = folders
        self.maxwidth = strnum[0]
        self.sectnum = strnum[1]
        self.eqnum = strnum[2]
        self.fignum = strnum[3]
        self.pltfile = ""
        self.pltname = ""

        try:
            plt.close()
        except:
            pass

    def t_str(self) -> tuple:
        """compose utf calc string for values

        Return:
            vcalc (list): list of calculated strings
            local_dict (list): local() dictionary
        """
        locals().update(self.rivet)

        if ".xlsx" in ipl[2]:                   # excel file
            df = pd.read_excel(filep, usecols = lambda x: x in list(col), 
                            skiprows = lambda x: x not in list(rowl))
            old_stdout = sys.stdout
            output = StringIO()
            output.write(tabulate(df, tablefmt="grid", headers="firstrow"))            
            table1 = output.getvalue()
            sys.stdout = old_stdout
            #self.icalc.append("\n" + str(data1) + "\n")
        else:
            pass
        
        for tline in self.tlist:
            globals().update(locals())
            tline1 = tline[4:]
            if len(tline1.strip()) == 0:
                self.tcalc.append("\n")
                continue
            exstr = ""
            if "|" == tline1[0]: 
                if " read " in tline1[:8]:
                    exstr = self.t_read(tline1)
                elif " write " in tline1[:8]:
                    extstr = self.t_write(tline1)
                elif " create " in tline1[:8]:
                    exstr = self.t_create(tline1)
                elif " insert " in tline1[:10]:
                    self.t_insert(tline1)
                elif " plot " in tline1[:8]:
                    cmd1, cmd2 = self.t_plot(tline1)
                    exec(cmd1)
                    exec(cmd2)
                    plt.savefig(self.pltfile)
                else:
                    self.tcalc.append(tline1)
                exec(exstr)
                continue
            if "=" in tline1:
                tline1a = tline1.split("|")
                if len(tline1a) > 1:
                    tcalc_eq = ""
                    tcalc_eq = tline1a[0].strip() 
                    exec(tcalc_eq)
                    self.tcalc.append(tcalc_eq + " | " + tline1a[1])        
                else:
                    exec(tline1a[0])
                    self.tcalc.append(tline1a)
            else: 
                self.tcalc.append(tline1)
        
        eq1 = []
        return locals(), self.tcalc, eq1
       
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

    def t_write(self, tline1: str) -> str:
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

    def t_create(self, tline1:str) -> str:
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

    def t_insert(self, tline1: str):
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
