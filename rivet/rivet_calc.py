#! python
"""convert rivet strings to utf-8 calcs

This module converts each rivet string type to a utf-8 calc string by means
of a class for each string type. 

"""
import os
import sys
import csv
import textwrap
import subprocess
import tempfile
import io
import re
import pandas as pd
import sympy as sp
from sympy.parsing.latex import parse_latex
from sympy.abc import _clash2
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
from IPython.display import Image as ipyImage, display
from tabulate import tabulate 
from pathlib import Path
from io import StringIO

class InsertU:
    """process rivet string of type insert to utf-calc string 

    Attributes:
        strl (list): rivet string
        folderd (dict): folder structure
        hdrd (dict):  header information    

    """

    def __init__(self, strl: list,  hdrd: dict, folderd: dict):
        """process rivet string of type insert to utf-calc string
        
        Arguments:
            strl (list): rivet string
            folderd (dict): folder structure
            hdrd (dict): header information
        """
        self.calcl = []
        self.strl = strl
        self.folderd = folderd
        self.hdrd = hdrd

    def i_parse(self) -> tuple:
        """ parse insert string
       
       Returns:
            list :  list of calc strings
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
                if  ipl[0].strip() == "text": self.i_txt(ipl)
                elif  ipl[0].strip() == "img": self.i_img(ipl)
                elif  ipl[0].strip() == "table": self.i_table(ipl)
                elif  ipl[0].strip() == "tex": self.i_tex(ipl)
                elif  ipl[0].strip() == "sym": self.i_sym(ipl)
                elif "[#]" in ipl: self.i_footnote(ipl)
                elif "[#]_" in ipl: self.i_footnote(ipl)
                else: self.calcl.append(ils.strip())
                continue    
            else:
                print(0, ils)
                self.calcl.append(ils)

        return self.calcl

    def i_footnote(self, iline1):
        
        pass

    def i_txt(self, ipl: list):
        """insert text from txt file
        
        Args:
            ipl (list): list of tag parameters
        """

        #print(ipl)
        texts=""
        txtpath = Path(self.folderd["xpath"] /  ipl[2].strip())
        if ".txt" in ipl[2] : 
            with open(txtpath, 'r') as txtf1:
                utfs = txtf1.read()
        self.calcl.append(utfs)
        print(utfs)

    def i_img(self, ipl: list):
        """ insert figure reference 
        """ 
        #print(ipl)
        self.hdrd["fignum"] += 1
        fign = self.hdrd["fignum"]
        sectn = self.hdrd["sectnum"]
        captions = ipl[4].strip()
        files = ipl[2].strip()
        patho = str(Path(self.folderd["fpath"], files))
        utfs = ("Figure " + str(sectn) + '.' + str(fign) + "  "  
               + captions + "\npath: " + str(patho) )
        self.calcl.append(utfs)
        print(utfs)
        try:
            display(ipyImage(filename = str(patho)))
        except:
            pass

    def i_tex(self,ipl: list):
        """insert formated equation from LaTeX string
        
        Arguments:
            ipl {list} -- parameters to insert tex equation from file

        """
        print(5, ipl)
        txs = ipl[2].strip()
        #txs = txs.encode('unicode-escape').decode()
        ltxs = parse_latex(txs)
        utfs = sp.pretty(sp.sympify(ltxs, _clash2, evaluate=False))
        self.calcl.append(utfs)    
        print(utfs)

    def i_sym(self,ipl):
        """insert formated equation from SymPy string 
        
        Arguments:
            ipl {list} -- parameters to insert tex equation from file
        """
        #print(ipl)
        sps = ipl[2].strip()
        spl = sps.split("=")
        sps = "Eq(" + spl[0] +",(" + spl[1] +"))" 
        #sps = sps.encode('unicode-escape').decode()
        utfs = sp.pretty(sp.sympify(sps, _clash2, evaluate=False))
        self.calcl.append(utfs)   
        print(utfs)
            
    def i_table(self, ipl):
        """insert formated equation from SymPy string 
        
        Arguments:
            ipl {list} -- parameters to insert tex equation from file
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

class Value_u:
    """Process value_strings to utf-calc

    Returns utf value calcs 
    """
 
    def __init__(self, vlist: list, rivet_dict: dict, \
                     folders: dict, strnum: list):    
        
        """

        Args:
            vlist (list): list of input lines in value string
        """

        self.rivet = rivet_dict
        self.vcalc = []
        self.eq1 = []
        self.vlist = vlist
        self.folderd = folders
        self.maxwidth = strnum[0]
        self.sectnum = strnum[1]
        self.eqnum = strnum[2]
        self.fignum = strnum[3]
            
    def v_str(self)-> tuple:
        """compose utf calc string for values

        Return:
            vcalc (list): list of calculated strings
            local_dict (list): local() dictionary
        """
        locals().update(self.rivet)
        
        for vline in self.vlist:
            if vline[0:2] == "##":          # filter out review comments
                continue
            vline1 = vline[4:]              # filter 4 space indent
            if len(vline1.strip()) == 0:
                self.vcalc.append("\n")
                continue
            if "|" == vline1[0]: 
                val1 = self.v_lookup(vline1)
                exec(val1)
                continue
            elif "|" in vline1: 
                val1 = self.v_assign(vline1)
                exec(val1)
            else: self.vcalc.append(vline1)

        return locals(), self.vcalc, self.eq1
        
    def v_assign(self, vline1: str) -> str:
        """[summary]
        
        Args:
            vline1 (str): [description]
        """
        vcalc_eq = ""
        vline2 = vline1.split("|")
        val1 = vline2[0].strip()
        self.eq1.append(vline2[1] + ", " + val1) 
        self.vcalc.append(val1 + " | " + vline2[1])

        return val1

    def v_lookup(self, vline1: str):
        """[summary]
        
        Args:
            vline1 (str): [description]
        """
        #print(vline1)
        vline1 = vline1.split("|")
        vfile1 = vline1[1].strip()
        rowcol1 = vline1[2].strip().split(",")
        unit1 = vline1[3].strip()
        var1 = rowcol1[0].strip()
        index1 = rowcol1[1].strip()
        label1 = rowcol1[2].strip()
        col1 = rowcol1[3].strip()
        
        csvfile1 = os.path.join(self.folderd["tpath"], vfile1)
        df = pd.read_csv(csvfile1, index_col =index1)
        data1 = df.loc[label1,col1]
        val1 = var1 + " = " + str(data1)
        val2 = val1 +  " | " + col1 + " of " + label1
        self.vcalc.append( val2 + "\n")

        return val1

class Equation_u:
    """Process equation_strings to utf-calc

    Returns utf equation calcs 
    """
    def __init__(self, elist: list, rivet_dict: dict, \
                     folders: dict, strnum: list):    
        """

        Args:
            elist (list): list of input lines in equation string
        """
        self.rivet = rivet_dict
        self.ecalc = []
        self.eq1 = []
        self.elist = elist
        self.folderd = folders
        self.maxwidth = strnum[0]
        self.sectnum = strnum[1]
        self.eqnum = strnum[2]
        self.fignum = strnum[3]
            
    def e_str(self):
        """compose utf calc string for equation
        
        Return:
            ecalc (list): list of calculated equation lines
            local_dict (list): local() dictionary
        """
        locals().update(self.rivet)
        ecalc_eq = ""
        ecalc_ans = ""
        descrip_flag = 0
        descrip1, unit1, sigfig1 = "equation", "", [2,2] 
        pad = ["","","",""]
        for eline in self.elist:
            #print(eline)
            if eline[0:2] == "##":          # filter out review comments
                continue
            eline = eline[4:]              # filter 4 space indent
            if len(eline1.strip()) == 0 :
                self.ecalc.append("\n")
            elif "|" in eline:
                descrip_flag = 1
                eline1 = (eline.strip()).split("|") + pad
                descrip2, unit2, sigfig2 = eline1[0:3]
                self.ecalc.append(descrip2.strip())
                #print("descrip", eline1)
            elif "=" in eline:
                ecalc_eq = eline.strip()
                if descrip_flag == 0:
                    descrip2, unit2, sigfig2 = descrip1, unit1, sigfig1
                exec(ecalc_eq)
                dep_var, ind_var = ecalc_eq.split("=")
                ecalc_ans = str(dep_var).strip() + " = " + str(eval(ind_var)).strip()
                self.ecalc.append(ecalc_eq)
                self.ecalc.append(ecalc_ans)
                self.eq1.append(descrip2 + ", " + ecalc_eq)
                ecalc_eq = ""
            else:
                self.ecalc.append(eline.strip())

        return locals(), self.ecalc, self.eq1

    def _prt_eq(self, dval):
        """ print equations.
            key : _e + line number  
            value:  p0  |  p1     |  p2   |   p3    |  p4  | p5   |  p6  |  p7       
                     var   expr    state    descrip   dec1  dec2   unit   eqnum
        
        """   
        try:                                                # set decimal format
            eformat, rformat = str(dval[4]).strip(), str(dval[5]).strip()
            exec("set_insertoptions(precision=" + eformat.strip() + ")")
            exec("Unum.VALUE_FORMAT = '%." + eformat.strip() + "f'")
        except:
            rformat = '3'
            eformat = '3'
            set_insertoptions(precision=3)
            Unum.VALUE_FORMAT = "%.3f"
        cunit = dval[6].strip()
        var0  =  dval[0].strip()
        #print('dval_e', dval
        for k1 in self.odict:                               # evaluate 
            if k1[0:2] in ['_v','_e']:
                    try: exec(self.odict[k1][2].strip())
                    except: pass       
        tmp = int(self.widthc-2) * '-'                      # print line
        self._write_utf(" ", 0, 0)
        self._write_utf((u'\u250C' + tmp + u'\u2510').rjust(self.widthc), 1, 0)
        self._write_utf((dval[3] + "  " + dval[7]).rjust(self.widthc-1), 0, 0)
        self._write_utf(" ", 0, 0)
        for _j in self.odict:                               # symbolic form
            if _j[0:2] in ['_v','_e']:
                #print(str(self.odict[_j][0]))
                varsym(str(self.odict[_j][0]))
        try:
            symeq = sympify(dval[1].strip())                # sympy form
            self._write_utf(symeq, 1, 0)
            self._write_utf(" ", 0, 0)
            self._write_utf(" ", 0, 0)
        except:
            self._write_utf(dval[1], 1, 0)                  # ASCII form
            self._write_utf(" ", 0, 0)
        try:                                                # substitute                            
            symat = symeq.atoms(Symbol)
            for _n2 in symat:
                evlen = len((eval(_n2.__str__())).__str__())  # get var length
                new_var = str(_n2).rjust(evlen, '~')
                new_var = new_var.replace('_','|')
                symeq1 = symeq.subs(_n2, symbols(new_var))
            out2 = pretty(symeq1, wrap_line=False)
            #print('out2a\n', out2)
            symat1 = symeq1.atoms(Symbol)       # adjust character length
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
            out3 = out2                             # clean up unicode 
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
            self._write_utf(out3, 1, 0)               # print substituted form
            self._write_utf(" ", 0, 0)
        except:
            pass
        for j2 in self.odict:                         # restore units
            try:
                statex = self.odict[j2][2].strip()
                exec(statex)
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

class Table_u:
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
