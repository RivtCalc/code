#!/usr/bin/env python
# makes folder a package
"""rivet

The *rivet* Python package and language produces formatted engineering 
calculation document files in UTF8, HTML and PDF formats using
the open source **r-i-v-e-t** environment.  The language is
designed to improve document editing, reuse, review and clarity. The
program and documentation are here: https://github.com/r-i-v-e-t .  The
r-i-v-e-t environment includes a Python installation with science libraries
(Anaconda is an example), an interactive open source code editor (VS Code and 
Pyzo are examples), a LaTeX distribution (TexLive and MikTex are examples) and
the rivet library.

A **rivet** calc is a Python file importing the *rivet* library
and containing calculation strings in the **rivet** language format.
Calc files have names of the form *ddcc_calc_name.py* where dd and cc
are two digit numbers identifying a division and calculation number
respectively. Calculation and Division numbers are used to organize 
**rivet** reports. 

The calcs and supporting ASCII input files are stored in a project 
folder tree set up by the user. Output calculations are written to the *calcs* 
directory in UTF8 format and the *docs* and *reports* directory in 
PDF and HTML formats::

  Project_Name (chosen by user)
      |- calcs
          |- sketches
          |- scripts
          |- tables
          |- text
      |- docs
          |- HTML
              |- figures
      |- reports
          |- attachments
          |- temp

An error will be raised if the program is run and the folder structure is not 
complete.  The program may be run in interactive mode, using an interactive 
code editor like VS Code, or from the command line.

.. code:: python

    python -m rivet rddcc_ design_filename.py 

**r-i-v-e-t** calcs can be shared through the **on-c-e** (OpeN Calculation Exchange)
database at http://on-c-e.net.  For **on-c-e** overview see http://rivet-calcs.net .

The overall program flow is shown below:
                     /--------------------------------\                    
                     |                                |                    
                     |  Read rivet file (or strings   |                    
                     |  in interactive mode).  String |                    
                     |  types:                        |                    
                     |                                |                    
                     |     r__, i__, v__, e__, t__    |                    
                     |                                |                    
                     |                                |                    
                     |                                |                    
                     \----------------+---------------/                    
                                      |                                    
  +---------------+  +----------------\/--------------+  +-------------+   
  |               |  |                                |  |             |   
  |               |  |                                |  |             |   
  |    process    |  |    is string type r__?         |  | parse and   |   
  |    Python     |Y |                                | N| process     |   
  |    code       <--+                                +--> rivet       |   
  |               |  |                                |  | strings     |   
  |               |  |                                |  |             |   
  +------+--------+  +--------------------------------+  +------+------+   
         |                                                      |          
         |           +================================+         |          
         |           |                                |         |          
         |           |                                |         |          
         |           |   generate utf-8 calcs to      |         |          
         |           |   terminal and files           |         |          
         +----------->                                <---------+          
                     |                                |                    
                     |                                |                    
                     +================================+                    
                     +================================+                    
                                      |                                    
                     +================\/==============+                    
                     |                                |                    
                     |                                |                    
                     |    write reST calcs to file    |                    
                     |                                |                    
                     |                                |                    
                     |                                |                    
                     |                                |                    
                     +================================+                    
                     +================================+                    
                                      |                                    
  +===============+  +----------------\/--------------+                    
  |               |  |                                |  /-------------\   
  |               |  |                                |  |             |   
  | write HTML    |  |                                |  |             |   
  | or PDF doc    |Y |     write docs?                | N|   End       |   
  | files         <--+                                +-->             |   
  |               |  |                                |  |             |   
  |               |  |                                |  |             |   
  +===============+  |                                |  \-------------/   
  +=====+=========+  +--------------------------------+                    
        |                                                                  
        |            +--------------------------------+                    
        |            |                                |  /-------------\   
        |            |                                |  |             |   
        |            |     write reports?             |  |             |   
        |            |                                | N|   End       |   
        +------------>                                +-->             |   
                     |                                |  |             |   
                     |                                |  |             |   
                     |                                |  \-------------/   
                     +----------------+---------------+                    
                                      |Y                                   
                     +================\/==============+                    
                     |                                |                    
                     |                                |                    
                     |    write HTML or PDF report    |                    
                     |    files                       |                    
                     |                                |                    
                     |                                |                    
                     |                                |                    
                     +================================+                    
                     +================================+                    
                                      |                                    
                     /----------------\/--------------\                    
                     |                                |                    
                     |                                |                    
                     |           End                  |                    
                     |                                |                    
                     |                                |                    
                     \--------------------------------/                    
                                                                           
                                                                           



"""