#! python 
#%%
from rivet.rivet_lib import *
r__(''' repository data
    || summary | section 
    The r__ function contains summary calc information
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

    || append | cover.pdf
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

    [line]_

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
    
    [line]_
    
    || table | ttext1.txt  | 50

    Render equations
    ---------------- 
                                                          ACI 318-05 5.5.1 [e]_
    || latex : 1 | x = \\frac{1 + \\omega}{2 + \\gamma} 

                                                          ACI 318-05 5.5.2 [e]_
    || sympy : 1 | x = (12 + omega + α) / (14 + gamma)  


    Render image file
    -----------------
    || image | pic1.png  | .5
    Inserted png file
        
    || image | pic2.jpg 

    Some added text xxxx is put here and a bit of nonsense to make some words
    for a paragraph.

                           Insert table or text from csv, rst or txt files [t]_
    || table | mercalli.csv  | 50
    
    note1: abc
    note2: def

                                                Rebar Table from reST file [t]_
    || table | rebars.rst  | 
    
                                                        Inline Table Title [t]_
    || table | inline  
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
    Some text about values. slsa sadlfksd sadfsfas  sadflkm sdflm saf
    afdak asdfas asflkm asf.
                                                        Steel Values [t]_
    a11 = 12.23*IN              | description 1, MM
    a22 = 2.2                   | description 2 
    a33 = 14                    | description 3 
    V1 = [1,4,3]*FT             | a vector, M         
    || values | v0103_testvalues.py | [:]
    ''')

e__(''' equations string
    Some introductory text.  Set equation format.

    || format | prec:2,trim:2
                                                        ACI 318-05 1.1 [e]_
    aa1 = a11*6*IN        | IN,M
    
    aa2 = V1*14*IN        | FT,mm
                                                        ACI 318-05 1.2 [e]_
    aa3 = (aa2 * 5)/a11             
    
    aa4 = BEAM1 * 7.2

    | fnct | scripts1.py | pin_pin(a11, a22) | FT*LB, N*M
    | fnct | scripts1.py | fixed_fixed(a11, a22) | FT*LB, N*M
    ''')
#%%
i__(''' [02]_ Seismic Analysis
    This is a test γ = 2*Σ of the system and this is a further test and
    another greek letter Γ₂.

    The need to distinguish between the various meanings of "frame of
    reference" has led to a variety of terms. For example, sometimes the
    type of coordinate. 
    
    [page]_

    || image2 | pic1.png, pic2.png | .5,.5 
    Inserted png file
    Side by side in docs

    The way it transforms to frames considered as related is emphasized as
    in Galilean frame of reference. Sometimes frames are distinguished by
    the scale of their observations, as in macroscopic and microscopic
    frames of reference [CIT2000]_.

    [cite]_ citation text
    ''')

v__(''' some values
    this is one line 4 γ
                                                        variable table [t]_
    gg = 5.4    | height of roof 
    hh = 12.2   | height of balcony
    w1 = 2.2    | uniform load 
    || vector | aisc13a.csv | BEAM1 : r4
    || vector | aisc13a.csv | BEAM2 : c2
    I_x = BEAM1[2]              | I major
    I_y = BEAM1[3]              | I minor
    I_z = BEAM1[2]              | I diagonal
    ''')

e__(''' some equations
                                                    equation reference [e]_
    xx1 = gg + 4     

    xx2 = hh + 10    

    [link]_ http:google.com
    ''')
#%%
t__(''' [03]_ Manipulate tables and plots    
    Test tables.

    create, modify and read tables
    ------------------------------    
    || data | T2 | description
    T2["len1"] = range(1,8)  
    T2["area1"] = range(10,17)  
    T2["prod1"] = T2["area1"]*T2["len1"]
    || save | T2 | plt1.csv

    Test plots.

    plot and save data from table
    -----------------------------
    || read | T4 | plt1.csv
    || plot | T4, P1 | x='len1',y='area1',kind='line',grid=True
    || add  | T4, P1 | x='len1', y='prod1' 
    || save | P1 | plt1.png

    || image | plt1.png | 1
                                                Plot caption goes here [f]

                                                            Table title [t]_
    || table | test1.csv | 40
    ''')
    
list_values()
#write_values()
#write_utfcalc()
#write_pdfdoc()
#write_htmldoc()
#write_pdfreport()

