#!python
"""converts rivt-strings to reST-strings

The OutputRST class converts rivt-strings to intermediate reST-strings which
may then be converted to pdf or html docs. """

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
from sympy.core.alphabets import greeks
from tabulate import tabulate
from pathlib import Path
from numpy import *
from IPython.display import display as _display
from IPython.display import Image as _Image

try:
    from PIL import Image as PImage
    from PIL import ImageOps as PImageOps
except:
    pass
from rivtcalc.rc_unit import *

logging.getLogger("numexpr").setLevel(logging.WARNING)


class OutputRST:
    """convert rivt-strings to reST strings"""

    def __init__(
        self,
        strL: list,
        folderD: dict,
        setcmdD: dict,
        setsectD: dict,
        rivtD: dict,
        exportS: str,
    ):

        """convert rivt-strings to reST-strings

        Args:
            exportS (str): stores values that are written to file
            strL (list): calc rivt-strings
            folderD (dict): folder paths
            setcmdD (dict): command settings
            setsectD (dict): section settings
            rivtD (dict): global rivt dictionary
        """

        self.restS = """"""  # restructured text string
        self.exportS = exportS  # value export string
        self.strL = strL  # rivt-string list
        self.valL = []  # value blocklist
        self.folderD = folderD
        self.setsectD = setsectD
        self.setcmdD = setcmdD
        self.rivtD = rivtD

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
        sfillS = str(self.setsectD["snumS"]).strip().zfill(2)
        cnumSS = str(self.setsectD["cnumS"])
        refS = typeS + cnumSS + "." + objfillS

        return refS

    def _tags(self, tagS: str, tagL: list) -> tuple:
        """parse tag

        Args:
            tagS (str): rivt-string with tag
            tagL (list): list of tag parameters
            setsectD (dict): section dictionary

        Return:
            rstS (str): restructured text string
            setsectD (dict): updated section dictionary
        """

        tagS = tagS.rstrip()
        uS = ""
        swidthI = self.setsectD["swidthI"] - 1
        try:
            tag = list(set(tagL).intersection(tagS.split()))[0]
        except:
            uS = tagS
            return uS

        if tag == "[#]_":  # auto increment footnote mark
            uS = tagS + "\n"
        elif tag == "[page]_":  # new page
            uS = ".. raw:: latex \n\n ?x?newpage \n"
        elif tag == "[line]_":  # horizontal line
            uS = int(self.setsectD["swidthI"]) * "-"
        elif tag == "[link]_":  # url link
            tgS = tagS.strip("[link]_").strip()
            tgL = tgS.split("|")
            uS = ".. _" + tgL[0].strip() + ": " + tgL[1].strip()
        elif tag == "[r]_":  # right adjust text
            tagL = tagS.strip().split("[r]_")
            uS = "?x?hfill " + tagL[0].strip()
        elif tag == "[c]_":  # center text
            tagL = tagS.strip().split("[c]_")
            uS = "?x?begin{center} " + tagL[0].strip() + "?x?end{center}"
        elif tag == "[x]_":  # format tex
            tagL = tagS.strip().split("[x]_")
            txS = tagL[0].strip()
            uS = ".. raw:: math\n\n   " + txS + "\n"
        elif tag == "[s]_":  # format sympy
            tagL = tagS.strip().split("[s]_")
            spS = tagL[0].strip()
            txS = sp.latex(S(spS))
            uS = ".. raw:: math\n\n   " + txS + "\n"
        elif tag == "[f]_":  # figure caption
            tagL = tagS.strip().split("[f]_")
            fnumI = int(self.setsectD["fnumI"]) + 1
            self.setsectD["fnumI"] = fnumI
            refS = self._refs(fnumI, "[ Fig: ") + " ]"
            uS = "**" + tagL[0].strip() + " ?x?hfill " + refS + "**?x?newline"
        elif tag == "[e]_":  # equation label
            tagL = tagS.strip().split("[e]_")
            enumI = int(self.setsectD["enumI"]) + 1
            self.setsectD["enumI"] = enumI
            refS = self._refs(enumI, "[ Equ: ")
            uS = "**" + tagL[0].strip() + " ?x?hfill " + refS + "**"
        elif tag == "[t]_":  # table label
            tagL = tagS.strip().split("[t]_")
            tnumI = int(self.setsectD["tnumI"]) + 1
            self.setsectD["tnumI"] = tnumI
            refS = self._refs(tnumI, "[Table: ") + "]"
            uS = "**" + tagL[0].strip() + " ?x?hfill  " + refS + "**"
        elif tag == "[foot]_":  # footnote label
            tagS = tagS.strip("[foot]_").strip()
            # ".. target-notes::\n\n"
            uS = ".. [*] " + tagS
        elif tag == "[n]_":  # new line
            tagL = tagS.strip().split("[n]_")
            tagS = tagL[0] + "\n"
            uS = tagS
        else:
            uS = tagS

        return uS

    def _parseRST(self, typeS: str, cmdL: list, methL: list, tagL: list):
        """parse rivt-string to reST

        Args:
            typeS (str): rivt-string type
            cmdL (list): command list
            methL (list): method list
            tagL (list): tag list
        """
        locals().update(self.rivtD)
        uL = []  # command arguments
        indxI = -1  # method index
        _rgx = r"\[([^\]]+)]_"  # find tags

        for uS in self.strL:
            if uS[0:2] == "##":
                continue  # remove comment
            uS = uS[4:]  # remove indent
            if len(uS) == 0:
                if len(self.valL) > 0:  # print value table
                    hdrL = ["variable", "value", "[value]", "description"]
                    alignL = ["left", "right", "right", "left"]
                    self._vtable(self.valL, hdrL, "rst", alignL)
                    self.valL = []
                    self.restS += "\n"
                    self.rivtD.update(locals())
                    continue
                else:
                    # self.restS += "?x?vspace{7pt}"
                    self.restS += "\n"
                    continue
            try:
                if uS[0] == "#":
                    continue  # remove comment
            except:
                self.restS += "\n"
                continue
            if uS.strip() == "[literal]_":
                continue
            if re.search(_rgx, uS):  # check for tag
                utgS = self._tags(uS, tagL)
                self.restS += utgS.rstrip() + "\n"
                continue
            if typeS == "values":  # chk for values
                self.setcmdD["saveB"] = False
                if "=" in uS and uS.strip()[-2] == "||":  # value to file
                    uS = uS.replace("||", " ")
                    self.setcmdD["saveB"] = True
                if "=" in uS:  # assign value
                    uL = uS.split("|")
                    self._vassign(uL)
                    continue
            if typeS == "table":  # check for table
                if uS[0:2] == "||":
                    uL = uS[2:].split("|")
                    indxI = cmdL.index(uL[0].strip())
                    methL[indxI](uL)
                    continue
                else:
                    exec(uS)
                    continue  # exec table code
            if uS[0:2] == "||":  # check for cmd
                # print(f"{cmdL=}")
                uL = uS[2:].split("|")
                indxI = cmdL.index(uL[0].strip())
                methL[indxI](uL)
                continue  # call any cmd

            self.rivtD.update(locals())
            if typeS != "table":  # skip table prnt
                self.restS += uS.rstrip() + "\n"

    def r_rst(self) -> str:
        """parse repository string

        Returns:
             rstS (list): utf formatted calc-string (appended)
             setsectD (dict): section settings
        """

        rcmdL = ["search", "keys", "info", "text", "table", "pdf"]
        rmethL = [
            self._rsearch,
            self._rkeys,
            self._rinfo,
            self._itext,
            self._itable,
            self._rpdf,
        ]
        rtagL = ["[links]_", "[literal]_", "[foot]_", "[#]__"]

        self._parseRST("repository", rcmdL, rmethL, rtagL)

        return self.restS, self.setsectD

    def _rsearch(self, rsL):
        a = 4

    def _rkeys(self, rsL):
        a = 4

    def _rinfo(self, rL):
        """insert tables or text from csv, xlsx or txt file

        Args:
            rL (list): parameter list

        Files are read from /docs/docfolder
        The command is identical to itable except file is read from docs/info.

        """
        alignD = {"s": "", "d": "decimal", "c": "center", "r": "right", "l": "left"}
        rtagL = [
            "[page]_",
            "[line]_",
            "[link]_",
            "[literal]_",
            "[foot]_",
            "[r]_",
            "[c]_",
            "[e]_",
            "[t]_",
            "[f]_",
            "[#]_",
        ]
        if len(rL) < 4:
            rL += [""] * (4 - len(rL))  # pad parameters
        rstS = ""
        contentL = []
        sumL = []
        fileS = rL[1].strip()
        tfileS = Path(self.folderD["dpath"] / "d0000" / fileS)
        extS = fileS.split(".")[1]
        if extS == "csv":
            with open(tfileS, "r") as csvfile:  # read csv file
                readL = list(csv.reader(csvfile))
        elif extS == "xlsx":
            xDF = pd.read_excel(tfileS, header=None)
            readL = xDF.values.tolist()
        else:
            return
        incl_colL = list(range(len(readL[0])))
        widthI = self.setcmdD["cwidthI"]
        alignS = self.setcmdD["calignS"]
        saS = alignD[alignS]
        if rL[2].strip():
            widthL = rL[2].split(",")  # new max col width
            widthI = int(widthL[0].strip())
            alignS = widthL[1].strip()
            saS = alignD[alignS]  # new alignment
            self.setcmdD.update({"cwidthI": widthI})
            self.setcmdD.update({"calignS": alignS})
        totalL = [""] * len(incl_colL)
        if rL[3].strip():  # columns
            if rL[3].strip() == "[:]":
                totalL = [""] * len(incl_colL)
            else:
                incl_colL = eval(rL[3].strip())
                totalL = [""] * len(incl_colL)
        ttitleS = readL[0][0].strip() + " [t]_"
        rstgS = self._tags(ttitleS, rtagL)
        self.restS += rstgS.rstrip() + "\n\n"
        for row in readL[1:]:
            contentL.append([row[i] for i in incl_colL])
        wcontentL = []
        for rowL in contentL:
            wrowL = []
            for iS in rowL:
                templist = textwrap.wrap(str(iS), int(widthI))
                templist = [i.replace("""\\n""", """\n""") for i in templist]
                wrowL.append("""\n""".join(templist))
            wcontentL.append(wrowL)
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate(
                wcontentL,
                tablefmt="rst",
                headers="firstrow",
                numalign="decimal",
                stralign=saS,
            )
        )
        rstS = output.getvalue()
        sys.stdout = old_stdout

        self.restS += rstS + "\n"

    def _rpdf(self, rsL):
        b = 5

    def i_rst(self) -> tuple:
        """parse insert-string

        Returns:
            calcS (list): utf formatted calc-string (appended)
            setsectD (dict): section settings
            setcmdD (dict): command settings
        """

        icmdL = ["text", "table", "image"]
        imethL = [
            self._itext,
            self._itable,
            self._iimage,
        ]
        itagL = [
            "[page]_",
            "[line]_",
            "[link]_",
            "[literal]_",
            "[foot]_",
            "[s]_",
            "[x]_",
            "[r]_",
            "[c]_",
            "[e]_",
            "[t]_",
            "[f]_",
            "[#]_",
        ]

        self._parseRST("insert", icmdL, imethL, itagL)

        return self.restS, self.setsectD, self.setcmdD

    def _itext(self, iL: list):
        """insert text from file

        Args:
            iL (list): text command list
        """
        calpS = "c" + self.setsectD["cnumS"]
        txapath = Path(self.folderD["cpath"] / calpS / iL[1].strip())
        with open(txapath, "r") as txtf1:
            rstL = txtf1.readlines()
        if iL[2].strip() == "indent":
            txtS = "".join(rstL)
            widthI = self.setcmdD["cwidth"]
            inS = " " * 4
            rstL = textwrap.wrap(txtS, width=widthI)
            rstL = [inS + S1 + "\n" for S1 in rstL]
            rstS = "".join(rstL)
        elif iL[2].strip() == "literal":
            txtS = " ".join(rstL)
            rstS = "::\n\n" + txtS + "\n"
        elif iL[2].strip() == "raw":
            txtS = "".join(rstL)
            rstS = "\n" + txtS
        else:
            txtS = "".join(rstL)
            rstS = "\n" + txtS

        self.restS += rstS + "\n"

    def _itable(self, iL: list):
        """insert table from csv or xlsx file

        Args:
            ipl (list): parameter list
        """
        alignD = {"s": "", "d": "decimal", "c": "center", "r": "right", "l": "left"}
        itagL = [
            "[page]_",
            "[line]_",
            "[link]_",
            "[literal]_",
            "[foot]_",
            "[r]_",
            "[c]_",
            "[e]_",
            "[t]_",
            "[f]_",
            "[#]_",
            "[n]_",
        ]
        if len(iL) < 4:
            iL += [""] * (4 - len(iL))  # pad parameters
        utfS = ""
        contentL = []
        sumL = []
        fileS = iL[1].strip()
        calpS = self.setsectD["fnumS"]
        tfileS = Path(self.folderD["cpath"] / calpS / fileS)
        extS = fileS.split(".")[1]
        if extS == "csv":
            with open(tfileS, "r") as csvfile:  # read csv file
                readL = list(csv.reader(csvfile))
        elif extS == "xlsx":
            tDF1 = pd.read_excel(tfileS, header=None)
            readL = tDF1.values.tolist()
        else:
            return

        incl_colL = list(range(len(readL[1])))
        widthI = self.setcmdD["cwidthI"]
        alignS = self.setcmdD["calignS"]
        saS = alignD[alignS]
        if iL[2].strip():
            widthL = iL[2].split(",")  # new max col width
            widthI = int(widthL[0].strip())
            alignS = widthL[1].strip()
            self.setcmdD.update({"cwidthI": widthI})
            self.setcmdD.update({"calignS": alignS})
            saS = alignD[alignS]  # new align
        totalL = [""] * len(incl_colL)
        if iL[3].strip():  # columns
            if iL[3].strip() == "[:]":
                totalL = [""] * len(incl_colL)
            else:
                incl_colL = eval(iL[3].strip())
                totalL = [""] * len(incl_colL)
        ttitleS = readL[0][0].strip() + " [t]_"
        utgS = self._tags(ttitleS, itagL)
        self.restS += utgS.rstrip() + "\n\n"
        for row in readL[1:]:
            contentL.append([row[i] for i in incl_colL])
        wcontentL = []
        for rowL in contentL:  # wrap columns
            wrowL = []
            for iS in rowL:
                templist = textwrap.wrap(str(iS), int(widthI))
                templist = [i.replace("""\\n""", """\n""") for i in templist]
                wrowL.append("""\n""".join(templist))
            wcontentL.append(wrowL)
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate(
                wcontentL,
                tablefmt="rst",
                headers="firstrow",
                numalign="decimal",
                stralign=saS,
            )
        )
        rstS = output.getvalue()
        sys.stdout = old_stdout

        # print(rstS)
        self.restS += rstS + "\n"

    def _iimage(self, iL: list):
        """insert one or two images from file

        Args:
            il (list): image parameters
        """
        rstS = ""
        dfoldS = "d" + self.setsectD["cnumS"]
        fileS = iL[1].split(",")
        file1S = fileS[0].strip()
        fileS = iL[1].split(",")
        file1S = fileS[0].strip()
        img1S = str(Path(self.folderD["docpath"], dfoldS, file1S).as_posix())
        scaleF = iL[2].split(",")
        scale1S = str(float(scaleF[0])) + " %"
        self.setcmdD.update({"scale1F": scale1S})
        if "," in iL[1]:  # two images
            scale2S = str(float(scaleF[1])) + " %"
            self.setcmdD.update({"scale2F": scale2S})
            file2S = fileS[1].strip()
            img2S = str(Path(self.folderD["docpath"] / dfoldS / file2S).as_posix())
            rstS += (
                "|pic1|  |pic2| "
                + "\n\n"
                + ".. |pic1| image:: "
                + img1S
                + "\n"
                + "   :width: "
                + scale1S
                + "\n\n"
                + ".. |pic2| image:: "
                + img2S
                + "\n"
                + "   :width: "
                + scale2S
                + "\n"
            )
        else:  # one image
            rstS += (
                ".. image:: "
                + img1S
                + "\n"
                + "   :width: "
                + scale1S
                + "\n"
                + "   :align: left \n"
            )

        self.restS += rstS + "\n"

    def v_rst(self) -> tuple:
        """parse value-string and set method

        Return:
            calcS (list): utf formatted calc-string (appended)
            setsectD (dict): section settings
            setcmdD (dict): command settings
            rivtD (list): calculation results
            exportS (list): value strings for export
        """

        locals().update(self.rivtD)
        vcmdL = ["config", "value", "data", "func", "text", "table", "image"]
        vmethL = [
            self._vconfig,
            self._vvalue,
            self._vdata,
            self._vfunc,
            self._itext,
            self._itable,
            self._iimage,
        ]

        vtagL = [
            "[page]_",
            "[line]_",
            "[link]_",
            "[literal]_",
            "[foot]_",
            "[s]_",
            "[x]_",
            "[r]_",
            "[c]_",
            "[e]_",
            "[t]_",
            "[f]_",
            "[#]_",
        ]

        self._parseRST("values", vcmdL, vmethL, vtagL)
        self.rivtD.update(locals())
        return self.restS, self.setsectD, self.setcmdD, self.rivtD, self.exportS

    def _vconfig(self, vL: list):
        """update dictionary format values

        Args:
            vL (list): configuration parameters
        """

        if vL[1].strip() == "sub":
            self.setcmdD["subB"] = True
        self.setcmdD["trmrI"] = vL[2].split(",")[0].strip()
        self.setcmdD["trmtI"] = vL[2].split(",")[1].strip()

    def _vassign(self, vL: list):
        """assign values to variables and equations

        Args:
            vL (list): list of assignments
        """

        locals().update(self.rivtD)
        if len(vL) <= 2:  # equation
            unitL = vL[1].split(",")
            unit1S, unit2S = unitL[0].strip(), unitL[1].strip()
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            val1U = val2U = array(eval(valS))
            if unit1S != "-":
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS
                    exec(cmdS, globals(), locals())
                    valU = eval(varS).cast_unit(eval(unit1S))
                    val1U = str(valU.number()) + " " + str(valU.unit())  # case=1
                    val2U = valU.cast_unit(eval(unit2S))
            utfS = vL[0]
            spS = "Eq(" + varS + ",(" + valS + "))"  # pretty prnt
            try:
                rstS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
            except:
                pass
            self.restS += "\n" + rstS + "\n"
            eqS = sp.sympify(valS)
            eqatom = eqS.atoms(sp.Symbol)
            if self.setcmdD["substB"]:
                self._vsub(vL)
            else:
                hdrL = []
                valL = []
                hdrL.append(varS)
                hdrL.append("[" + varS + "]")
                valL.append(str(val1U))
                valL.append(str(val2U))
                for sym in eqatom:
                    hdrL.append(str(sym))
                    valL.append(eval(str(sym)))
                alignL = ["center"] * len(valL)
                self._vtable([valL], hdrL, "rst", alignL)
            if self.setcmdD["saveB"] == True:
                pyS = vL[0] + vL[1] + "  # equation" + "\n"
                # print(pyS)
                self.exportS += pyS
            locals().update(self.rivtD)
        elif len(vL) >= 3:  # value
            descripS = vL[2].strip()
            unitL = vL[1].split(",")
            unit1S, unit2S = unitL[0].strip(), unitL[1].strip()
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            val1U = val2U = array(eval(valS))
            if unit1S != "-":
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS + "*" + unit1S
                    exec(cmdS, globals(), locals())
                    valU = eval(varS)
                    val1U = str(valU.number()) + " " + str(valU.unit())  # case=1
                    val2U = valU.cast_unit(eval(unit2S))
            self.valL.append([varS, val1U, val2U, descripS])
            if self.setcmdD["saveB"] == True:
                pyS = vL[0] + vL[1] + vL[2] + "\n"
                # print(pyS)
                self.exportS += pyS
        self.rivtD.update(locals())

    def _vtable(self, tbl, hdrL, tblfmt, alignL):
        """write value table"""

        locals().update(self.rivtD)
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate(
                tbl, tablefmt=tblfmt, headers=hdrL, showindex=False, colalign=alignL
            )
        )
        valS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()
        rstS = output.getvalue()
        sys.stdout = old_stdout
        self.restS += rstS + "\n"
        self.rivtD.update(locals())

    def _vvalue(self, vL: list):
        """import values from files

        Args:
            vL (list): value command arguments
        """

        locals().update(self.rivtD)
        valL = []
        if len(vL) < 5:
            vL += [""] * (5 - len(vL))  # pad command
        calpS = self.setsectD["fnumS"]
        vfileS = Path(self.folderD["cpath"] / calpS / vL[1].strip())
        with open(vfileS, "r") as csvfile:
            readL = list(csv.reader(csvfile))
        for vaL in readL[1:]:
            if len(vaL) < 5:
                vaL += [""] * (5 - len(vL))  # pad values
            varS = vaL[0].strip()
            valS = vaL[1].strip()
            unit1S, unit2S = vaL[2].strip(), vaL[3].strip()
            descripS = vaL[4].strip()
            if not len(varS):
                valL.append(["---------", " ", " ", " "])  # totals
                continue
            val1U = val2U = array(eval(valS))
            if unit1S != "-":
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS + "*" + unit1S
                    exec(cmdS, globals(), locals())
                    valU = eval(varS)
                    val1U = str(valU.number()) + " " + str(valU.unit())
                    val2U = valU.cast_unit(eval(unit2S))
            valL.append([varS, val1U, val2U, descripS])
        hdrL = ["variable", "value", "[value]", "description"]
        alignL = ["left", "right", "right", "left"]
        self._vtable(valL, hdrL, "rst", alignL)
        self.rivtD.update(locals())

    def _vdata(self, vL: list):
        """import data from files

        Args:
            vL (list): data command arguments
        """

        locals().update(self.rivtD)
        valL = []
        if len(vL) < 5:
            vL += [""] * (5 - len(vL))  # pad command
        valL.append(["variable", "values"])
        vfileS = Path(self.folderD["apath"] / vL[2].strip())
        vecL = eval(vL[3].strip())
        with open(vfileS, "r") as csvF:
            reader = csv.reader(csvF)
        vL = list(reader)
        for i in vL:
            varS = i[0]
            varL = array(i[1:])
            cmdS = varS + "=" + str(varL)
            exec(cmdS, globals(), locals())
            if len(varL) > 4:
                varL = str((varL[:2]).append(["..."]))
            valL.append([varS, varL])
        hdrL = ["variable", "values"]
        alignL = ["left", "right"]
        self._vtable(valL, hdrL, "rst", alignL)
        self.rivtD.update(locals())

    def _vsub(self, eqL: list, eqS: str):
        """substitute numbers for variables in printed output

        Args:
            epL (list): equation and units
            epS (str): [description]
        """

        locals().update(self.rivtd)

        eformat = ""
        utfS = eqL[0].strip()
        descripS = eqL[3]
        parD = dict(eqL[1])
        varS = utfS.split("=")
        resultS = vars[0].strip() + " = " + str(eval(vars[1]))
        try:
            eqS = "Eq(" + eqL[0] + ",(" + eqL[1] + "))"
            # sps = sps.encode('unicode-escape').decode()
            utfs = sp.pretty(sp.sympify(eqS, _clash2, evaluate=False))
            self.calcl.append(utfs)
        except:
            self.calcl.append(utfs)
        try:
            symeq = sp.sympify(eqS.strip())  # substitute
            symat = symeq.atoms(sp.Symbol)
            for _n2 in symat:
                evlen = len((eval(_n2.__str__())).__str__())  # get var length
                new_var = str(_n2).rjust(evlen, "~")
                new_var = new_var.replace("_", "|")
                symeq1 = symeq.subs(_n2, sp.Symbols(new_var))
            out2 = sp.pretty(symeq1, wrap_line=False)
            # print('out2a\n', out2)
            symat1 = symeq1.atoms(sp.Symbol)  # adjust character length
            for _n1 in symat1:
                orig_var = str(_n1).replace("~", "")
                orig_var = orig_var.replace("|", "_")
                try:
                    expr = eval((self.odict[orig_var][1]).split("=")[1])
                    if type(expr) == float:
                        form = "{:." + eformat + "f}"
                        symeval1 = form.format(eval(str(expr)))
                    else:
                        symeval1 = eval(orig_var.__str__()).__str__()
                except:
                    symeval1 = eval(orig_var.__str__()).__str__()
                out2 = out2.replace(_n1.__str__(), symeval1)
            # print('out2b\n', out2)
            out3 = out2  # clean up unicode
            out3.replace("*", "\\u22C5")
            # print('out3a\n', out3)
            _cnt = 0
            for _m in out3:
                if _m == "-":
                    _cnt += 1
                    continue
                else:
                    if _cnt > 1:
                        out3 = out3.replace("-" * _cnt, "\u2014" * _cnt)
                    _cnt = 0
            # print('out3b \n', out3)
            self._write_text(out3, 1, 0)  # print substituted form
            self._write_text(" ", 0, 0)
        except:
            pass

    def _vfunc(self, vL: list):
        pass

    def t_rst(self) -> tuple:
        """parse table-strings

        Return:
            calcS (list): utf formatted calc-string (appended)
            setsectD (dict): section settings
            setcmdD (dict): command settings
            rivtD (list): calculation values
        """

        tcmdL = ["text", "table", "image"]
        tmethL = [self._itext, self._itable, self._iimage]
        ttagL = [
            "[page]_",
            "[line]_",
            "[link]_",
            "[literal]_",
            "[foot]_",
            "[s]",
            "[x]",
            "[r]_",
            "[c]_",
            "[e]_",
            "[t]_",
            "[f]_",
            "[#]_",
        ]

        self._parseUTF("table", tcmdL, tmethL, ttagL)

        return self.calcS, self.setsectD, self.setcmdD, self.rivtD