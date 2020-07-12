**RivetCalc** (https://github.com/rivetcalc/rivetcalc-code) is a cross-platform,
open source calculation tool for writing engineering calculation documents.  
It is implemented is a Python package and produces formatted calculation documents 
and reports in  UTF8, HTML and PDF file formats from Python files written 
in the **rivet** light-weight markup language. The program is designed  
to improve calculation editing, reuse, review and clarity, and 
eliminate the problem of unreadable calculation input files 
arising from binary formats or program changes.

The minimum working version of **RivetCalc** includes a Python installation 
with science libraries (conda is an example), and a text editor.  code 
editor (VS Code and Pyzo are examples), a LaTeX distribution (TexLive or 
MikTex are examples) and the **rivet** package. If docs 
(see below) are not needed then the LaTeX distribution may be omitted.

**RivetCalc** components may be individually installed and configured 
by the user on a workstation, downloaded as a no-install Windows expanded 
zip folder (**r-i-v-e-t-s_32.zip** or **r-i-v-e-t-s_64.zip**), or used 
remotely (paid service) with a VS Code front end, support and private 
cloud storage (http://www.rivet-calcs.net).   

A **RivetCalc** file is a Python file that imports the *rivet* library
and contains **rivet** calculation strings. The input (rivet) and 
output (calc) files have names of the form *ddcc_calcname.py*  and 
*ddcc_calcname.txt* respectively, where dd (division) and 
cc (calculation) are two digit numbers that organize the 
PDF and HTML documents (docs) and reports. 

The program may be run in interactive mode, using an interactive 
code editor like VS Code and importing *rivet-lib*, or from the 
command line:: 

    python -m rivet ddcc_calcname.py 

Supporting files used in calcs are stored in a project folder 
tree.  Calcs are written to the *calcs* folder in UTF8 format, 
and the *docs* and *reports* folders in PDF and HTML formats 
when specified. The user creates the folder
structure either by copying a template or from scratch::

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

A template for sharing a project on Github under the MIT license has the form::

  RivetCalcTemplate_nnn (Repository name where nnn are numbers)
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

Files in the *calcs* folder are in  ASCII or UTF-8 format only. The 
folder tree *calcs* 
folder may be uploaded to a personal github repository and shared 
under the MIT open source license through the **on-c-e** (OpeN Calculation Exchange) database 
front end at http://www.on-c-e.net/distribute/. For a **on-c-e** overview see 
http://www.rivet-calcs.net. The program flow is::

                     /--------------------------------\                    
                     |    Process RivetCalc file or   |
                     |    cells in interactive mode.  |                   
                     |    
                     |    cell types:                 |                    
                     |    r__, i__, v__, e__, t__     |                    
                     \--------------------------------/                    
                                     ||                                    
  +---------------+  +---------------\/---------------+  +-------------+   
  |               |Y |                                |  |             |   
  |    Process    |E |    Working in IDE              | N|  Process    |   
  |    cell or    |S |    interactively?              | O|  file       |   
  |    file       <--+    (VSCode, Spyder, Pyzo)      +-->             |   
  +------+--------+  +--------------------------------+  +------+------+   
         |           +================================+         |          
         |           |   Write utf-8 calc to          |         |          
         +===========>  terminal (and file).          <=========+            
                     |================================|                    
                     +================================+                    
                                      || 
                                      \/
                     +================================+                    
                     |    Write reST calc file if     |
                     |    complete file is            |       
                     |    processed.                  |                    
                     |================================|                    
                     +================================+                    
                                      ||
                                      \/
  +===============+  +--------------------------------+                    
  |               |Y |                                |  /-------------\             |   
  | Write HTML    |E |                                | N|             |   
  | or PDF doc    |S |     Write docs?                | O|   End       |   
  | files         <==+                                +==>             |   
  |===============|  +--------------------------------+  \-------------/ 
  +=====+=========+        
        |            +--------------------------------+  /-------------\   
        |            |                                | N|             |   
        |            |     Write report?              | O|   End       |   
        +============>                                +==>             |   
                     +----------------+---------------+  \-------------/ 
                                     ||Yes                                   
                                     \/
                     +================================+                    
                     |    Write PDF report file       |                    
                     |================================|                    
                     +================================+                    
                                      ||
                                      \/
                     /--------------------------------\                    
                     |           End                  |                    
                     \--------------------------------/                       
                               
                                                                           
                                                                          
