# command line help

"""rivet

The *rivet* package implements the **r-i-v-e-t** calculation language as a
component of **on-c-e** (**O**\ pe\ **N** **C**\ alculation **E**\ nvironment),
which produces formatted engineering calculation documents. It is written in
Python and designed to improve document reuse and review.  The program and
documentation are here: https://github.com/r-i-v-e-t .  For an overview of
**on-c-e** see https://github.com/on-c-e .

A **r-i-v-e-t** design is a collection of ASCII text files containing
engineering calculations in the **r-i-v-e-t** and Python language format.
Design files have names of the form *rddcc_design_filename.py* where dd and cc
are two digit numbers identifying the division and calculation number
respectively. Division numbers organize **r-i-v-e-t** reports. 

The designs and their required supporting files must be stored in their respective
*designs* subfolder. Output calc files are written to the *calcs* directory in
html and text (utf) format. PDF calcs, if specified, are written to the report
folder and may be assembled into collated reports. The user must initially set
up a project by creating the project folder structure using the following
naming conventions::

  Project_Name (chosen by user)
      |- designs
          |- scripts
          |- tables
      |- reports
          |- attachments
          |- figures
          |- HTML          
          |- temp

The program will display an error and stop if the design file is not located
within the correct folder structure.  

In the common case where designs are developed and edited in interactive mode,
calculations are produced by importing the *rivet.rivet_lib* library into the
design file. Calculations can also be produced by processing the design file (or
file set) from the command line by invoking the rivet package as follows:

.. code:: python

    python rivet rddcc_ design_filename.py  (list_of_files.txt)

"""

import sys

if __name__ == "__main__":
    sysargv = sys.argv[1]


def cmdlinehelp():
    """[summary]

    Returns:
        [type] -- [description]
    """
    print()
    print("Run rivet at the command line in the design folder with:")
    print("     python  ddcc_ userdescrip.py")
    print("where ddcc_ userdescrip.py is a design file in the folder")
    print("and **ddcc** is the model number")
    print()
    print("Specified output is written to the respective calc folder:")
    print("     ddcc_userdescrip.txt")
    print("     ddcc_userdescrip.html")
    print("     ddcc_userdescrip.pdf")
    print("Logs and other intermediate files are written to the temp subfolder.")
    print()
    print("Program and documentation are here: http://r-i-v-e-t.github.io.")
    sys.exit()


def _paramlines(dline1):
    """ set calc level parameter flags

        #| width:nn | pdf | noclean | margins:T:B:L:R | verbose |
    """
    cfg.pdfflag = 0
    cfg.cleanflag = 1
    cfg.projectflag = 0
    cfg.echoflag = 0
    cfg.calcwidth = 80
    cfg.pdfmargins = "1.0in,0.75in,0.9in,1.0in"
    if mline1[0:2] == "#|":
        mline2 = mline1[2:].strip("\n").split(",")
        mline2 = [x.strip(" ") for x in mline2]
        # print('mline2', mline2)
        if "pdf" in mline2:
            cfg.pdfflag = 1
        if "noclean" in mline2:
            cfg.cleanflag = 0
        if "verbose" in mline2:
            cfg.verboseflag = 1
        if "stoc" in mline2:
            cfg.stocflag = 1
        if "width" in mline2:
            pass
        for param in mline2:
            if param.strip()[0:5] == "title":
                cfg.calctitle = param.strip()[6:]
        for param in mline2:
            if param.strip()[0:7] == "margins":
                cfg.pdfmargins = param.strip()[6:]
    else:
        pass


vbos = cfg.verboseflag  # set verbose echo flag
_dt = datetime.datetime
with open(os.path.join(cfg.cpath, cfg.cfileutf), "w") as f2:
    f2.write(str(_dt.now()) + "      once version: " + __version__)
_mdict = ModDict()  # 1 read model
_mdict._build_mdict()  # 2 build dictionary
mdict = {}
mdict = _mdict.get_mdict()
newmod = CalcUTF(mdict)  # 4 generate UTF calc
newmod._gen_utf()
newmod._write_py()  # 4 write Python script
_el.logwrite("< python script written >", vbos)
_el.logwrite("< pdfflag setting = " + str(cfg.pdfflag) + " >", vbos)
if int(
    cfg.pdfflag
):  # 5 check for PDF parameter                                       # generate reST file
    rstout1 = CalcRST(mdict)
    rstout1.gen_rst()
    pdfout1 = CalcPDF()  # 5 generate TeX file
    pdfout1.gen_tex()
    pdfout1.reprt_list()  # 5 update reportmerge file
    _el.logwrite("< reportmerge.txt file updated >", 1)
    os.chdir(once.__path__[0])  # 5 check LaTeX install
    f4 = open("once.sty")
    f4.close()
    os.chdir(cfg.ppath)
    _el.logwrite("< style file found >", vbos)
    os.system("latex --version")
    _el.logwrite("< Tex Live installation found>", vbos)
    pdfout1.gen_pdf()  # 5 generate PDF calc
os.chdir(cfg.ppath)
return mdict  # 6 ret

# on return clean up and echo result summaries
vbos = cfg.verboseflag
if cfg.cleanflag:  # check noclean flag
    _el.logwrite("<cleanflag setting = " + str(cfg.cleanflag) + ">", vbos)
    os.chdir(_tpath)
    for _i4 in _cleanlist:
        try:
            os.remove(_i4)
        except OSError:
            pass
    os.chdir(_ppath)
if cfg.echoflag:  # check echo calc flag
    _el.logwrite("<echoflag setting = " + str(cfg.echoflag) + ">", vbos)
    try:
        with open(_cfile, "r") as file2:
            for il2 in file2.readlines():
                print(il2.strip("\n"))
    except:
        _el.logwrite("< utf calc file could not be opened >", vbos)
if cfg.openflagpdf:  # check open PDF flag
    try:
        pdffilex = os.path.join(_ppath, _cpath, _cfilepdf)
        os.system(pdffilex)
    except:
        _el.logwrite("< pdf calc file could not be opened >", vbos)

if cfg.openflagutf:  # check open UTF flag
    try:
        utffilex = os.path.join(_ppath, _cpath, _cfileutf)
        os.system(utffilex)
    except:
        _el.logwrite("< txt calc file could not be opened >", vbos)

calstart._variablesummary()  # echo calc results
_el.logwrite("< end of once program >", 1)
_el.logclose()  # close log
# end of program
