**RivetCalc** (https://github.com/rivetcalc/rivetcalc-code) is a 
cross-platform, open source tool for writing engineering calculation documents.  
It is implemented as a Python library and produces formatted calculation 
documents and reports in  UTF8, HTML and PDF file formats.  
The tool is designed  to improve editing, reuse, review and clarity, 
and eliminate the problem of unreadable calculation inputs
that arise from binary input files and program incompatibiilties.
Calculations are written in **rivet**, a light-weight and 
context sensitve markup language. 

The **rivet** language includes a dozen commands and tags and a subset of 
reStructuredText that are used within five funtions that take a text
string as an argument. The functions are:

========== =======================================================
Function    Description
========== =======================================================
r __        repository, report and calc summary informtion

i __        insert descriptive text, tables, figures and equations

v __        define and import values 

e __        define and import equations and functions

t __        define tables and plots 

========== =======================================================

A **RivetCalc** file is a Python file that imports the *rivet* library
and contains **rivet** calculation strings. The input (rivet) and 
output (calc) files have names of the form *ddcc_calcname.py*  and 
*ddcc_calcname.txt* respectively, where dd (division) and 
cc (calculation) are two digit numbers used to organize the 
PDF and HTML documents and reports. 

===================  =====================================================
File type             File description                                      
===================  =====================================================
design (.py)          text input, written in rivet                      
calc (.txt)           formatted UTF-8 output, written to screen (and file) 
doc (.pdf or .html)   formatted HTML or PDF output, written to file                  
report (.pdf)         organized and formatted PDF docs, written to file
===================  =====================================================       

Design and supporting files are stored in a project folder 
tree.  Calcs are written to the *calcs* folder in UTF8 format.  
The *calcs* folder also contains calculation supporting files.
Docs and reports are written to their respective folders in 
PDF and HTML formats when specified. Binary image files used
in the calcs are stored in the *html* folder. The user 
initially creates the complete folder
tree either by copying a template or from scratch::

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

Folders are restricted in the types of files they contain. A calc folder 
contains only ASCII or UTF-8 files. Templates are full project trees with 
*calc* folders they fully define the desing and only default config files 
in the *docs* and *reports* folders. Templates shared and discovered on 
Github have the form::

  RivetCalcTemplate_nnn (Github repository name, where nnn are numbers)
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

The minimum working version of **RivetCalc** includes a Python 
installation with a dozen Python science libraries 
(https://github.com/rivetcalcs/rivet-code/requirements.txt) 
and a text editor. If a LaTeX distribution is installed, 
formatted PDF documents and reports can be generated. If an IDE 
code editor is used the calculations can be executed and output 
interactively and in stages. Documentation addresses the use case
of the VSCode IDE, which dramatically increases efficiency.

The program may be run in interactive mode, using an interactive 
code editor like VS Code and importing *rivet-lib*, or from the 
command line:: 

    python -m rivet ddcc_calcname.py 

The program execution flow is::

                     /--------------------------------\                    
                     |    Run RivetCalc file or       |
                     |    cells in interactive mode.  |                   
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
                     |    Write reST calc file if     |
                     |    complete file is output.    |       
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
                     
                     
A **RivetCalc** may be installed by:

1. Individually installing and configuring the open source components
2. Downloading and unzipping a single no-install file for Windows (**r-i-v-e-t-s_32.zip** or **r-i-v-e-t-s_64.zip**) 
3. Running as a cloud service in a container (also available with paid support, see **RivetCloud.net**)

Refer to the User Manual for details.

                               
                                                                           
                                                                          
