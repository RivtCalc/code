#! python 
#%%
from rivet.rivet_lib import *
r__(''' repository data

    || summary | section The r__ function contains summary calc information
    used in repositories and dababases. It writes an .rst file that can be
    uploaded to a GitHub gist or repository. The **summary** command includes
    this paragraph, an optional a table of contents at the level of sections or
    functions, and an optional listing of docstrings used in imported
    functions. The file contents are also appended to the front of the calc
    output.

    || label | rivet
    field, structures, buildings
    assemblies,  floor, wall  
    materials, concrete, steel 
    components, beams, columns 
    loads, fire, seismic, vibration           
    analysis, series, spectrum, nonlinear 
    codes, ACI318-2005, CBC-200
    notes, damage estimates, cracked concrete

    [link]_ http://www.github.com

    || append | cover
    myreport1.pdf, A. Some Data
    myreport2.pdf, B. Some Tables 

    ''')
#%%  
i__(''' [01]_ Load Sums 
    
    The need to distinguish between the various meanings of "frame of
    reference" has led to a variety of terms. For example, sometimes the type
    of coordinate system is attached as a modifier, as in Cartesian frame of
    reference [#]_.
    
    [foot]_ footnote text 1

    Sometimes the state of motion asfda asd s fdas sfdfasdfasdf is emphasized,
    as in rotating frame of reference.

    :: 

                        2
                    d w
             M = -EI ───                                 
                        2
                    dx 

            
                            (x + i y)
                ┌── 10   ijk
             ζ= >     ────────────                            
                └── i=4   (γ+ 4)
    
    
    Render equations
    ----------------
    
    || latex : 1 | x = \\frac{1 + \\omega}{2 + \\gamma} 
    ACI 318-05 5.5.1

    ACI 318-05 5.5.2 [r]_
    || sympy : 1 | x = (12 + omega + α) / (14 + gamma)  

    Render image file
    -----------------
    || image : .5 | pic1.png 
    Inserted png file
        
    || image | pic2.jpg 

    Some added text xxxx is put here and a bit of nonsense to make some words
    for a paragraph.

    Insert table from csv and rst files
    ------------------------------------
    || table : 50 | mercalli.csv   
    Rebar Table from CSV file
    
    note1: abc
    note2: def

    || table | rebars.rst     
    Rebar Table from reST file
    
    || table | inline 
    Inline Table Title
    +-----------+-------+--------+-------------+-----------+
    |   barsize |   dia |   area |   perimeter |   wt/foot |
    +===========+=======+========+=============+===========+
    |         2 | 0.25  |   0.05 |        0.79 |     0.167 |
    +-----------+-------+--------+-------------+-----------+
    |         3 | 0.375 |   0.11 |        1.18 |     0.376 |
    +-----------+-------+--------+-------------+-----------+
    |         4 | 0.5   |   0.2  |        1.57 |     0.668 |
    +-----------+-------+--------+-------------+-----------+
    |         5 | 0.625 |   0.31 |        1.96 |     1.043 |
    +-----------+-------+--------+-------------+-----------+
    |         6 | 0.75  |   0.44 |        2.36 |     1.502 |
    +-----------+-------+--------+-------------+-----------+
    |         7 | 0.875 |   0.6  |        2.75 |     2.044 |
    +-----------+-------+--------+-------------+-----------+
    |         8 | 1     |   0.79 |        3.14 |     2.67  |
    +-----------+-------+--------+-------------+-----------+
    |         9 | 1.128 |   1    |        3.54 |     3.4   |
    +-----------+-------+--------+-------------+-----------+
    |        10 | 1.27  |   1.27 |        3.99 |     4.303 |
    +-----------+-------+--------+-------------+-----------+
   
    ''')

v__(''' some values 
    
    || values | inline | Steel Properties
    a11 = 12.23                 | description 1 
    a22 = 2.2                   | description 2 
    a33 = 14                    | description 3 
    BEAM1 => aisc13.csv[4]      | steel property vector 
    I_x = BEAM1[2]              | I major
    I_y = BEAM1[3]              | I minor

    || values | 0103_values.py | Rebar Properties

    a11 ==                      | reprint a value


    ''')

e__(''' equations header
    
    Some introductory text.  Set equation format.

    || format | equ:2,ans:2,chk:0,prt:2
    
                                            ACI 318-05 1.1 [r]_
    aa1 = a11*14                    

    aa2 = a11*14  

                                            ACI 318-05 1.2 [r]_
    aa3 = (aa2 * 5)/a11             
    
    aa4 = BEAM1[4] * 7.2  
    
    ''')
#%%
i__(''' [02]_ Seismic Analysis
    
    This is a test γ = 2*Σ of the system and this is a further test and
    another greek letter Γ₂.

    The need to distinguish between the various meanings of "frame of
    reference" has led to a variety of terms. For example, sometimes the
    type of coordinate. 
    
    [page]_

    || image2 : .5,.5 | pic1.png | pic2.png 
    Inserted png file
    Side by side in docs

    The way it transforms to frames considered as related is emphasized as
    in Galilean frame of reference. Sometimes frames are distinguished by
    the scale of their observations, as in macroscopic and microscopic
    frames of reference [CIT2000]_.

    || cite | CIT2000 | citation text

    ''')

v__(''' some values

    || values | nodoc
    0102_values.py

    this is one line 4 γ
  
    gg = 5.4    | height of roof 
    hh = 12.2   | height of balcony
    w1 = 2.2    | uniform load 

    ''')

e__(''' some equations

    || functions | nodoc
    script1.py
    script2.py
    
    equation reference [r]_
    xx1 = gg + 4     

    || format |n:f 

    xx2 = hh + 10    
    
    [line]_

    || link | http:google.com

    ''')
#%%
t__(''' [03]_ Manipulate Tables (dataframes) and Plots    

    create a dataframe
    -------------------    
    || data | inline | T2 | optional description
    T2["len1"] = range(1,8)  
    T2["area1"] = range(10,17)  
    T2["prod1"] = T2["area1"]*T2["len1"]
    || save | test3.csv | T2 
    
    read csv file into dataframe
    ----------------------------
    || data | test1.csv  | T3 | optional description
    || select | T3 | cols = [], rows = []

    insert a table
    --------------
    || table : 20 | T3  
    Table title goes here

    plot data from csv file
    ----------------------------
    || data | plt1.csv | P1 | optional description
    || plot | P1 | x:len1, y:area1, type:line, grid:t
    || add  | P1 | x:len1, y:prod1, c:blue 
    || save | plt1.png | P1

    insert a plot
    -------------
    || image : 1 | tb1.png  
    Plot title goes here
    ''')

#write_values()
#write_utfcalc()
#write_pdfdoc()
#write_htmldoc()
#write_pdfreport()

