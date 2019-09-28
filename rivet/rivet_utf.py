#! python
import os
import sys

__version__ = "0.9.0"
__author__ = 'rholland@structurelabs.com'
      
class Rexec_u:
    """Process insert strings

    Returns utf calcs 
    """
 
    def __init__(self, vlist : list):
        """

        Args:
            slist (list): list of input parameters in string settings
            vlist (list): list of input lines in value string
            sectnum (int):  section number
        """

        self.rlist = rlist

    def r_utf(self):
        """compose utf calc string for values

        Return:
            vcalc (list): list of calculated strings
            local_dict (list): local() dictionary
        """
        pass

class Iexec_u:
    """Process insert strings

       Return formatted utf calcs 
    """
 
    def __init__(self, ilist: list, idict: dict, folders: dict, opt: dict ):
        """

        Args:
            slist (list): list of input parameters in string settings
            vlist (list): list of input lines in value string
            sectnum (int):  section number
        """

        self.ilist = ilist
        self.folders = folders
        self.idict = idict
        self.opt = opt
        self.icalc = []

    def i_line(self):
        self.icalc.append("\n" + "=" * _calcwidth + "\n")

    def i_str(self) -> tuple[dict, list]:
        """ compose utf calc string from insert-string
        
        Returns:
            tuple[dict, list]: locals dict, list of calc strings
        """
        icalc_temp = ""
        for iline in self.ilist:
            #print(iline)
            iline1 = iline.strip()
            if len(iline1) == 0:
                icalc.append("\n")
                continue
            if iline1[0] == "|":
                if ".txt" in iline1: i_txt()
                elif ".jpg" in iline1: i_fig(iline1)
                elif ".png" in iline1: i_fig(iline1)
                elif ".tex" in iline1: i_tex()
                elif ".rst" in iline1: i_csv()
                elif ".csv" in iline1: i_csv()
            else:
                self.icalc.append(iline1)

        return locals(), icalc

    def i_txt(self, iline1):
        """insert file from text into model
        """
        with open(fpath, 'r') as f1:
            txstrng = f1.readlines()
        if var1.strip() != '':
            instxt = eval('txstrng[' + var1.strip() + ']')
            instxt = ''.join(instxt)
        else:
            instxt = ''.join(txstrng)

        self._write_utf(instxt, 0)

        link1 = "< text inserted from file: " + str(fpath) + " >"
        self.ew.errwrite(link1, 1)
        self.ew.errwrite('', 0)

    def i_fig(self, iline1):
        """ insert figure reference in utf calc
        """        
        self.fignum += 1
        link1 = "< insert figure " + str(self.fignum) + '. ' \
                + " file: " + str(fpath) + '>'
        link2 = "Figure " + str(self.fignum) + '. ' + var1 \
                + " <file: " + str(fpath) + " >"
        self.icalc.append(link2)

        
    def i_tex(self,iline1):
        pass
    
    def i_csv(self, iline1):
        
        elif 'csv' in alinev[0]:                    # find [i] csv
            newaline = "  #" + aline
            modfile2.write(newaline)                # convert comment
            csvfile = alinev[1].strip()
            csvpath = os.path.join(tpath, csvfile)
            rsttab = csv2rst._run(csvpath,(0,0,0))
            rsttabv = rsttab.split("\n")                        
            rsttab2 ="\n"
            for _i in rsttabv:
                rsttab2 += "  " + _i + "\n"
            modfile2.write(rsttab2)                 # insert table
            continue

class Vexec_u:
    """Process value strings

    Returns utf value calcs 
    """
 
    def __init__(self, vlist : list, global1):
        """

        Args:
            vlist (list): list of input lines in value string
        """

        self.vlist = vlist
        globals().update(global1)
            
    def v_utf(self):
        """compose utf calc string for values

        Return:
            vcalc (list): list of calculated strings
            local_dict (list): local() dictionary
        """
        vcalc = []
        vcalc_eq = ""

        for vline in self.vlist:
            #print(vline)
            if "|" in vline:
                vcalc_eq = ""
                vline1 = vline.split("|")
                vcalc_eq = vline1[0].strip() 
                exec(vcalc_eq)
                vcalc.append(vcalc_eq + " | " + vline1[1].strip("|"))
            else:
                vcalc.append(vline.strip())

        return [locals(), vcalc]
        

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


