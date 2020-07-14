**RivetCalc** is a cross-platform, open source tool for writing 
engineering calculation documents.  It's implemented as a Python 
library that produces formatted calculation documents and reports 
in  UTF8, HTML and PDF file formats.  The tool is designed  to 
improve editing, explicitness, clarity, reuse and review.  It 
eliminates the problem of unusable calculations arising from incompatible 
binary input files and other program version incompatibiilties. 

Calculations are written in **rivet**, a light-weight, context based,
indexed markup language. The language includes a dozen commands, tags, 
and a subset of reStructuredText that may be mixed arbitrarily with
utf-8 text strings.

The RivetCalc API consistes of five functions:

========== =======================================================
Function    Description
========== =======================================================
 R()        repository, report and calc summary information
 I()        insert descriptive text, tables, figures and equations
 V()        define and import values 
 E()        define and import equations and functions
 T()        define tables and plots 
========== =======================================================

A **RivetCalc** file is a Python file that typically imports 
*rivetcalc.rc_lib as rc* and calls the API functions as 
rc.R('''**rivet-string**''') where **rivet-string** contains **rivet**
commands and tags.

Input file names have the form *rddcc_calcname.py*. Corresponding 
output files have the names *rddcc_calcname.txt*, *rddcc_calcname.html*, 
or *rddcc_calcname.pdf*;where dd (division) and cc (calculation) are 
two digit numbers used to organize the PDF and HTML documents and reports. 

===================  =====================================================
File type             File description                                      
===================  =====================================================
design (.py)          text input, written in rivet                      
calc (.txt)           formatted UTF-8 output, written to screen (and file) 
doc (.pdf or .html)   formatted HTML or PDF output, written to file                  
report (.pdf)         organized and formatted PDF docs, written to file
===================  =====================================================       

All files needed for a calcuation are stored in a project folder tree.  Calcs 
are written to the *calcs* folder in UTF-8 format.  Docs and reports are written 
to their respective folders in PDF and HTML formats when specified. Binary 
image files used in the docs and reports are stored in the *html* folder. The user 
initially creates the complete folder tree either by scratch or starting with
a template::

  Project_Name (chosen by user)
      |- calcs
          |- sketches
          |- scripts
          |- tables
          |- text
          |- temp
      |- docs
          |- html
      |- reports
          |- attachments

Folders are restricted in the types of files they contain. The *calcs* folder 
and sub-folders contain only UTF-8 files. Binary files, including image and 
PDF files, are stored in the *docs* and *reports* folders.

**RivetCalc** templates are full project trees with  UTF-8 *calcs* folders that
fully define a calc or set of calcs. The *docs* and *reports* folders are 
empty except for a few default config files (needed to keep the folder structure 
intact on Github). Templates have the form::

  RivetCalcTemplate_nnn (nnn is a unique three digit number)
      |- calcs
          |- sketches
          |- scripts
          |- tables
          |- text
          |- temp
      |- docs
          |- html
      |- reports
          |- attachments

Where RivetCalcTemplate_nnn is the literal Github repository 
name with a unique number that facilitates searching for terms within
the calculations. RivetCalc templates may be cloned, downloaded as a zip
file or run on Gitpod.

A minimum working version of **RivetCalc** includes a Python 
installation with a dozen Python science libraries 
(https://github.com/rivetcalcs/rivet-code/requirements.txt) 
and a text editor. If a LaTeX distribution is installed, 
formatted PDF documents and reports can be generated. If an IDE 
code editor is used the calculations can be executed and output 
interactively and in stages by marking functions or groups 
of funcitons as cells. The documentation focuses on the use 
case of a **VSCode** IDE, which dramatically increases efficiency.

**RivetCalc** may be run in interactive mode, using an interactive 
code editor like VSCode, or from the command line:: 

    python -m rivet ddcc_calcname.py 

The program execution flow follows::

                     /--------------------------------\                    
                     |   Run RivetCalc design file    |
                     |   or cells.                    |                   
                     |                                |
                     |          cell types:           |                    
                     |    r__, i__, v__, e__, t__     |                    
                     \--------------------------------/                    
                                     \/                                    
  +--------------+|  +--------------------------------+  +-------------+
  |    Process    |  |   Working in interactive IDE?  |  |  Process    |   
  |    cell or    |  |     (VSCode, Spyder, Pyzo)     |  |  file       |   
  |    file       <--+ YES                         NO +-->             |   
  +------+--------+  +--------------------------------+  +------+------+   
         |           +================================+         |          
         |           |  Write utf-8 calc to :         |         |          
         +===========>    terminal   |  file          <=========+            
                     |================================|                    
                     +================================+                    
                                     \/
                     +================================+                    
                     |   Write reST calc file if      |
                     |   complete file is processed.  |       
                     |================================|                    
                     +================================+                    
                                     \/
  +===============+  +--------------------------------+                    
  | Write HTML    |  |                                |  /---------\    
  | or PDF doc    |  |         Write docs?            |  |   End   |   
  | files         <==+ YES                         NO +==>         |   
  |===============|  +--------------------------------+  \---------/ 
  +=====+=========+        
        |            +--------------------------------+  /---------\   
        |            |         Write report?          |  |   End   |   
        +============>                             NO +==>         |   
                     +----------------+---------------+  \---------/ 
                                     \/ YES
                     +================================+                    
                     |    Write PDF report file       |                    
                     |================================|                    
                     +================================+    
                     
                     
**RivetCalc** may be installed by:

1. Locally Installing and configuring the individual open source components (about a half dozen steps).
2. Locally downloading and unzipping a single no-install file for Windows (a couple of steps).
3. Remotely running a cloud service in a container (about a dozen steps). 

A cloud installation (**RivetCloud.net**) is available with paid support. 
Refer to the User Manual for details.

                               
                                                                           
                                                                          
