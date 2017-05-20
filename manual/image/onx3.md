![](onx2_files/image001.jpg)

** **

** **

** **

**ON-C-E**

![](onx2_files/image002.png)**O**pe**N** **C**alculation **E**nvironment
for\
 Structural Calculations and Documents

 

 

 

 

 

+--------------------+--------------------+--------------------+--------------------+
| **USER MANUAL and  |
| SPECIFICATION**    |
|                    |
| ** **              |
|                    |
| ** **              |
|                    |
| ** **              |
+--------------------+--------------------+--------------------+--------------------+

 

 

 

 

![Structural Model](onx2_files/image003.png)

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

\

[![on-c-e is an open source project started by StructureLabs. The
project was initiated to stimulate design variety and creativity in
research and practice by simplifying the composition, modification,
review and sharing of structural engineering calculations.  Features -
implements a simple, readable, natural markup language - produces
clear, explicit, organized calculation documents - facilitates sharing
and reuse through web databases - runs on workstations, web platforms
and mobile devices - uses Python engineering and scientific libraries 
- integrates with other structural engineering programs 
](onx2_files/image004.png)](http://www.structurelabs.com/)

 

 

 

 

 

 

![“Simplicity is the ultimate sophistication.” Leonardo da Vinci
](onx2_files/image005.png)

 

 

 

 

 

+--------------------------------------------------------------------------+
|                                                                          |
+--------------------------------------------------------------------------+

 

**CONTENTS**

 

[1..... Introduction   5](#_Toc395008070)

[2..... Add a simple template to once-db   6](#_Toc395008071)

[3..... Generate a calc from a template   7](#_Toc395008072)

[4..... on-c-e Overview    8](#_Toc395008073)

[5..... Files and Paths  9](#_Toc395008074)

[6..... Model Operations  11](#_Toc395008075)

[7..... Project Operations  11](#_Toc395008076)

[8. ... Web Resources  13](#_Toc395008077)

[9. ... Interactive Analysis  15](#_Toc395008078)

[Appendix A – Example Model and Calc   17](#_Toc395008079)

[Appendix B – Operations  23](#_Toc395008080)

[Appendix C – Komodo Edit   30](#_Toc395008081)

[Appendix D – Linux, Windows, Mac, iOS, Android   32](#_Toc395008082)

[Appendix E – Wakari, PythonAnywhere   36](#_Toc395008083)

[Appendix F – Minimum Programs and Libraries  38](#_Toc395008084)

[Appendix G – Licenses  39](#_Toc395008085)

[Appendix H – Security and Namespaces  41](#_Toc395008086)

[Appendix I – Examples  42](#_Toc395008087)

[Index   43](#_Toc395008088)

 

 

 

 

                               

 

 

 

 

 

 

**Figures**

** **

** **

[**Figure 1. Program and interface structure**. 5](#_Toc395008056)

[**Figure 2. Basic environment components**. 9](#_Toc395008057)

[**Figure 3. Model, calc and project content**
13](once-manual-spec-041_x.docx#_Toc395008058)

[**Figure 4.  Screenshots of equation history in IPython terminal and QT
shells**. 16](#_Toc395008059)

[**Figure 5. Example PDF calc**.
20](once-manual-spec-041_x.docx#_Toc395008060)

[**Figure 6. Example PDF calc (continued)**.
21](once-manual-spec-041_x.docx#_Toc395008061)

[**Figure 7. Example PDF calc (continued)**.
22](once-manual-spec-041_x.docx#_Toc395008062)

[**Figure 8. Komodo interface**. 30](#_Toc395008063)

[**Figure 9.  Notesy screenshot of onceutf calc running on iPhone**.
33](#_Toc395008064)

[**Figure 10. DroidEdit screenshot of onceutf calc running on Android
tablet** 35](#_Toc395008065)

[**Figure 11. Wakari – terminal and editor in split windows**.
36](#_Toc395008066)

[**Figure 12.** **PythonAnywhere – side by side browser windows**.
37](#_Toc395008067)

[**Figure 13. http://opensource.org/licenses/MIT**.. 39](#_Toc395008068)

[**Figure 14. http://creativecommons.org/publicdomain/zero/1.0/**.
40](#_Toc395008069)

 

 

 

 

 

 

**Tables**

 

 

[**Table 1. Open source components (See Appendices D, E for details)**.
8](#_Toc395008089)

[**Table 2. File and folder structure**. 10](#_Toc395008090)

[**Table 3. Operations summary**. 12](#_Toc395008091)

[**Table 4. Minimum required versions of programs and libraries**.
38](#_Toc395008092)

* *

 

\

\

 

1.   Introduction {style="margin-left:.25in;text-indent:-.25in"}
=================

**on-c-e (**pronounced once) implements a readable, sequentially
organized markup language for writing and publishing structural
engineering calculations.  Calculations are stored in text files called
**models** or **templates** that describe structural behavior using
equations, text, tables and figures.  Relative to Mathematica ™, Mathcad
™ or MATLAB ™ it has several advantages:  it is much easier to use,
files will never be incompatible, and the program can be freely shared. 

Models generate design or analysis calculations. Templates are similar
but they do not represent specific designs.  The same model generates
calculations in two types of formatted documents referred to as
**calcs** (see Appendices A and H for examples).  A UTF calc is used for
iterative design and study and is formatted with UTF-8 characters.  It
is generated instantly and can be easily edited.  A PDF calc includes
graphics and **LaTeX** math and is used for reports or construction
documents. It takes a few seconds to generate. Models can interact with
other models, files and external structural engineering programs to
produce calcs or input to **IPython notebooks** for interactive
analysis. Typical models are less than a few hundred lines. Because they
are text they can be searched and stored in many types of databases. 
From a software point of view, models are instructions given in a
structural calculation markup language to **Python scientific and
engineering libraries** and external programs.

Calcs may be standalone PDF or UTF-8 files, or combined into a single
PDF **project calc** file.  Typical calcs are less than one or two dozen
pages but project calcs can be as large as needed. A project calc is
defined in a project file that specifies organization, numbering, title
blocks and table of contents.  From a software point of view, calcs are
produced by wrapping the **numpy** and **sympy** libraries in a
structural document formatting language. **PDF** and **project calcs**
are produced by processing the calc through **reStructuredText**,
**docutils**, **LaTeX** and **PyPDF2** libraries.

![](onx2_files/image006.png)**on-c-e **runs on workstations, web and
mobile platforms on top of **Python. ** The interface is an
**Interactive Development Environment** on workstations (Section 4),
**** a **browser** on web platforms, **** and **Apps** on mobile
platforms **** (Appendix D).

**Figure** **1. Program and interface structure**

2.    Add a simple template to once-db

This page describes the simplest approach to adding a template to the
once-db database. The purpose of the exercise is to gain an initial
familiarity with the process. 

We will use the template **0001.simple.txt** **** and modify it to make
a new template. Everything will be done in a browser – no installation
is needed.

Step 1.  Go to <http://on-c-e.org>.  Click on **** [**  [Download Model
Templates] **](http://structurelabs.knackhq.com/oncedb#home/)** ** at
the top of the page.

Step 2.  Scroll down to **search once-db**, click on the **description**
dropdown box and select **contains**.  Enter the search term ‘**simple
example’**.  Click on the **Search** button.  One or more results should
appear at the bottom of the page.

Step 3.  Look for the template name **0001.simple.txt** and the
associated calc names **cal0001.simple.txt** and **cal0001.simple.pdf.**
Click on the links that begin with **cal** to view the two different
calc formats in a browser window. 

Step 4.  Select the window for **cal0001.simple.txt.** Press the keys
CTRL-A or select all of the template text by dragging the mouse.  Press
CTRL-C or right click in the browser window and select copy to copy the
text to the clipboard.

Step 5.  Click on [**  [Upload Model
Templates] **](http://structurelabs.knackhq.com/oncedb#upload-model/) at
the top of the page.  Scroll down to the box labeled **Template Text**
and enlarge it by left clicking on the handle in the lower right corner
and dragging it.  Click in the box and press CTRL-V or right click and
select paste.  You should now have a copy of the template in the box.

+--------------------------------------------------------------------------+
| :                                                                        |
+--------------------------------------------------------------------------+

+--------------------------------------------------------------------------+
| :                                                                        |
+--------------------------------------------------------------------------+

+--------------------------------------------------------------------------+
| ##### ***Upload Template*** {align="center" style="text-align:center"}   |
+--------------------------------------------------------------------------+

+--------------------------------------------------------------------------+
| ##### ***Edit Template*** {align="center" style="text-align:center"}     |
+--------------------------------------------------------------------------+

Step 5.  Read over the template and edit the text, terms, and equations
to represent your own idea. Maybe you want to change it to a calculation
of calories or driving time to work. The only rules you need to follow
are to leave the tags and vertical bars in place and just edit the text
between them or delete the whole line with the tag. Section 6 provides
an overview and Appendix B describes what each tag does in more detail. 

When you finish editing the template, type a brief template summary in
the **Template Summary Description** box above. Include the phrase
‘**learning template’** in the description. Delete all of the words
 ‘**example**’  from the template and description (so it doesn’t show up
in the search).  Don’t worry about the template contents; the learning
templates will be removed from the database every few days.

 

Step 6.  Click on the **** **  Submit **  button. You should receive a
confirmation message that the template was submitted.

 

That’s it!  Thanks for learning how to contribute.

(note: typically the template file will be prepared on your computer and
uploaded)

 

3.    Generate a calc from a template

This page describes the simplest approach to running an example
template. It uses a web platform that does not require program
installation. 

+--------------------+--------------------+--------------------+--------------------+
| icon key           |
|                    |
| 1 ** Web           |
| Document**         |
|                    |
| : **Exercise**     |
|                    |
| **\$**             |
| **Summary**        |
+--------------------+--------------------+--------------------+--------------------+

**on-c-e** is designed to run on workstations with Python installed, but
it can also run in the cloud on Python web platforms like **Wakari **and
**PythonAnywhere. ** They provide an in-browser editor and shell
terminal interface.  **Wakari** and **PythonAnywhere** are discussed in
the manual but other Python web platforms can be used.  Appendix E
provides additional details for web execution.  Appendix D discusses
installation of the program on a computer or mobile device.

For this exercise a simple example model is run on a Python web platform
using the program onceutfnnn.py.  You can preview and download other
models at <http://on-c-e.org>.  Printed example models and calc output
are provided in Appendix I. onceutf.py is a single file subset of
**on-c-e** that does not include project options, PDF calcs, or unit
overrides.  ** **It was written to simplify program testing and
implementation on web and mobile platforms.  

+--------------------------------------------------------------------------+
| :                                                                        |
+--------------------------------------------------------------------------+

+--------------------------------------------------------------------------+
| ##### ***Run\                                                            |
|  template**** *** {align="center" style="text-align:center"}             |
+--------------------------------------------------------------------------+

1.      Sign up for a Wakari account at <http://continuum.io/>\
       or at\
 PythonAnywhere at 
[https://www.pythonanywhere.com/‎](https://www.pythonanywhere.com/‎)

2.      Download onceutfnnn.py and **0101.simple.txt** **** or
**0101.template.txt** from  <http://on-c-e.us>

3.      Upload the program and template files to a folder on your
Wakari or PythonAnywhere account.  Choose a bash shell terminal from the
drop-down list and open it (Appendix E).  At the shell command line
check that both files are in the folder you selected (type ***ls*** or
***dir***).  Enter the command

python  onceutfnnn.py  **0001.simple.txt**  -e

 

where *nnn*  is the program version number (i.e. 040).

 

The model will write several files to the directory (Table 2) and echo
the log file and calc, **cal0101.simple.txt**, to the screen.  You can
open the calc using the browser editor provided by the web platform. 
The switches following the model name echo the calc to the console
(–**e)** or browser\
 (**–b)**.  The browser option works when run on local computer.

 

Congratulation on running your first model!

(note: refer to Appendix D for **on-c-e** installation instructions)

 

4.    on-c-e Overview {style="margin-left:.25in;text-indent:-.25in"}
=====================

The **** **OpeN Calculation Environment** is defined by:

-    **oncepy** - Python package

-    **onceutf.py –** single file program and subset of **oncepy**

-    **onceipy.py** – updates the IPython database with
**on-c-e** equations for interactive analysis

-    **once-db **- online browser accessible database for sharing
template files.

-    **Komodo Edit** - a multilanguage IDE for Windows, Linux,
OSX (others may be used)

-    **Anaconda 1.9.2  **- scientific Python distribution for Windows,
Linux, OSX (others may be used)

-    **Wakari –** web based scientific Python distribution with browser
interface (others may be used)

-    **Pythonista **- Python platform for iOS

-    **QPython **- Python platform for Android 

+--------------------------------------------------------------------------+
| 1                                                                        |
+--------------------------------------------------------------------------+

**oncepy** is written **** for **Python 2 or 3** and **IPython. **
Python is a dynamic, high-level, general-purpose language widely used
for engineering and scientific scripting and programs.  For comparisons
with other numerical computing environments, such as **MATLAB,** see for
example:

+--------------------------------------------------------------------------+
| ##### ***MATLAB\                                                         |
|  vs****\                                                                 |
|  Python*** {align="center" style="margin-right:-2.25pt;text-align:center |
| "}                                                                       |
+--------------------------------------------------------------------------+

 

<http://www.stat.washington.edu/~hoytak/blog/whypython.html>

           
  <https://sites.google.com/site/pythonforscientists/python-vs-matlab>

 

A single file program called **onceutf.py,** was written to simplify
testing and implementation in web and mobile environments. It produces
UTF calcs and does not require any installation other than copying the
file to a folder.

 

![](onx2_files/image007.jpg)**Komodo Edit\
 IDE**

![](onx2_files/image008.jpg)**Anaconda\
 Python\
 Platform** ****

**\
   Wakari\
   Web\
   Platform**

![](onx2_files/image009.jpg)**oncepy                           
      once-db                                                  onceutf.py                                            \
                  **

**Links**

[**activestate.com**](http://www.activestate.com/komodo-edit/downloads)

[**anaconda**](https://store.continuum.io/cshop/anaconda)

[**wakari.io**](https://wakari.io/)

[**on-c-e.org**](http://on-c-e.org/)[](http://structurelabs.knackhq.com/oncedb#programs/)

[**oncedb**](http://structurelabs.knackhq.com/oncedb#home/)

**OS**

Windows, Linux and OSX

**Details**

Full featured open source IDE for multiple languages

Enterprise-ready distribution for scientific computing

Python package and single file subset for structural calculations  

Online template database with web interface

**Sponsor**

Active State\
 Canada

Continuum\
 USA

StructureLabs\
 USA

**License**

Mozilla Public License

Various Open Source Licenses

Program: MIT License\
 Models:  CCO1.0 Public Domain

**\
                          Table** **1. Open source components (See
Appendices D, E for details)**

5.    Files and Paths {style="margin-left:.25in;text-indent:-.25in"}
=====================

The fundamental program component is a model file xxyy.model.txt, where
**model** is a user-created file name and **xxyy** is a four digit model
designation.  The first two digits refer to the model division number
and the last two to the model number. The designation is used for calc
and project organization and must be unique. Models are stored in
division folders and division folders are stored in a project folder
(one level deep).  When a model is run it produces the following output
files (Figure 2, Table 2):

-          ­­UTF-8 calc **calxxyy.model.txt**.

-          calc description file sumxxyy.model.txt that can be pasted in
the once-db form.

-          IPython input file \_onceeq.py for interactive analysis.

-          execution log file \_modelog.txt, also (partially) echoed to
screen.

-          optional PDF calc **calxxyy.model.pdf** and supporting files\
 (.rst, .tex, .log, .out, fls, fdb\_latexmk – see Appendix D for file
handling).

-          optional project calc **project.pdf** assembled from a
specified set of division folders.   

Models are grouped in division folders and may include references to
other models, external functions, data, and batch or script control
files. External model files are generally located in the model
division folder and are identified by file name only.  The program
recreates the full path name internally, which allows division folders
to be moved without changing the models.  The exceptions include files
manipulated by the disk operation parameters r (read) and e (edit) which
require a full path name, and comodels imported with option i which
require the division folder name (see operation [d] with options i, r, e
in Appendix B).

 

A division folder has the name xx\_division\_name where xx is the unique
division number.  Each division or project folder may contain up to 100
models or divisions respectively.  The project folder contains the
project definition file if needed, and it may contain unit and PDF style
definition files (**unitc.py**, **once.sty**) that override the program
defaults for the entire project.  Definition files in a division file
override all other definition files. 

 

![](onx2_files/image010.jpg)

 

**Figure** **2.** **Basic environment components**

 

**Project Files**

**Project / Division Folder Structure**

 

 

![](onx2_files/image011.jpg)

**Division Files**

**xxyy.model.txt\
** Model

 

** (project.txt)\
**  Project file

**(unitc.py)\
** Custom units

**(background.pdf)**\
 Calc background

**(unitc.py)\
** Custom units

**(once.sty)\
** Custom PDF style

 

**(once.sty)\
** Custom PDF style

**calxxyy.model.txt\
** UTF-8 calc

**sumxxyy.model.txt\
** Model description

**(project.pdf)\
** Project calc

**\_onceeq.py\
** IPython file

**(project.log.txt)\
** Project execution log

**\_log.txt\
** Model execution log

**(calxxyy.model.pdf)\
** PDF calc

** **

Notes:\
 1. Input files are in blue; output in green\
 2. Optional files are in parenthesis   \
 3. PDF calc auxillary files are erased by default (Appendix D)\
     To keep auxillary files use ‘–noclean’ command line option \
  \
\

** **

**Table** **2. File and folder structure**

**\
**

** **

 

6.    Model Operations {style="margin-left:.25in;text-indent:-.25in"}
======================

Models are composed of a dozen operations. The basic operations are
**sections**, **terms**, **equations checks**, **arrays**,
**functions,** and **format** (see Figure 3, Table 3, and Appendix B).
 When operations are processed the calc sections and equations are
sequentially numbered. Equations are first formatted symbolically and
then with numerical substitutions. The degree of printed detail is
controlled by formatting statements. Tables are created from arrays and
vectors.  Units and decimal places are reduced and formatted (see
**unitc.py** file).  PDF calcs start a new page at every section and
figures are inserted.

 

Operations are identified by bracketed **tags** and may occur in any
order or frequency as long as each term or variable is defined before
use. Operations are executed sequentially, in the order they are
entered.  Nesting is not permitted.  Parameters and options associated
with tags are provided on the same line, separated by vertical bars (|).
Parameters with defaults or empty parameters may be omitted but the bar
delimiters (with at least one space in between) must be provided. Arrays
do not include unit processing.   Operations may extend over single or
multiple lines.  Tags for single line operations include [d], **** [o],
**** [t]**.** Tags for multi-line operations include [c], **** [a], ****
[f], **** [e], **** [s].  Multi-line operations are terminated with a
blank line.  

 

The **disk operation** [d] performs several file functions depending on
the option selected. Options are designated by s, t, o, w, f, i, r, e. 
The option s reads external Python files that can define functions
available to the **function tag** [f].  The option i imports a comodel
into the main model. A comodel is a model that does not import other
models (only one level of model recursion is permitted).  Other options
import figures and text, and execute read, write, edit and run
operations on external files and programs. 

 

Tags may be indented to improve model readability (4 spaces is
standard).    Any text in the model not associated with an operation tag
is passed through to the output unchanged, including
**reStructuredText** markup. For example, surrounding text with
\*\*double asterisks\*\* will print **bold**, \*single asterisks\* will
print *italics* and a vertical bar in the first column will force a new
line in PDF calcs.  See the [reST quick
reference](http://docutils.sourceforge.net/docs/user/rst/quickref.html)
for further documentation.  

7.    Project Operations {style="margin-left:.25in;text-align:justify;text-indent:-.25in"}
========================

**Project** operations are identified with tags [p] **** and [\#]
pformat.  The operation writes a project calc with the name
**project.pdf** to the project folder, overwriting an existing file. The
project operation is divided into a project data definition section and
a division (folder) inclusion list (Table 3 and Appendix B).  Each
division designation includes the option to override the project
defaults on a calc by calc basis.  Project data is defined by a
dictionary of keyword-data pairs that can easily be incorporated into
databases.  The project format operation defines the page print
location, if any, for a specific piece of project data.

 

Project calcs produced from the project operation are simply ordered
assemblies of calcs that include a title page, table of contents, title
blocks and navigational links. 

 

**Tags**

**Operations (optional parameters)**

**Notes**

[**[d]**](#d_op)

Disk file\
 [d] folder/file | option | (var1) | (var2) | (var3)

option is one of\
 s,t,o,w,f,i,r,e

[**[o]**](#disk)

Symbolic representation\
 [o] sympy symbolic expression

Expression is printed but not evaluated.

[**[t]**](#term)**\
\
**

Term\
 [t] description | var = value

 

[**[c]**](#disk)

Check expression against limit\
 [c] decimal | description | ok\
      expression | op | limit

 

[**[a]**](#array)

Array table\
 [a] format\_number | table description\
     range variables\
     var = expression

For format reference numbers see format operation.

** **

[**[f]**](#equation)

Function\
 [f] var | function description\
      function\_name()

Functions are defined in external files and imported with [d] | s |

[**[e]**](#equation)**\
\
**

Equation\
 [e] format\_number | equation description\
      var = expression

 

[**[s]**](#section)

Section\
 [s] section heading\
     section description

 

[**[\#]**](#format)

[**format**](#format)

**stop**

Comment or equation and array formats

[\#] format | (deci, deci) | (out type)\
     format\_number | (deci, deci) | (units) | (label/prnt code)

[\#] stop

[\#] comment line

[\#] followed by format or stop are special cases. stop terminates model
processing. 

[**[p]**](#project)

Project data (requires oncepy)\
 [p] (pdf size) | (background.pdf)\
 keyword = data | (format\_number)\
 keyword = data |\
 01\_divisionfolder | (division title)\
   model\_name1 | (pdf size) | (background1.pdf)\
     keyword = format\_number  | keyword = format\_number | | |\
   model\_name2 |            |\
     keyword = format\_number  | | | |\
 02\_divisionfolder \
 03\_divisionfolder

Model files (.txt suffix) are first processed to PDF.

[**[\#]**](#pformat)

[**pformat**](#pformat)

 

Project formats (requires oncepy)

[\#] pformat  | format\_number\
     keyword | x location | y location\
     keyword | x location | y location

[\#] followed by format is a special cases. Terminate with blank line

 

**Table** **3. Operations summary**

** **

![](onx2_files/image012.png)\
 {style="margin-left:0in"}
=============================

![Figure 3. Model, calc and project content](onx2_files/image013.png)

\
 8.     Web Resources

 

+--------------------------------------+--------------------------------------+
| \                                    |
| :                                    |
+--------------------------------------+--------------------------------------+

+--------------------------------------------------------------------------+
| ##### * Share models*                                                    |
+--------------------------------------------------------------------------+

**Download  Models\
** <http://on-c-e.org>

**Upload Models\
** <http://on-c-e.org/upload-model>

** **

+--------------------------------------------------------------------------+
| :                                                                        |
+--------------------------------------------------------------------------+

+--------------------------------------------------------------------------+
| ##### *Run locally* {align="center" style="margin-left:9.0pt;text-align: |
| center"}                                                                 |
+--------------------------------------------------------------------------+

**Download and install Anaconda 1.9.2. ** Using ***pip***, install
**Unum**, **tabulate** and **PyPDF2**.  Install **Tex Live** 2014.
Download and install Komodo Edit (see Appendices D and F). 

 

 

Although any text editor is adequate for composing and running models,
the most effective tool is an interactive development environment
(IDE).  It provides project and file management, font management, code
navigation, templates, custom toolbars and macros, syntax coloring,
window layout controls and remote file access. Komodo Edit is an open
source workstation IDE which can manage **Python, TCL, Ruby** and other
programing languages applicable to structural engineering work. Several
Komodo specific tools are provided for **on-c-e** and described in
Appendix C.  Although Komodo is discussed in this manual other IDEs may
be used.** **

+--------------------------------------------------------------------------+
| \$                                                                       |
+--------------------------------------------------------------------------+

 

+--------------------------------------------------------------------------+
| ##### *Find\                                                             |
| \                                                                        |
| * {style="margin-left:4.5pt"}                                            |
+--------------------------------------------------------------------------+

About                                                
[on-c-e.org](http://on-c-e.org)\
 User manual                                     <http://on-c-e.us/>\
 Komodo Edit                                    
<http://activestate.com/komodo-edit>\
 DejaVu Fonts                                               
<http://dejavu-fonts.org/wiki/Main_Page>\
 Workstation (Anaconda 1.9.2)      
<http://repo.continuum.io/archive/index.html>\
 Web Platform (Wakari)                    <https://wakari.io/>\
 onceutf                                             
<http://on-c-e.us>\
 oncepy                                              
<http://on-c-e.org/programs/>\
 model database                              
[http://](http://structurelabs.knackhq.com/oncedb#home/)on-c-e.org/\
 TeX Live                                            
<https://www.tug.org/texlive/>\
 Code and docs                                
<http://on-c-e.github.io/>\
 Road map                                          <http://on-c-e.info/>

\

 

9.     Interactive Analysis {style="margin-left:0in"}
===========================

In some cases equation level interactive analysis and design is
preferred over complete model runs.  An import equation file,
\_**onceeq.py,** is written when **on-c-e** is run and may be used for
interactive analysis.  Three interactive interfaces are available:

 

+--------------------------------------------------------------------------+
| :                                                                        |
+--------------------------------------------------------------------------+

o   **Komodo IDE** (commercial version):  Cut and paste the entire
**onceeq.py** file into the interactive shell for access to equations
and terms.

 

o   ![](onx2_files/image014.jpg)**IPython Notebook**:
 <http://ipython.org/notebook.html>  Cut and paste the entire
**onceeq.py** file into a notebook cell for interactive access to
equations and terms.

 

o   **IPython Terminal** and **Qt shell**:  <http://ipython.org/>

 

Equations from **\_onceeq.py** are loaded into a shell in two steps:

 

1.      The script **onceipy.py** updates the
**history.sqlilte** database with the equations. Copy **onceipy.py** to
the Python /lib/site-packages directory.

 

2.      \_**onceeq.py** is loaded into Ipython using the ‘run’ command. 

 

Both steps are executed by the **IPy** macro button on the Komodo
**on-c-e** toolbar (see Appendix C).  Run this macro after running the
model and when the division file for the model has focus.  Prior to
using the button, modify the command "**run\_onceipy**" (at the end of
the tool list in the Komodo toolbox) by adding the location of the
history.sqlite directory to the command line entry (do not type
brackets), i.e.

 

    python -m onceipy.py  [C:\\Users\\rhh\\.ipython\\profile\_default]

 

When **onceipy** is run, the equations are read from the **onceeq.py**
file generated when **on-c-e** is run.  They are assigned the next
session number and added to the end of the **history.sqlite** file. A
backup copy of the file is made before the new equation records are
added.

 

If the history.sqlite file becomes too large or corrupted it may be
deleted and reinitialized simply by running IPython from the command
line.

 

Equations and terms are available in the shell through command history
scrolling or using the **%rep ref** command, where **ref** is the
equation history reference.

![](onx2_files/image015.png)![](onx2_files/image016.png)

 

**Figure** **4.  Screenshots of equation history in IPython terminal and
QT shells**

Appendix A – Example Model and Calc {style="margin-left:0in"}
===================================

 

**Example Template / Model**

 

[s] Example 0101 - basic model template

    This example template calculates the mid-span beam moment

    under uniformly distributed (UDL) floor loads.  It demonstrates

    \*\*section [s], term [t] equation [e] and [\#] format
operations\*\*.

    reStructuredText inline markup is also used.

 

 

[d] beam.png | f | Simply supported beam | 70 |

 

[s] Beam Loads and geometry

    Dead and live load contributions to beam UDL and beam layout

    configuration

 

    \*\*Dead loads\*\* from permanent weights

    [t] joists          | jst\_DL   =   3.8\*PSF

    [t] plywood         | ply\_DL   =   2.1\*PSF

    [t] partitions      | part\_DL  =  10.0\*PSF

    [t] fixed machinery | equip\_DL =   0.5\*KLF

 

    \*\*Live loads\*\* from people and moveable items

    [t] ASCE7-O5        | live\_LL = 40\*PSF

 

 

    \*\*Beam tributary width and span\*\*

    [t] distance between beams  | trib\_width = 2\*FT

    [t] beam span               | span = 14\*FT

 

 

[s] Maximum bending moment

    Calculate factored UDL loads and bending moment at mid-span of beam

 

    [e] 010122 |  Total UDL factored dead load

        DL\_D = 1.4 \* (trib\_width \*(jst\_DL + ply\_DL + part\_DL) +
equip\_DL)

 

    [e] 010122 |  Total UDL factored live load

        LL\_D = 1.7 \* trib\_width \* live\_LL

 

    [e] 010122 | factored UDL

        omega\_1 = DL\_D + LL\_D

 

    [e] 010123 | Bending moment at mid-span

        M\_0 = omega\_1 \* span\*\*2 / 8

 

 

[\#] format  | 3,3  | pdf

    010122  | 2,2  | KLF     | 2

    010123  | 2,1  | KIP\*FT  | 3

 

[\#] This file contains a generic on-c-e model template (the template).

[\#] It is distributed under the CCO 1.0 Public Domain Dedication at

[\#] http://creativecommons.org/publicdomain/zero/1.0/

[\#] The template is not a structural design calculation and

[\#] must be modified by the user prior to use.

[\#] The template user assumes sole and complete responsibility for

[\#] all existing or modified inputs and the computed model results.

\

 

 

**UTF calc**

 

![07/19/14 21:04:30
==========================================================================================
[1] Example 0101 - basic model template [0101]
==========================================================================================
This example model calculates the mid-span beam moment under uniformly
distributed (UDL) floor loads. It demonstrates \*\*section [s], term
[t] equation [e] and [\#] format operations\*\*. reStructuredText
inline markup is also used.    Figure 1. Simply supported beam
\<file: beam.png \> 
==========================================================================================
[2] Beam Loads and geometry [0101]
==========================================================================================
Dead and live load contributions to beam UDL and beam layout
configuration   \*\*Dead loads\*\* from permanent weights joists |
jst\_DL = 3.8 [psf] plywood | ply\_DL = 2.1 [psf] partitions |
part\_DL = 10.0 [psf] fixed machinery | equip\_DL = 0.5 [kips/ft] 
\*\*Live loads\*\* from people and moveable items ASCE7-O5 | live\_LL =
40 [psf]   \*\*Beam tributary width and span\*\* distance between
beams | trib\_width = 2 [ft] beam span | span = 14 [ft] 
](onx2_files/image017.png)

 

 

 

 

\

 

**UTF calc - continued**

 

![==========================================================================================
[3] Maximum bending moment [0101]
==========================================================================================
Calculate factored UDL loads and bending moment at mid-span of beam  
-----------------------------------------------------------------------------------------┐
DL\_D | Total UDL factored dead load [3.1]  1.4⋅equip\_DL +
1.4⋅trib\_width⋅(jst\_DL + part\_DL + ply\_DL)   DL\_D = 0.74
[kips/ft]
-----------------------------------------------------------------------------------------┘

-----------------------------------------------------------------------------------------┐
LL\_D | Total UDL factored live load [3.2]  1.7⋅live\_LL⋅trib\_width
  LL\_D = 0.14 [kips/ft]
-----------------------------------------------------------------------------------------┘

-----------------------------------------------------------------------------------------┐
omega\_1 | factored UDL [3.3]  DL\_D + LL\_D   omega\_1 = 0.88
[kips/ft]
-----------------------------------------------------------------------------------------┘

-----------------------------------------------------------------------------------------┐
M\_0 | Bending moment at mid-span [3.4]  2 ω₁⋅span  ──────── 8  
 2 0.88 [kips/ft]⋅14.00 [ft]  —————————————————————————— 8   M\_0
= 21.6 [ft.kip]
-----------------------------------------------------------------------------------------┘
 ](onx2_files/image018.png)

\

 

![](onx2_files/image019.png)![Figure 5. Example PDF
calc](onx2_files/image020.png)\

![Figure 6. Example PDF calc
(continued)](onx2_files/image021.png)![](onx2_files/image022.png)

![](onx2_files/image023.png)![Figure 7. Example PDF calc
(continued)](onx2_files/image024.png)

Appendix B – Operations {style="margin-left:0in"}
=======================

Calcs are composed of nine model operations: three operations are single
lines with the tags [d]**,** [o]**,** [t], and six operations are
multiline with tags [c]**,** [a]**,** [f]**,** [e]**,** [s], and [\#]
format.  Project calcs are built with a multiline operation using the
[p] **** and [\#] format tags.  All multiline operations are terminated
with a blank line. 

 

![](onx2_files/image025.png)** **

\

**[d]**   (path)/filename | s,t,o,w,f,i,r,e | (v1) | (v2) | (v3)

 

The disk operation processes external disk files according to single
letter options. Files for the first 5 options are located in the
model folder and are specified by file name only.  The model folder and
name are used for the i **** operation.  Full file paths are used for
the r **** and e **** options. This approach makes a model as portable
as possible across different folder organizations.

** **

filename: **** file name used in disk operation. See details for each
parameter type.\
 v1-v3: **** variables specific to the disk operation option. See
details.

s: **** execute Python file in model.  Typically used to process
external functions.

t: **** add text file boilerplate to output (no operations are
processed).

o: **** run an operating system batch or script file. Typically runs a
program.

w: **** write values of variable to CSV file. Overwrites existing
files.  w+ **** appends files.

f: **** insert image from file into calc (jpg, png etc.)

i: **** insert and process a comodel file.  Integrates sections and
equation numbering.

r: **** read CSV file data into array variable.

e: **** edit line of existing text file and save in copy of file.

 

s: **** execute an external Python script in model namespace.\
\

Executes an external Python script and includes the methods (functions)
and variables in the model namespace.

** **

t: **** inset text file contents into output (no operations are
processed).

 

Inserts the text file contents at the operation location. The var
parameter optionally specifies the line range to be inserted for lines
n1:n2 inclusive.

** **

o: **** run an operating system command or executable file

.

w: **** write array values to file.\
\

Write contents of array v1 to the file specified by filename. Each line
or row is written using the **numpy.tofile** method. To append data to
an existing file use the option w+.  v2 specifies the separation
character (comma is default, for a space character use \*). v3 is the
data type (default is character format %s).

 

f: **** insert figure from file into calc (**jpg, png etc.**).\
\

Insert figure from file with caption v1. Figure labels are automatically
added and incremented. v2 specifies the image width in percent of
document width.  The figure is centered and the aspect ratio is
maintained.   v3 specifies a side by side arrangement for a second
consecutive figure using the keyword adjacent. For UTF-8 output the
following text is inserted: \
 **Figure n:  caption - file: filename**

** **

i: **** insert and process a comodel file. \
 division\_folder/file: **** model folder and file name

 

Merge a comodel file into the main model file at the operation
location.  The comodel cannot include a comodel.  Sections and equation
numbers are integrated into the main model sequence.  Format numbers
must be unique in the two models (see format operation for suggested
format numbering schemes).

** **

r: **** read file data into variable

path/file: **** absolute path name

 

Read CSV contents of **path/filename** into variable v1 **** and store
as array using the **numpy.genfromtext** method.  v2 specifies the
separation character (comma is default, for space character use \*). v3
specifies the number of lines to skip before reading the data (default
is 0).

 

** **

e: **** edit text file

path/file: **** absolute path name

 

Edit an external file at run time. Lines immediately following the edit
operation have the form:

 

n | replacement text for line n

           

where n **** is the line number to be replaced with the specified
replacement text. The v1 parameter is appended to the file name before
it is saved with edits i.e. if v1 **** is **copy** and the filename is
**file.tcl** the edited file is saved as **filecopy.tcl.**

** **

Template variables may be used in the replacement line.  A
template variable is created by appending a **%** in front of the
variable name used in the model.  

 

\

 

 

**[o]** **** Python or sympy expression ** **

 

The symbolic operation formats a sympy symbolic expression without
evaluating the terms.

 

![](onx2_files/image025.png)** **

\

**[t]** **** var = value | (description) ****

 

The term operation is used to assign values to terms used in equations. 
It evaluates expressions that multiply by constants or units.

 

var = value: **** define term

description: **** term description

** **

![](onx2_files/image025.png)*** ***

\

**[\#]**  The hash tag is used for non-printing comments. If the comment
is format** **the format operation is subsequently processed.  If the
comment is stop the program processes the model to that point along with
any formats in the model. This can be useful for developing and
debugging a model. 

*** ***

**[\#] format**   |(default deci, deci) | (output type)

format number |(deci, deci)     | (units/label)\`     | (prt
code/label)          format number |(deci, deci)     | (units/label)
     | (prt code/label)

 

The format operation describes decimals, units and labels for
equations and arrays. \
 Use print code 0, 1 or 2 for equations that return arrays.

** **

default deci: number of printed decimal places in equation and result
(default 3, 3)

output type: **** output type is ***txt*, *rst*** or ***pdf* (**default
is txt). Not read when running **onceutf.**  Set command line option to
**–noclean** to retain **rst** file.  See Appendix D.

ref: Unique six digit equation or array format number between 1 and
99999.  Typically the first four digits are the model number and the
fifth digit is the section number.  This pattern facilities organization
and unique formats when comodels are used.

deci, deci: **** number of printed decimal places in equation and result

units/label: **** unum unit for dependent variable or label for first
range variable

print code/label: **** For equations provide print code 0, 1, 2, 3
(default is 3) where:

0 - evaluate but do not print result

1 - print result

2 - print symbolic expansion and result

3 - print full results - symbolic expansion, substitution and result

 

For 2D arrays provide a label for the second range variable.   

\

 

 

**[c]** decimal, decimal | description | ok

expression | operation | limit

 

The check operation checks an expression value (no variable assignment)
against a limit for a given operation.

** **

decimal: **** number of printed decimal places in equation, result
(default 3, 3)

description: **** description of comparison

expression: **** expression to evaluate – typically a ratio

operation: **** Python expression with comparison operator (\<, \>, \<=,
\>=, =)

limit: **** value or expression to evaluate that sets upper or lower
limit

ok: **** phrase that prints if compare evaluates to True. If expression
evaluates to False the word ‘not’ is prepended.  May be blank.

** **

![](onx2_files/image025.png)

** **

\

**[a]**  format ref | array description\
      vector variable1

(vector variable2 for 2D arrays)

var = expression

** **

The array operation input is similar to the equation operation but
outputs the results of vector equations in tables 1D or 2D table with
column and row labels.  Range variables and expressions must be
unitless.  If only one range variable is provided a single row table is
output.  The variable name may be a previously defined vector.  Note
that the number of printed decimals corresponds to the first entry in
the integer pair.

** **

variable1: **** a range statement or variable containing vector or array
values.\
 variable2: **** a range statement for 2D tables.\
 var = expression: **** unitless equation using Python syntax

 

![](onx2_files/image025.png)

** **

** **

\

**[f]** var | function description

     function\_name(args)

** **

The function operation executes a function and assigns the return value
to variable var. The function is defined in a Python file and imported
using the [d]operation with the s option.   Describe the function using
the function doc strings which are imported into the model.  Printed
decimals should be controlled by the function itself.

** **

var : **** one line description of function\
 function description : **** short description of function

function\_name(args): **** name of function and arguments to be executed

** **

** **

**[e]** **** format number | (description)\
      var = expression

 

The equation operation evaluates a Python math statement and optionally
prints the symbolic representation, equation with substituted values and
solution.  The format operation (**[\#] format**) controls the level of
printing detail, decimals and units.  Equation input may extend over a
maximum of three lines.   Terminate the operation with a blank line.
Indenting equations, terms, functions and arrays may help legibility.

** **

format ref: **** integer between 1 and 999999 that references a
formatting operation.

description: **** equation description and building code references

var = expression: ****  equation using Python syntax

** **

![](onx2_files/image025.png)**\
\
**

**[s]** section heading

(description)

**\
** The section operation provides organization to the calculation.
Sections are automatically numbered and labeled with the associated
model. The source model designation number is added to the section
heading and right justified.  Equation numbers are generated within
sections as **s . e** where **e** restarts at 1 in each section.

 

heading: **** left justified heading

description: **** up to 10 lines of text (no blank lines) describing the
section. Terminate with blank line.

** **

**\
**

** **

 

.

*** ***

**[p]** **** (project default size) | (default background.pdf)

(keyword = data) | (format\_number)

(keyword = data) |

(keyword = data) |

**.**

**.**

01(\_divisionfolder) | (division title)

01yy.model.txt| size| background2.pdf

keyword = data | keyword = data | | |

02 | (division title)

02yy.model.pdf| size| nobackground

03 | (division title)

03yy.model.txt| size| background2.pdf

keyword = -1| kewyword = -1|  | |

04 | (division title)

04yy.model.pdf| | omit

| | | |

04yy.model.pdf| size |

05 | (division title)

**.**

**.**

 

The project operation is specified in the project file and provides
project calc information. Project files are located in the project
folder which in turn contain division folders as subfolders. 

**\
** size: **** size and orientation settings of PDF pages. 

portrait\_letter (default)

landscape\_letter

landscape\_tableau (11x17)

portrait\_A4

landscape\_A4

** **

background.pdf: ****** user file name for the calc background (default:
none)

 

keyword = data: **** keyword-data pairs to be added to the
project dictionary.  Any key word may be defined except for key words
reserved for project calc printing.  They include:

ptitle, pname, padd1, padd2**,** pstate, pzip, powner, pnumber, eng**,**
date, rev, stamp1, stamp2

** **

\

 

xx(\_divisionfolder): **** by default include calcs from this folder in
the project calcs.  If \_divisionfolder is provided as part of the
folder name it is used for the division name in the project calcs (i.e.
table of contents).  If division title is provided it is used instead.

 

For each model in the folder, if a PDF calc is available, it is used. 
Otherwise the model is run to produce the PDF calc.

 

Project settings may be overridden for a specified calc or model.   If
default background.pdf is set, then set the value to nobackground ****
to suppress the default template and all keywords for a particular
calc.  To omit a calc from the project set use omit for the template
value. A keyword data may be redefined for a specific calc.  To suppress
writing the keyword value to a calc set its value to -1.  To write only
keyword data without a template specify the keyword data on the keyword
override line.

** **

The project or division folder may also include the file **once.sty**
which defines the LaTeX PDF style settings, and the **unitc.py** file
which defines calc units.  They will override the default settings in
the **oncepy** package directory – division folder files override
project folder files.

 

*** ***

**[\#] pformat**   | format\_number

 

The project format operation describes the print location on a
calc sheet of keyword data defined in the project operation.  Terminate
format number definitions with a blank line.

** **

keyword | x location | y location

keyword | x location | y location

keyword | x location | y location

.\
 .

 

keyword: project keyword

x location: **** x location of keyword value on page in points from
upper left corner.

y location: y location of keyword value on page in points from upper
left corner.

** **

 

 

 

 

 

 

 

** **

+--------------------------------------------------------------------------+
| :                                                                        |
+--------------------------------------------------------------------------+

![](onx2_files/image026.png)\
 Appendix C – Komodo Edit {style="margin-left:0in"}
=============================

![](onx2_files/image027.png)

\

**Figure** **8. Komodo interface** ****

** **

Template files can be prepared using any text editor however Komodo Edit
provides additional useful capabilities and tools.  **on-c-e** syntax
coloring and operation tools are provided to improve readability and
efficiency. A **on-c-e** toolbar is provided to simplify program
execution.

 

**Install on-c-e utilities and fonts in Komodo**

1.      Download and install DejaVu fonts from

<http://dejavu-fonts.org/wiki/Main_Page>

![](onx2_files/image028.png)A point size of 9 and line width of 90 is
suggest.

![run model in IPy](onx2_files/image029.png)

 

** **

** **

\

**            The toolbar operates on the model that has focus**

2.      Download and unzip **oncetoolsnnn.zip**

3.      **Install the on-c-e tools folder** by - right clicking in tool
box pane – import folder – select the **on-c-e\_tools** folder rom the
unzipped file. Tools include a **tool bar**, **documentation menu** and
**code snippets** that can be inserted into models by double clicking.

4.      Close and reopen Komodo to complete installation. Edit a tool by
right clicking on it in the tool pane and selecting Properties.  Pane
arrangement can be controlled by the user.

5.      **Install the syntax coloring plugin** **once-0.3.1-ko.xpi**
**** using the menu - Tools – Add On. Select the xpi file from the
unzipped **oncetoolsnnn** folder. To see **once** syntax coloring in
your file set the language for the **.txt** file type to type **once**
**** using the right click context Properties and Settings when the file
is open. 

6.      After running a model the UTF calc is automatically opened in
the input pane. The associated PDF calc can then be opened in the users
default PDF viewer with the tool bar when the UTF calc has focus.

 

7.      The suggested model line length is 90 characters using
mono-spaced 9pt font.  Indents should be spaces, not tab characters. 
UTF calcs are formatted to a 90 character width.

 

8.      **PDF calcs** require installation of **TexLive**. See Appendix
D and F.

\

 

 

+--------------------------------------------------------------------------+
| :                                                                        |
+--------------------------------------------------------------------------+

Appendix D – Linux, Windows, Mac, iOS, Android {style="margin-left:0in"}
==============================================

** **

**Install local copy of onceutf.py on Linux, Windows, Mac:**

Install a scientific Python distribution.  Copy **onceutfnnn.py** and
the model file into the same folder, open a console window in the folder
and type:

 

***python onceutfnnn.py modfile.m.txt  (-e or –b) (-noclean)***

 

where **nnn** is the program version number (i.e. 040),
 **nnnn.modfile.txt** is the file name of the input model, **-e** or
**–b**  are options to echo calculation results to the console or
terminal or browser and **–noclean** retains the auxiliary PDF files
(erased by default).

 

To open a terminal window in in Windows 7 or 8, navigate to the folder
with the model, hold the shift key, right click in the folder and click
on 'open command window here'. 

Change the browser encoding settings if needed:

·         Chrome – type **chrome:settings/fonts ** in url bar - scroll
to the bottom of the dialog box to make the change.

·         Firefox - options - content - advanced - UTF-8

·         Internet Explorer - right click in window - encoding - UTF-8

 

**For UTF font symbols install font package from\
**
[**http://dejavu-fonts.org/wiki/Main\_Page**](http://dejavu-fonts.org/wiki/Main_Page)

** **

** **

**Install local ‘site-packages’ copy of onceutf on Linux, Windows,
Mac:**

Install a scientific Python distribution.  Copy the **onceutfnnn.py**
file into the Python/Lib/site-packages/ folder and rename to
**onceutf.py.** Run from any directory with the command

*** ***

***python –m onceutf** nnnn.modfile.txt ***

 

**Install a complete oncepy environment on Linux, Windows, Mac:\
 See Section 8 for links**

1.      Install Anaconda 1.9.2

2.      Install unum and tabulate modules (using pip install)

3.      Install TexLive

4.      Install DejaVu Fonts (and set to Mono in IDE)

5.      Install Komodo Edit

6.      Install on-c-e tools for Komodo

7.      Unzip and copy the **oncepy** folder into the
Python/Lib/site-packages/

8.      Run from any folder containing the model file with the command:

***python –m oncepy nnnn.modfile.txt ***

\

**Install onceutf on iOS:**

 

**onceutf** runs in the iOS **Pythonista** **App** environment which
includes numpy, sympy and matplotlib libraries.  Copy the **onceutf.py**
file to the site-packages folder and a model file to a division folder.

 

Without Dropbox integration files will need to be moved by creating new
empty files in Pythonista and using copy and paste (script for
downloading  Dropbox files to Pythonista
<https://omz-forums.appspot.com/pythonista/post/4995757044137984>).   

 

Open the **onceutf.py** program in Pythonista and create an ‘action’
(wrench menu) for it, leaving the argument blank.  Open a model or
template.  Run it by invoking the action.  The calc will be echoed to
the screen. The following script makes it convenient to iterate a model
by editing in Pythonista and viewing with the **Notesy App** (UTF-8
fonts).

 

**notesy.py script (**<http://on-c-e.us>)

"""open Pythonista calc in Notesy

 

1\. Copy this script to Pythonista and set it as an action.

2\. Set the fixed width font in Notesy to DejaVu Sans Mono.

"""

import editor

import webbrowser

import clipboard

base = 'notesy://x-callback-url/append?name=calc\_tmp.txt'  

text = editor.get\_text()

url = clipboard.set(text)

webbrowser.open(base)

![](onx2_files/image030.png)

**Figure** **9.  Notesy screenshot of onceutf calc running on iPhone**

 

 

**Install onceutf on Android:**

 

**onceutf** runs in the **QPython** **App** (Python 2) environment on
Android.  Copy the compiled numpy and sympy libraries into the
site-packages folder at

 

/mnt/sdcard/com.hipipal.qpyplus/lib/python2.7/site-packages.

 

The compiled libraries are available through QPython sites and also at
<http://on-c-e.us>.  Matplotlib libraries are not yet available.

 

The following file arrangement and script makes it convenient to iterate
and review a model.  It uses the **DroidEdit App** to edit the model and
view the calc. The **Hackers Keyboard App** is efficient for writing
models.

 

**once.py script (**<http://on-c-e.us>)

 

\#qpy:console

"""

once.py script runs a onceutf model on Android using QPython

 

1\. Copy onceutf.py to the ‘scripts’ folder (see prog path below)

2\. Create a division folder for the models (see model path below)

3\. Copy the model and this script into the division folder

4\. Open this script in QEdit (which is part of QPython)

5\. Modify folder and model names below, as needed, and save.

6\. Edit models and review calcs in DroidEdit (or similar editor).

7\. Set the editor font to DejaVu Sans Mono for calc math symbols.

8\. Run this script in QEdit to execute program.

 

"""

 

import os, sys

 

prog ='/mnt/sdcard/com.hipipal.qpyplus/scripts/onceutf.py'

model ='/mnt/sdcard/com.hipipal.qpyplus/models/0301.deflection.txt'

os.system(sys.executable + “ “ + prog + “ “ + model) 

 

 

 

![](onx2_files/image031.png)

**Figure** **10. DroidEdit screenshot of onceutf calc running on
Android tablet**

\

 

 

+--------------------------------------------------------------------------+
| :                                                                        |
+--------------------------------------------------------------------------+

Appendix E – Wakari, PythonAnywhere {style="margin-left:0in"}
===================================

![](onx2_files/image032.jpg)

** **

\

**Onceutf.py** runs on desktop and web platforms.  Both environments are
discussed in this section.

 

**Wakari** is a Python-Linux web platform that runs in the browser. 
Upload **onceutfnnn.py** and **mode.01.txt** to your Wakari account. 
Open a **bash shell** window (not Ipython) and type

\
 ***python onceutfnnn.py 0101.simple.txt –c***

 

at the command prompt, where nnn is the version number (i.e. 040).  The
program will output a model summary followed by the calc output (the –c
option echoes the output to stdout; use –b to echo output to the browser
when using the program locally). Use the browser file editor to review
and modify the files. 

** **

**![](onx2_files/image033.png)**

**Figure** **11. Wakari – terminal and editor in split windows**

** **

+--------------------------------------------------------------------------+
| :                                                                        |
+--------------------------------------------------------------------------+

**PythonAnywhere** is a Python-Linux web platform that runs in the
browser.  Upload **onceutfnnn.py** and **mode.001.txt** to your
**PythonAnywhere** account.  Open a **bash shell** window (not Ipython
or Python) and type

![](onx2_files/image034.jpg)\
 ***python onceutfnnn.py 0101.simple.txt –c***

 

at the command prompt, where nnn is the version number (i.e. 040).  The
program will output a model summary followed by the calc output (the –c
option echoes the output to stdout).  Edit files in the file editor.

![](onx2_files/image035.png) 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

\

**                Figure** **12.** **PythonAnywhere – side by side
browser windows**

\

 

 

** **

** **

** **

Appendix F – Minimum Programs and Libraries {style="margin-left:0in"}
===========================================

 

Note:  If the standard scientific distribution does not include a
library use the pip install method or in the case of Anaconda use
conda.  Other installed scientific libraries including SciPy, pandas,
rpy etc. may be installed by the distribution or installed separately
and will be available to **on-c-e** through functions and script
operations (see disk operations, Appendix B).

 

**Program**

**Python 2**

**Python 3**

**Notes**

** **

 

 

 

**onceutf **

**0.4.0**

**0.4.0**

 

**Python**

2.7.x  and above

3.4 and above

Python Platform

**Numpy**

1.7.x and above

1.8 and above

Python Library

**SymPy**

0.7.x and above

0.7.5 and above

Python Library

**Matplotlib**

1.2.x and above

1.3.1 and above

Python Library

**DejaVu fonts**

(note: **Unum** and **tabulate** are built-in classes of **onceutf**

2.3.4 and above

2.3.4 and above

UTF math fonts (external program)

 

 

 

 

**oncepy\
** in addition to above

**0.4.0**

**0.4.0**

 

**Unum**

4.1.x and above

4.1.x and above

Install with pip

**Tabulate**

0.7.x and above

0.7.x and above

Install with pip

**once.sty**

0.4.0

0.4.0

Customize PDF styles

**unitc.py**

0.4.0

0.4.0

Customize units

**oncepy  with PDF\
** in addition to above

**0.4.0**

**0.4.0**

 

**TeX Live**

2013 and above

2013 and above

Network install (external program)

**PyPDF2**

1.1x and above

1.1x and above

Install with pip

 

 

 

 

 

 

 

 

 

 

 

 

 

**Table** **4. Minimum required versions of programs and libraries**

 

 

 

 

 

+--------------------------------------------------------------------------+
| 1                                                                        |
+--------------------------------------------------------------------------+

Appendix G – Licenses {style="margin-left:0in"}
=====================

 

 

**oncepy, onceutf** and **on-c-e Komodo tools** are distributed under
the **MIT** or compatible license.  Copyright is retained by the code
author.

 

![](onx2_files/image036.png)

 

** **

**Figure** **13.**
[**http://opensource.org/licenses/MIT**](http://opensource.org/licenses/MIT)

\

 

![](onx2_files/image037.png)

 

**Figure** **14. http://creativecommons.org/publicdomain/zero/1.0/**

Template files uploaded to **once-db** are made available to others
under the CCO 1.0 Public Domain Dedication. A **Komodo** snippet is
provided for inserting license text in a template file:

 

**[\#] This file contains a generic on-c-e model template (the
template).**

**[\#] The template is distributed under the CCO 1.0 Public Domain
Dedication**

**[\#] http://creativecommons.org/publicdomain/zero/1.0/**

**[\#] The template is not a structural design calculation and**

**[\#] must be modified by the user prior to use.**

**[\#] The template user assumes sole and complete responsibility for**

**[\#] all existing or modified inputs and the computed model results.\
**

 

+--------------------------------------------------------------------------+
| \$                                                                       |
+--------------------------------------------------------------------------+

Appendix H – Security and Namespaces {style="margin-left:0in"}
====================================

** **

** **

** **

** **

**on-c-e** is designed to be a flexible and efficient tool for
structural analysis and design. It is also designed to facilitate
program verification by keeping the source code relatively compact. 
**onceutf.py** and **oncepy** are each about 1500 lines of source code
(about 3000 lines with comments).  Programming tradeoffs occur in
pursuing these objectives. 

 

The programs use Python **exec** and **eval** statements because it is
the simple, straightforward way to process the model operations. It is
possible to send input to **exec** and **eval** that does unexpected or
undesirable things. However the chances of this happening can be
controlled or eliminated with relatively little effort.  Sensible model
file input is tightly constrained and under the control of engineers and
designers who are running the models. Appropriate inputs, in the form of
structural analysis equations, arrays and functions are well known and
easily recognized by the engineers using the tool.  Because unsafe code
in the model would appear very different from these well understood
structural forms it is straightforward to spot and delete suspicious or
problematic model code before it is run.  Model security checks may be
added in the future but the only way to ensure proper operation of the
program is to check the input.

 

The programs also import **numpy**, **sympy** and other libraries in
their entirety into the model namespace.  This approach improves
readability and streamlines equation input but may introduce potential
problems with naming collisions. Some variable naming rules have been
developed and more will be added as experience is gained using the
program.  The programs currently includes some tools and methods for
checking collisions between model variable names and more will be added.

 

In summary, to make **on-c-e** more readable, useful and flexible, the
design philosophy chosen is code simplicity and transparency, along with
the obviousness of appropriate input as opposed to verbose and
restrictive input and processing policies. 

\

 

+--------------------------------------------------------------------------+
| :                                                                        |
+--------------------------------------------------------------------------+

Appendix I – Examples {style="margin-left:0in"}
=====================

 

This appendix includes the PDF calc output for each example. The PDF
calcs are followed by inputs and outputs for each example, in order:
**(1)** model **(2)** UTF calc **(3)** IPython file\
 **(4)** function file **(5)** summary file **(6)** log file.  Download
example files at <http://on-c-e.org>.

**00\_Simple:** 0001.simple.txt ****

**               Demonstrates:** sections, terms and equations

**01\_Template:** 0101.template.txt** **

**              ** Sections, terms, equations and inline
reStructuredText

**02\_Bearing:** 0201.bearing.txt 

**              ** Figures, complex equations, limit checks

**03\_Deflection:** 0301.deflection.txt

               Figures, arrays, equation expansion options

**04\_Seismic:**  

0401.bldg\_info.txt       term lists, inline reStructuredText

0402.seismic.txt                      built-in math functions

0403.seismic.txt                      comodels, symbolic expressions

0404.frame.txt             sections, arrays

0405.brace.txt             limit checks

**05\_Eigenvector:**  0501.eigenvector.txt

                        External functions, plotting and linear algebra
library.

**06\_OpenSees:**  0601.truss.txt

               Read, edit and disk operations for external programs and
data

**07\_Matrix:**  0701.stiffness.txt

                        External functions, plotting and linear algebra
library

 

*** ***

** **

Index {style="margin-left:0in"}
=====

  {style="margin-left:0in"}
=

 

\

**0101.template.txt**, 7, 42

Android, 8, 32, 34, 35

**arrays**, 11, 25, 26, 27, 41, 42

ASCII, 9

calc, 6, 7, 9, 10, 11, 23, 24, 28, 29, 31, 36, 37, 42

calculation, 5, 7, 8, 9, 27, 32

**DejaVu**, 14, 31, 38

**Download**, 7, 14, 31

equations, 12, 25, 27

fonts, 14, 31, 32

Fonts, 14

**format**, 11, 12, 23, 24, 25, 26, 27, 28, 29

functions, 23, 42

IDE, 8, 14

**install**, 14, 38

interactive analysis, 5, 8, 9, 15

iOS, 8, 32, 33

**IPython**, 4, 5, 8, 9, 15, 16, 42

**Komodo Edit**, 14

**LaTeX**, 29

Linux, 8, 32, 36, 37

**MATLAB**, 8

model, 7, 8, 9, 10, 11, 14, 23, 24, 25, 28, 31, 32, 36, 37, 40

***on-c-e***, 2, 5, 7, 8, 14, 31, 38, 39

**once-db**, 8, 40

**onceutf**, 8, 14, 25, 32, 33, 34, 38, 41

**OpenSees**, 42

OSX, 8

**PDF**, 10, 12, 38

project, 4, 5, 7, 9, 10, 11, 14, 28, 29

Python, 7, 8, 10, 14, 23, 26, 27, 36, 37, 38

**PythonAnywhere**, 7, 36, 37

**Pythonista**, 8, 33

**QPython**, 8, 34

**sections**, 11, 23, 27, 42

**sqlilte**, 15

template, 6, 7, 8, 24, 29, 31, 40

terms, 25, 27

**TexLive**, 31

**Upload**, 7, 14, 36, 37

UTF, 5, 10, 24, 31, 32, 38, 42

UTF-8, 5, 10, 24, 32

**Wakari**, 7, 8, 36

Windows, 8, 32

\

 

 

 

 

 

 

 

 

 

 

**ã** **StructureLabs**

       15 Blanca Drive

     Novato, CA  94947

Phone 415.314.8453 **• rholland@structurelabs.com**

 

\

 

