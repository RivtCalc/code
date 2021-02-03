Program Structure
----------------- 

**rivtlib** is an open source Python library for producing engineering calculation 
documents. It simplifies writing, checking and sharing calculations and 
runs on all desktop, mobile and server platforms. It produces calculation
documents and reports in UTF8, HTML and PDF file formats from plain text input.
Calculations are written in **RivtText**, a light-weight, procedural markup
language. The language includes commands and tags, and incorporates a
subset of reStructuredText.

A **rivt** file is a Python file that imports *rivtlib.rv_lib as rv* and
calls functions on **rivt-strings** which are plain text and include
commands and tags defining the calculation. 

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

The **rivtlib** API consists of five functions that take a **rivt-string** as
input (only four produce output) and a function that controls the output format.
A function call is of the form::

  rc.V(''' several line rivt-string ''')

API Functions
=============
================ =======================================================
 API              Description
================ =======================================================
  rv.R()            repository, report and calc summary information
  rv.I()            insert descriptive text, tables, figures and equations
  rv.V()            define and import values, equations and functions 
  rv.T()            define and import tables and plots   
  rv.S()            skip processing of string (used for calc debugging)
  rv.D()            controls document output type and format
================ =======================================================

Reuse and sharing is simplified by standardizing the file and folder structure for a calculation project.  Each rivt file is stored in a rivt project folder and identified with a name that starts with a four digit calc number of the form:

cddnn_filename.py

where dd is the division and folder number and ddnn is the calc number.  The two subfolders under the project folder are calcs and docs. The calcs folder includes all of the plain text input files and output calc files (.txt and .tex). The docs folder includes all of the binary inputs (i.e. images) and  calc documents (.pdf and .html).  The calcs folder contains only plain text files.  This division of file types makes it easy to share and impose version control on the primary calculation inputs. rivtlib includes functions that automate sharing to GitHub. 

A **rivt** project is started by copying the folder structure from a similar existing project.  The calcs folder will always be available.  The docs folder can be copied and derived from the calcs folder..  In summary, **rivtlib** reads string functions in a .py file as input and outputs a plain text calculation to the calcs folder.  Options are available to write pdf or html files and reports to the docs folder   Functions are available to assemble complete project reports from pdf files.

Example project folder tree:

::

    rivtproject_name 
       calcs
          c00 (config data)
             units.py
          c01_loads
             c0101_gravity.py
             c0102_wind.py 
             c0101_gravity.txt     
             c0102_wind.txt
          c02_beams
             c0201_floor.py
             c0202_roof.py
             c0201_floor.txt
             c0202_roof.txt
       docs
          d00 (project/config data)
             pdf_style.sty
             config.txt
             project_data.xlsx    
          d01_loads
             image1.jpg
             d0101_gravity.pdf
             d0102_wind.pdf      
          d02_beams
             image2.jpg
             attachment.pdf
             d0201_floor.pdf
             d0202_roof.pdf
          html
             resources 
                image3.png
             index.html
             d0101_gravity.html
             d0102_wind.html
             d0201_gravity.html
             d0202_wind.html


Minimum Setup and Execution
---------------------------

**RivtCalc** refers to the complete framework for writing calculations. The minimum 
working version of **RivtCalc** on a PC workstation includes a
Python installation with a dozen Python science libraries
(https://github.com/rivtcalcs/rivt-code/requirements.txt) and a text 
editor.  In this case the input model is run from the command line as::

  python -m rivtlib cddnn_filename.py 

If a LaTeX distribution is installed, formatted PDF documents and reports can
be generated. If an IDE or full-featured code editor is used the calculations
can be executed interactively and in stages by tagging (# %%) the API functions as
cells. Execution steps include::

                     /--------------------------------\                    
                     |     Edit and run rivt file     |
                     |     or interactive cells.      |                   
                     |                                |
                     |    cell or function types:     |                    
                     |       R(), I(), V(), T()       |                    
                     \---------------||---------------/                    
                                     \/                                    
  +---------------+  +--------------------------------+  +-------------+
  |   Process     |  |   Working in interactive IDE?  |  |  Process    |   
  |   cell to     |  |     (VSCode, Spyder, Pyzo)     |  |  file       |   
  |   terminal    <--+ YES                         NO +-->             |   
  +------+--------+  +--------------------------------+  +------+------+   
         |           +================================+         |          
         |           |    Write utf-8, reST, TeX      |         |          
         +===========>    calc to file                <=========+            
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
                     
                     
**RivtCalc** may be installed by:

- Locally installing and configuring the individual open source components.
- Download and unzipping a pre-configured installation (Windows only).
- Remotely installing as a cloud service in a container. 

Pre-installed cloud installations (**RvetCloud.net**) that run through a
broswer are available with paid support. Refer to the **RivtCalc User Manual**
for details.

Efficient IDE's
---------------

By far the most efficient way to write **rivt** models is to use a full
featured code editor or IDE like Microsoft VSCode. Use of VSCode is extensibly
documented in the **Rivt User Manual**. When working in VSCode the models
can be written and evaluated step by step and graphics can be output inline.  Other
options include Pyzo and Spyder.

'Rivt User Manual <http://www.rivtdocs.net>'

Learning Curve
--------------

The estimated time to set up **RivtCalc** and begin producing calculations is
about 15 minutes for portable program, one hour for people familiar with Python, and about four hours for those
starting from scratch.


