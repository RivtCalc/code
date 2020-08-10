Program Structure
----------------- 

**RivtCalc** is a cross-platform, open source tool for writing engineering
calculation documents. The intention is to improve calculation clarity and
reuse. It is implemented as a Python library that produces calculation
documents and reports in UTF8, HTML and PDF file formats from plain text input.
Calculations are written in **rivt**, a light-weight, procedural markup
language. The language includes a dozen commands and tags, and incorporate a
subset of reStructuredText.

A **RivtCalc** file is a Python file that imports *rivtcalc.rc_lib as rc* and
calls functions on **rivt-strings**. A **rivt-string** contains text,
commands and tags defining the calculation. A function call is of the form::

  rc.V(''' several line rivt-string ''')

Input file names (models) have the form *rddss_modelname.py*. Corresponding
output files (calcs, docs and reports) have the names *rddss_calcname.txt*,
*rddss_calcname.html*, or *rddcc_calcname.pdf*; where *ddss* is the calculation
number made up of the division (*dd*) and sequence (*ss*) numbers which are
used to organize PDF documents into collated reports.

Files
=====
===================  =====================================================
File type             File description                                      
===================  =====================================================
model (.py)           input model written in **rivt**                      
calc (.txt)           formatted UTF-8 output, written to screen (and file) 
doc (.pdf or .html)   formatted HTML or PDF calc output, written to file                  
report (.pdf)         formatted and collated PDF doc, written to a file
===================  =====================================================       

The **RivtCalc** API consists of four functions that take a **rivt-string** as
input and four functions that control the output format.

API Functions
=============
================ =======================================================
 API              Description
================ =======================================================
  R()            repository, report and calc summary information
  I()            insert descriptive text, tables, figures and equations
  V()            define and import values, equations and functions 
  T()            define and import tables and plots   
write_utfcalc()  write utf calc to file
write_pdfdoc()   write pdf doc to file (includes images)
write_htmldoc()  write html doc to file (includes images) 
write_report()   compile pdf docs into a report
================ =======================================================

All calculation and supporting files are stored in a structured project tree.
UTF-8 model input and output are stored in the *calcs* folder. Docs are written
to their respective folders in PDF or HTML formts. PDF reports are written to
the *reports* folder. Binary image files used in docs and reports are stored in
the *html* folder. The user initially starts a project by copying a complete
folder tree from a prior project or template.

Project Folder Tree
=================== 
::

  Project_Name (chosen by user)
      |- calcs
          |- data
          |- scripts
          |- sketches
          |- text
          |- temp
      |- docs
          |- html
      |- reports
          |- attachments

Reuse and sharing
-----------------

File types are categorized into folders to facilitate calc organization,
version control and sharing. The *calcs* folder and sub-folders contain only
UTF-8 or ASCII files. Binary files, including image and PDF files, are stored
in the *docs* and *reports* folders. A shared project or calc includes the full
project tree containing only text (ASCII, UTF-8) files. The calcs folder is
typically fully populated and the *docs* and *reports* folders contain only
config files. A shared template on Github has the following form:

Shared Project Template Tree
============================ 
::

  RivetCalcTemplate_nnnn (nnnn is a unique three digit number)
      |- calcs
          |- sketches
          |- scripts
          |- tables
          |- text
          |- temp
      |- docs (config file only)
          |- html (config file only)
      |- reports (config file only)
          |- attachments (config file only)

**RivtCalcTemplate_nnnn** is the standard Github repository name where nnnn is
a unique four digit number. This shared common name across Github accounts and
repositories facilitates searches. Each account may contain many repositories
(templates). **RivtCalc** templates may be cloned, downloaded as a zip file, or
run directly on Digital Ocean, Gitpod or repl.it with the addition of a few
setup files.

Minimum Setup and Execution
---------------------------

The minimum working version of **RivtCalc** on a PC workstation includes a
Python installation with about a dozen Python science libraries
(https://github.com/rivetcalcs/rivet-code/requirements.txt) and a text editor.
In this case the input model is run from the command line as::

  python -m rivtcalc ddss_modelname.py 

If a LaTeX distribution is installed, formatted PDF documents and reports can
be generated. If an IDE or full-featured code editor is used the calculations
can be executed interactively and in stages by tagging the API functions as
cells. Execution steps include::

                     /--------------------------------\                    
                     |     Edit and run RivtCalc      |
                     |     model file or              | 
                     |     interactive cells.         |                   
                     |                                |
                     |    cell or function types:     |                    
                     |       R(), I(), V(), T()       |                    
                     \---------------||---------------/                    
                                     \/                                    
  +--------------+|  +--------------------------------+  +-------------+
  |    Process    |  |   Working in interactive IDE?  |  |  Process    |   
  |    cell or    |  |     (VSCode, Spyder, Pyzo)     |  |  file       |   
  |    file       <--+ YES                         NO +-->             |   
  +------+--------+  +--------------------------------+  +------+------+   
         |           +================================+         |          
         |           |    Write utf-8 calc to :       |         |          
         +===========>    terminal  or  file          <=========+            
                     |================================|                    
                     +===============||===============+                    
                                     \/
                     +================================+                    
                     |   Write reST calc file if      |
                     |   complete file is processed.  |       
                     |================================|                    
                     +===============||===============+                    
                                     \/
  +===============+  +--------------------------------+                    
  | Write HTML    |  |                                |  /---------\    
  | or PDF doc    |  |         Write docs?            |  |   End   |   
  | files         <==+ YES                         NO +==>         |   
  |===============|  +--------------------------------+  \---------/ 
  +=====+=========+        
        |            +--------------------------------+  /---------\   
        |            |         Write report?          |  |   End   |   
        +============>               YES           NO +==>         |   
                     +---------------||---------------+  \---------/ 
                                     \/ 
                     +================================+                    
                     |    Write PDF report file       |                    
                     |================================|                    
                     +================================+    
                     
                     
**RivetCalc** may be installed by:

- Locally installing and configuring the individual open source components.
- Locally downloading and unzipping a pre-configured installation (Windows only).
- Remotely installing as a cloud service in a container. 

Pre-installed cloud installations (**RvetCloud.net**) that run through a
broswer are available with paid support. Refer to the **RivtCalc User Manual**
for details.

Efficient IDE Development
-------------------------

By far the most efficient way to write **rivt** models is to use a full
featured code editor or IDE like Microsoft VSCode. Use of VSCode is extensibly
documented in the **RivtCalc User Manual**. When working in VSCode the models
can be written and evaluated step by step and graphics can be output inline.

