#! python 
#%%
from rivet.rivet_lib import *

#%%  
i__(''' [[01]] Load Summations
    
    The need to distinguish between the various meanings of "frame of
    reference" has led to a variety of terms. For example, sometimes the type
    of coordinate system is attached as a modifier, as in Cartesian frame of
    reference [#]_.
    
    || [#] footnote text 1

    Sometimes the state of motion asfda asd s fdas sfdfasdfasdf is
    emphasized, as in rotating frame of reference. 

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
    
    ::

    Insert text from text, rst, docx or html files
    || text  | ttext1.txt  | i5
    
    Render equations
    || tex   | x = \\frac{1 + \\omega}{2 + \\gamma} | s.5,# |
    || ACI 318-05 5.5.1

    || sym | x = (1 + omega + α) / (4 + gamma)  | s.5,# |
    || ACI 318-05 5.5.2

    Render image file
    || img | pic1.png | s.5,# |  
    || inserted png file  
 
    || img | pic2.jpg  | s.5,# |
    || inserted jpg file   

    Some added text xxxx is put here and a bit of nonsense to make some
    words for a paragraph.

    Insert table from csv and rst files
    || table | mercalli.csv | r[0:5]c[0,1]w30 | 
    || Rebar Table from CSV file [#]_ 
    || [#] footnote text 2

    || table | rebars.rst  | 
    || Rebar Table from reST file
    
    || table | Table Title [#]_
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
    |        11 | 1.41  |   1.56 |        4.43 |     5.313 |
    +-----------+-------+--------+-------------+-----------+
    |        14 | 1.693 |   2.25 |        5.32 |     7.65  |
    +-----------+-------+--------+-------------+-----------+
    |        18 | 2.257 |   4    |        7.09 |    13.6   |
    +-----------+-------+--------+-------------+-----------+

    || [#] footnote text 3

    ''')

v__(''' some values 
    
    Some text if needed

    a11 = 12.23                 | description 1 
    a22 = 2.2                   | description 2 
    a33 = 14                    | description 3 
    
    aisc13.csv[4] => BEAM1      | property vector 
    I_x = BEAM1[2]              | I major
    I_y = BEAM1[3]              | I minor

    ''')

e__(''' equations header
    
    Some introductory text. xx

    aa2 = a11*14    | e2,r2,c1,s2,# | 
    equation label 1 - code reference 
     
    aa3 = aa2 * 5    | e2,r2,c0,s1,# |
    equation label 2

    aa4 = BEAM1[4] * 7.2  | e2,r2,c0,s1,# |
    equation label 3

    ''')
#%%
i__(''' [[02]] Seismic Analysis
    
    This is a test γ = 2*Σ of the system and this is a further test
    and another greek letter Γ₂.

    The need to distinguish between the various meanings of "frame of
    reference" has led to a variety of terms. For example, sometimes the type
    of coordinate

    || newpage

    The way it transforms to frames considered as related is emphasized as in
    Galilean frame of reference. Sometimes frames are distinguished by the
    scale of their observations, as in macroscopic and microscopic frames of
    reference [CIT2000]_.

    || [CIT2000] citation text

    ''')

v__(''' some values

    this is one line 4 γ
  
    gg = 5.4    | height of roof 
    hh = 12.2   | height of balcony
    w1 = 2.2    | uniform load 

    ''')

e__(''' some equations
    
    xx1 = gg + 4     | [2,2,0,#,1] |
    equation label and number

    xx2 = hh + 10    | [2,2,0,2,#]
    no equation label

    ''')

#%%
t__(''' [[03]] Manipulate Tables (dataframes) and Plots    

    read csv file into dataframe
    || read | T1 | rebars.csv  
    
    create and populate a table    
    || create | T2 | rebars2.csv
    T2["len1"] = range(1,8)  
    T2["area1"] = range(10,17)  
    T2["prod"] = T2["area1"]*T2["len1"]
    || save | table | T2
    
    insert a table
    || table | rebars2.rst |  rest |
    Deflection Table

    plot some data from csv 
    || plot | tb1.csv | x="dia", y="area", row=[1:10], kind="line", grid=1   
    || add  | x="dia", y="perimeter", color="blue"  |
    || save | plot | tb1.png | 

    || img | .5 | tb1.png |
    plot title

    ''')

r__(''' write calc, docs or report to files 

    write_utfcalc()
    #write_pdfdoc()
    #write_htmldoc()
    #write_pdfreport()
    
    ''')
