#! python
import os
import sys
import csv
import textwrap
import subprocess
import pandas as pd
from tabulate import tabulate 
from pathlib import Path
from typing import List, Set, Dict, Tuple, Optional
from io import StringIO


__version__ = "0.9.0"
__author__ = 'rholland@structurelabs.com'
      

class Iexec_u:
    """Process insert-strings

        Args:
            slist (list): list of input parameters in string settings
            vlist (list): list of input lines in value string
            sectnum (int):  section number

       Return formatted utf calcs 
    """

    def __init__(self, ilist: list, rivet_dict: dict, \
                     folders: dict, strnum: list):

        self.icalc = []
        self.ilist = ilist
        self.folders = folders
        self.maxwidth = strnum[0]
        self.sectnum = strnum[1]
        self.eqnum = strnum[2]
        self.fignum = strnum[3]

    def i_str(self) -> Tuple[dict, list]:
        """ compose utf calc string from insert-string
        
        Returns:
            tuple[dict, list]: locals dict, list of calc strings
        """
        icalc_temp = ""
        for iline in self.ilist:
            #print(iline)
            iline1 = iline[4:]
            if len(iline1.strip()) == 0:
                self.icalc.append("\n")
                continue
            if iline1[0] == "|":
                if ".txt" in iline1: self.i_txt(iline1)
                if ".jpg" in iline1: self.i_fig(iline1)
                if ".png" in iline1: self.i_fig(iline1)
                if  "["   in iline1: self.i_tex(iline1)
                if  "\\"  in iline1: self.i_tex(iline1)
                if ".rst" in iline1: self.i_rst(iline1)
                if ".csv" in iline1: self.i_csv(iline1)
                if "line" in iline1: self.i_line()
                else: pass
            else:
                self.icalc.append(iline1)

        eq1 = []
        return locals(), self.icalc, eq1

    def i_line(self):
        self.icalc.append("\n" + "=" * self.maxwidth + "\n")

    def i_txt(self, iline1):
        """insert text file into insert string

        """
        iline1 = iline1.split("|")
        txt1 = Path(self.folders["tpath"] /  iline1[1].strip())
        with open(txt1, 'r') as txtf1:
            txtstrng1 = txtf1.read()

        self.icalc.append(txtstrng1)

    def i_fig(self, iline1):
        """ insert figure reference in utf calc
        """ 
        self.fignum += 1
        iline1 = iline1.split("|")  
        caption1 = "  " + iline1[2].split("[[")[0]
        ref1 = ("Figure " + str(self.sectnum) + '.' + str(self.fignum)  
                + caption1 + "\nfile: " + str(self.folders["fpath"]))
        
        self.icalc.append(ref1)

    def i_tex(self,iline1):
        if "\\" in iline1:
            try:
                asciiform = subprocess.Popen(['perl', 'tex2uni.pl', iline1[1:]], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT)
            except:
                print("perl or tex2uni.pl not found - see user manual page x")
        if "[" in iline1:            
            try:
                eq_df = pd.read_csv(self.folders["spath"], skiprows = 1)
                rows = iline1.split("|")[1]
                for row in rows:
                    if "code" in iline1.split("|")[2]:
                        self.icalc.append(eq_df['code'][row] + 
                                " : " + eq_df['label'][row] + "\n")    
                    self.icalc.append(eq_df['ascii'][row] + "\n")
            except:
                pass

    def i_rst(self, iline1):
        iline1 = iline1.split("|")
        rstfile = os.path.join(self.folders["tpath"], iline1[1].strip())
        with open(rstfile,'r') as rstf1: 
            rstf2 = rstf1.read()
        self.icalc.append(rstf2)

    def i_csv(self, iline1):
        iline1 = iline1.split("|")
        maxcol =  iline1[2].split("[")[1].strip("]")
        csvfile = os.path.join(self.folders["tpath"], iline1[1].strip())
        parse1 = []
        with open(csvfile,'r') as csvf1:
            read1 = csv.reader(csvf1)
            for row in read1:
                for i in range(len(row)):
                    templist = textwrap.wrap(row[i], int(maxcol)) 
                    row[i] = """\n""".join(templist)
                parse1.append(row)
        
        old_stdout = sys.stdout
        output = StringIO()
        output.write(tabulate(parse1, tablefmt="grid", headers="firstrow"))            
        rstout = output.getvalue()
        sys.stdout = old_stdout

        self.icalc.append(rstout)

class Vexec_u:
    """Process value strings

    Returns utf value calcs 
    """
 
    def __init__(self, vlist: list, rivet_dict: dict, \
                     folders: dict, strnum: list):    
        
        """

        Args:
            vlist (list): list of input lines in value string
        """

        self.vcalc = []
        self.vlist = vlist
        self.folders = folders
        self.maxwidth = strnum[0]
        self.sectnum = strnum[1]
        self.eqnum = strnum[2]
        self.fignum = strnum[3]
            
    def v_str(self):
        """compose utf calc string for values

        Return:
            vcalc (list): list of calculated strings
            local_dict (list): local() dictionary
        """

        for vline in self.vlist:
            vline1 = vline[4:]
            if len(vline1.strip()) == 0:
                    self.vcalc.append("\n")
                    continue
            if "|" == vline1[0]:
                self.vcalc.append(vline1)
                continue
            if "|" in vline1:
                vcalc_eq = ""
                vline2 = vline1.split("|")
                vcalc_eq = vline2[0].strip() 
                exec(vcalc_eq)
                self.vcalc.append(vcalc_eq + " | " + vline2[1])
            else:
                self.vcalc.append(vline1)

        eq1 = []
        return locals(), self.vcalc, eq1
        

class Eexec_u:
    """Process equation strings

    Returns utf equation calcs 
    """
 
    def __init__(self, elist: list, global1: dict):
        """

        Args:
            elist (list): list of input lines in equation string
        """
        self.elist = elist
        globals().update(global1)
            
    def e_utf(self):
        """compose utf calc string for equation
        
        Return:
            ecalc (list): list of calculated equation lines
            local_dict (list): local() dictionary
        """
        ecalc = []
        ecalc_eq = ""
        ecalc_ans = ""
        descrip_flag = 0
        descrip1, unit1, sigfig1 = "equation", "", [2,2] 
        pad = ["","","",""]
        for eline in self.elist:
            #print(eline)
            if len(eline.strip()) == 0 :
                ecalc.append("\n")
            elif "|" in eline:
                descrip_flag = 1
                eline1 = (eline.strip()).split("|") + pad
                descrip2, unit2, sigfig2 = eline1[0:3]
                ecalc.append(descrip2.strip())
                #print("descrip", eline1)
            elif "=" in eline:
                ecalc_eq = eline.strip()
                if descrip_flag == 0:
                    descrip2, unit2, sigfig2 = descrip1, unit1, sigfig1
                exec(ecalc_eq)
                dep_var, ind_var = ecalc_eq.split("=")
                ecalc_ans = str(dep_var).strip() + " = " + str(eval(ind_var)).strip()
                ecalc.append(ecalc_eq)
                ecalc.append(ecalc_ans)
                ecalc_eq = ""
            else:
                ecalc.append(eline.strip())

        local_dict = locals()
        return [local_dict, ecalc]

    def _prt_eq(self, dval):
        """ print equations.
            key : _e + line number  
            value:  p0  |  p1     |  p2   |   p3    |  p4  | p5   |  p6  |  p7       
                     var   expr    state    descrip   dec1  dec2   unit   eqnum
        
        """   
        try:                                                # set decimal format
            eformat, rformat = str(dval[4]).strip(), str(dval[5]).strip()
            exec("set_printoptions(precision=" + eformat.strip() + ")")
            exec("Unum.VALUE_FORMAT = '%." + eformat.strip() + "f'")
        except:
            rformat = '3'
            eformat = '3'
            set_printoptions(precision=3)
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


class Texec_u:
    """Process table strings

    Returns utf calcs 
    """
 
    def __init__(self, tlist : list):
        """

        Args:
            slist (list): list of input parameters in string settings
            tlist (list): list of input lines in table string
            sectnum (int):  section number
        """

        self.tlist = tlist
            
    def t_utf(self):
        """compose utf calc string for equations

        Return:
            ecalc (list): list of calculated equation lines
            local_dict (list): local() dictionary
        """
        vcalc = []
        vcalc_temp = ""
        descrip_flag = 0

        for vline in self.vlist:
            #print(vline)
            if len(vline.strip()) == 0:
                vcalc.append("\n")
            elif descrip_flag == 1:
                vcalc.append(vcalc_temp + " | " + vline)
                vcalc_temp = ""
                descrip_flag = 0
            elif "=" in vline:
                exec(vline.strip())
                vcalc_temp = vline.strip()
                descrip_flag = 1
            else:
                vcalc.append(vline.strip() + "\n")

        local_dict = locals()
        return [local_dict, vcalc]


